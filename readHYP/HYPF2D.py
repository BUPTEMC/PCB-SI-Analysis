import os
import re
import copy
import pandas as pd
import numpy as np

def getNetNames(path):
    nets = []
    with open(path, 'r') as f:
        for line in f.readlines():
            if line[:4] == "{NET":
                nets.append(line[5:-1])
    return nets

def getLayersInfo(path, N=0):
    """
    读取HYP文件的层叠信息
    :param path: 文件路径
    :param N: 从第N行开始读文件
    :return: 1. layers = {层名:(第几层, 层的材料)}; 2. idx = 层信息结束的行数
    """
    with open(path, 'r') as f:
        layers = {}
        num = 1
        idx = 0
        flag = False
        for i, line in enumerate(f.readlines()[N:]):
            # 读取结束, 返回层信息
            if line[:-1] == "}" and flag:
                flag = False
                idx = i + N + 1
                return layers, idx
            # 读到"STACKUP", 开启层信息的读取
            if line[1:-1] == "STACKUP":
                flag = True
                continue

            # 读取层信息
            if flag:
                _line = line.strip()
                _line = re.split(r'[ ](?![^=]*\")', _line)
                # 读取信号层的信息
                if _line[0][1:] == "PLANE" or _line[0][1:] == "SIGNAL":
                    for info in _line:
                        # 层名
                        if info[0] == 'L':
                            # 去掉结尾的')'
                            if info[-1] == ')':
                                layerName = info[2:-1]
                            else:
                                layerName = info[2:]
                        # 材料
                        if info[0] == 'M':
                            # 去掉结尾的')'\
                            if info[-1] == ')':
                                material = info[2:-1]
                            else:
                                material = info[2:]
                        else:
                            material = 0
                    layerInfo = (num, material)
                    num = num + 1
                    layers.update({layerName: layerInfo})
                # 读取介质层的信息
                if _line[0][1:] == "DIELECTRIC":
                    continue
        return layers, idx


def getDevicesInfo(path, N=0):
    """
    读取HYP文件的设备信息
    :param path: 文件路径
    :param N: 从第N行开始读文件
    :return: 1. devices:["设备名"]; 2. 设备信息到第几行结束
    """
    # 从一行中找到设备信息的正则表达式
    rule = re.compile('REF=[a-zA-Z]*[0-9]*')
    idx = 0
    with open(path, 'r') as f:
        flag = False
        devices = []
        for i, line in enumerate(f.readlines()[N:]):
            if flag and line[:-1] == '}':
                flag = False
                idx = i + N + 1
                return devices, idx
            if line[1:-1] == 'DEVICES':
                flag = True
                continue
            if flag:
                device = rule.findall(line)
                devices.append(device[0][4:])
        return devices, idx


def getSegsAndPins(path, csvPath, N=0):
    """
    找到HYP文件中所有的线段和管脚
    :param path: 文件路径
    :param N: 从第N行开始读文件
    :return: 1. segs:{坐标点1:[(与坐标点1相连的坐标点a, 线宽, 线段所在的层),(...)]}
             2. aPins:{坐标点：(器件名.管脚号，所在网络)}
             3. nPins:{坐标点：(器件名.管脚号，所在网络)} 和 {器件名: [(坐标，所在网络，管脚号)]}
    """
    # pins里包含了所有的有源器件和无源器件
    pins = getActiveAndNegtivePins(csvPath)
    segs = {}
    aPins = {}
    nPins = {}
    flag = False
    with open(path, 'r') as f:
        for i, line in enumerate(f.readlines()[N:]):
            if line[:] == '{END}':
                return segs, aPins, nPins
            if flag and line[:-1] == '}':
                flag = False
                continue
            if line[1:4] == 'NET':
                flag = True
                net = line[5:-1]
                continue 
            if flag:
                # 首尾去空格
                line = line.strip()
                if line[1:4] == 'SEG':
                    _line = re.split(r'[ ](?![^=]*\")', line)
                    coord1 = (_line[1][3:], _line[2][3:])
                    coord2 = (_line[3][3:], _line[4][3:])
                    width = _line[5][2:]
                    layer = _line[6][2:-1]
                    if segs.get(coord1) is None:
                        segs.update({coord1: [(coord2, width, layer)]})
                    else:
                        pointList = segs.get(coord1)
                        pointList.append((coord2, width, layer))
                        segs.update({coord1: pointList})
                    if segs.get(coord2) is None:
                        segs.update({coord2: [(coord1, width, layer)]})
                    else:
                        pointList = segs.get(coord2)
                        pointList.append((coord1, width, layer))
                        segs.update({coord2: pointList})
                    continue
                if line[1:4] == 'PIN':
                    _line = re.split(r'[ ](?![^=]*\")', line)
                    coord = (_line[1][2:], _line[2][2:])
                    # 找到 器件名.管脚
                    device = re.findall(r'[^=]*\.[^\)]*', _line[3])[0]
                    _device = device.split('.')
                    deviceName = _device[0]
                    pinNum = _device[1]
                    attr = pins.get(deviceName)
                    if attr is None or attr is 0:
                        nPins.update({coord: (device, net)})
                        if nPins.get(deviceName) is None:
                            nPins.update({deviceName: [(coord, net, pinNum)]})
                        else:
                            pointList = nPins.get(deviceName)
                            pointList.append((coord, net, pinNum))
                            nPins.update({deviceName: pointList})
                    else:
                        aPins.update({coord: (device, net)})
                    continue
        return segs, aPins, nPins

def getActiveAndNegtivePins(csvPath):
    """
    找出电路板上所有的pins，并用0/1表示为有源器件或无源器件
    目前一个器件的管脚数量大于2则判断为有源器件
    :param csvPath: 从AD中导出的csv文件
    :return: pins ： {器件名：0/1} （0表示无源，1表示有源）
    """
    pins = {}
    df = pd.read_csv(csvPath, encoding="GBK")
    nDf = df[df["Pins"] <= 2]
    aDf = df[df["Pins"] > 2]
    nPinList = nDf["Designator"]
    aPinList = aDf["Designator"]
    for nPin in nPinList:
        tempList = nPin.split(",")
        for e in tempList:
            pins.update({e:0})
    for aPin in aPinList:
        tempList = aPin.split(",")
        for e in tempList:
            pins.update({e:1})
    return pins

def generateModels(activePins, negtivePins, segs, planeNames):
    keys = activePins.keys()
    models = []
    # 确定dfs的起点,必从有源器件开始
    # TODO
    # (这里是有瑕疵的，但是我懒得改了，应该是从有源output出发, 到input结束最合理)
    # 但是我们看文件不可能知道哪里是output，哪里是input，所以这个问题只能留给后人处理了，问题对结果影响不大
    for key in keys:
        # 如果有源器件的管脚没有连接，则继续
        if segs.get(key) is None or len(segs.get(key)) == 0:
            continue
        else:
            temp = []
            plane = []
            # 信号层
            signals = []
            _models = []
            # (坐标， 器件名.管脚号)
            unit = (key, activePins.get(key)[0])
            # 找到一个所有连接到的plane层的线路
            # 确定起点
            plane.append(unit)
            temp.append(unit)
            plane = findVCCGND(plane, key, segs, activePins, negtivePins, planeNames)
            signals = findAPin(signals, temp, key, segs, activePins, negtivePins)
            _models = genModel(signals, plane)
            tempModels = copy.deepcopy(_models)
            models.append(tempModels)
    return models

def findVCCGND(model, key, segs, aPins, nPins, planeNameList):
    """
    从一个点出发，找到与这个点连接的所有终点为Plane层的线路，实际上连接一个就ok了，不然没意义,此步判断是否有端接
    :param model: 每次迭代保持更新的线路
    :param key: 起点坐标， 一个tuple
    :param segs: {坐标点1:[(与坐标点1相连的坐标点a, 线宽, 线段所在的层),(...)]}
    :param aPins: {坐标点：(器件名.管脚号，所在网络)}
    :param nPins: {坐标点：(器件名.管脚号，所在网络)} 和 {器件名: [(坐标，所在网络，管脚号)]}
    :param planeNameList: plane层在这个电路中的名字列表
    :return:
    """
    segList = segs.get(key)
    if segList == None:
        return None
    for seg in segList:
        # 防止seg重复, 保证每条路不回头
        tempList = segs.get(seg[0])
        for i, elem in enumerate(tempList):
            if elem[0] == key:
                tempList.pop(i)
                segs.update({seg[0]: tempList})
                break
        # 先存储线段：（（左，右），宽度， 层，’seg'）
        unit = ((key, seg[0]), seg[1], seg[2], 'seg')
        model.append(unit)
        aPin = aPins.get(seg[0])
        nPin = nPins.get(seg[0])
        if aPin is not None:
            net = aPin[1]
            if net in planeNameList:
                model.append((seg[0], ('net', net), aPin[0], 'aPin'))
                # 一条SI模型中只允许一个接地或电源，不然没意义
                return model
        if nPin is not None:
            net = nPin[1]
            if net in planeNameList:
                model.append((seg[0], ('net', net), nPin[0], 'nPin'))
                return model
            else:
                # (坐标， 无源器件名.管脚号)
                unit = (seg[0], nPin[0], 'nPin')
                model.append(unit)
                name = nPin[0].split('.')[0]
                _nPins = nPins.get(name)
                for nPin in _nPins:
                    if nPin[0] == seg[0]:
                        continue
                    net = nPin[1]
                    unit = ((seg[0], nPin[0]), seg[1], seg[2], 'seg')
                    model.append(unit)
                    if net in planeNameList:
                        # （坐标，网络名，无源器件名.管脚号）
                        model.append((nPin[0], ('net', net), name+'.'+str(nPin[2]), 'nPin'))
                        return model
                    else:
                        unit = (nPin[0], name+'.'+str(nPin[2]), 'nPin')
                        model.append(unit)
                        _model = findVCCGND(model, nPin[0], segs, aPins, nPins, planeNameList)
                        if _model is not None:
                            return _model
                        model.pop(len(model) - 1)
                    model.pop(len(model) - 1)
                model.pop(len(model) - 1)
        _model = findVCCGND(model, seg[0], segs, aPins, nPins, planeNameList)
        if _model is not None:
            return _model
        model.pop(len(model) - 1)
    return None

def findAPin(models, model, key, segs, aPins, nPins):
    """
    从一个点开始，找到所有终点为有源器件的线路(这个代码可以被优化的，主要是参数可能不需要这么多)
    :param models: 用于迭代更新的线路列表，列表里面每一个元素都是一个线路，入参为空列表就行
    :param model: 用于迭代更新的线路, 入参为空列表就行
    :param key: 起点坐标, 一个tuple
    :param segs: {坐标点1:[(与坐标点1相连的坐标点a, 线宽, 线段所在的层),(...)]}
    :param aPins: {坐标点：(器件名.管脚号，所在网络)}
    :param nPins: {坐标点：(器件名.管脚号，所在网络)} 和 {器件名: [(坐标，所在网络，管脚号)]}
    :return: 从key起，所有终点是有源pin的线路(有返回值是为了让这个函数更清晰，其实没有也行)
    """
    segList = segs.get(key)
    if segList is None:
        return None
    for seg in segList:
        # 防止seg重复
        tempList = segs.get(seg[0])
        for i, elem in enumerate(tempList):
            if elem[0] == key:
                tempList.pop(i)
                segs.update({seg[0]: tempList})
                break
        # 先存储线段：（（左，右），宽度， 层，’seg'）
        unit = ((key, seg[0]), seg[1], seg[2], 'seg')
        model.append(unit)
        aPin = aPins.get(seg[0])
        nPin = nPins.get(seg[0])
        if aPin is not None:
            unit = (seg[0], aPin[0], 'aPin')
            model.append(unit)
            _temp = copy.deepcopy(model)
            models.append(_temp)
            model.pop(len(model) - 1)
            model.pop(len(model) - 1)
            continue
        if nPin is not None:
            # (坐标， 无源器件名)
            unit = (seg[0], nPin[0], 'nPin')
            model.append(unit)
            name = nPin[0].split('.')[0]
            _nPins = nPins.get(name)
            for nPin in _nPins:
                if nPin[0] == seg[0]:
                    continue
                unit = ((seg[0], nPin[0]), seg[1], seg[2], 'seg')
                model.append(unit)
                unit = (nPin[0], name+'.'+str(nPin[2]), 'nPin')
                model.append(unit)
                findAPin(models, model, nPin[0], segs, aPins, nPins)
                model.pop(len(model) - 1)
                model.pop(len(model) - 1)
            model.pop(len(model) - 1)
            model.pop(len(model) - 1)
            continue
        findAPin(models, model, seg[0], segs, aPins, nPins)
        model.pop(len(model) - 1)
    return models


def sortModels(activePins, negtivePins, segs, planeNames):
    keys = activePins.keys()
    # 一个model应该有有源pin，端接情况（端接电阻，端接电容，接地电压），线段
    models = []
    for key in keys:
        if segs.get(key) is None or len(segs.get(key)) == 0:
            continue
        else:
            temp = []
            plane = []
            signals = []
            unit = (key, activePins.get(key)[0], 'aPin')
            temp.append(unit)
            plane = findVCCGND(plane, key, segs, activePins, negtivePins, planeNames)
            # [端接无源器件名，端接的网络名]
            terminateInfo = []
            # 有端接
            if plane is not None:
                for ele in plane:
                    if ele[-1] == 'nPin':
                        terminateInfo.append(ele[-2].split('.')[0])
                        if ele[-3][0] == 'net':
                            terminateInfo.append(ele[-3][1])
                terminateInfo = list(set(terminateInfo))
            signals = findAPin(signals, temp, key, segs, activePins, negtivePins)
            for model in signals:
                aPinInfo = []
                segsInfo = []
                for ele in model:
                    if ele[-1] == 'seg':
                        segsInfo.append(ele)
                    else:
                        # Attention: 在aPinInfo里可能存在nPin，在最后的生成文件数据的时候要排查出来加入端接的信息
                        aPinInfo.append(ele)
                models.append([aPinInfo, segsInfo, terminateInfo])
    # models: [[aPins, segs, 端接情况],...]
    return models

def genModel(signals, plane):
    """
    内部函数，主要用来整合到有源pin和到plane层线路，防止重复
    :param signals: 到有源pin的线路列表
    :param plane: 到plane层的线路列表
    :return: 整合好的SI高速模型
    """
    models = []
    if plane is None:
        for elem in signals:
            if elem is None:
                continue
            else:
                models.append(elem)
        return models
    for elem in signals:
        if elem is None:
            continue
        elem = elem + plane
        elem = list(set(elem))
        models.append(elem)
    return models

def readHYP2File(HYPPath, csvPath, outputPath, planeNames):
    """
    :param HYPPath: HYP文件
    :param csvPath: 电路板器件对应的表
    :param outputPath: 训练用data输出的地址
    :param planeNames: 电源层网络名和地层网络名，客户应该提供这个，不然起名五花八门的没法搞
    :return:
    """
    layers, idx = getLayersInfo(HYPPath)
    devices, idx = getDevicesInfo(HYPPath, idx)
    segs, aPins, nPins = getSegsAndPins(HYPPath, csvPath, idx)
    pins = getActiveAndNegtivePins(csvPath)
    models = sortModels(aPins, nPins, segs, planeNames)
    # 对models进行处理， 使数据达到相同维度
    segMaxDim = 50
    pinMaxDim = 2
    datas = []
    for model in models:
        data = []
        nPinNames = []
        aPinsData = []
        segsData = []
        pinDim = 0
        segDim = 0
        res = 0
        capacity = 0
        volt = 0
        for aPin in model[0]:
            if pinDim >= pinMaxDim:
                break
            if aPin[-1] == "aPin":
                # 如果是aPin需要添加aPin的属性
                name = aPin[1]
                # TODO:通过名字和管脚号在这里写入读文件的代码半自动化生成数据
                # 每个pin：输入输出flag，输入电容，输出电阻，信号上升下降时间
                # 最后添加：传输延迟，工作频率
                # 这里先存默认值：输入电容20，输入电阻100，上升下降0以及坐标
                aPinsData.extend([20, 100, 0, aPin[0][0], aPin[0][1]])
                pinDim += 1
            elif aPin[-1] == 'nPin':
                # 保存nPin的情况
                nPinNames.append(aPin[1].split('.')[0])
        while pinDim < pinMaxDim:
            aPinsData.extend([0, 0, 0, 0, 0])
            pinDim += 1
        # aPin输入完成后统一属性有传输延迟0，工作频率133
        aPinsData.extend([0, 133])
        data.extend(aPinsData)
        # 保存线段，最大100条
        segsHead = model[1][0]
        # 坐标，宽度，层的编号（层的材料暂时没加）
        segsData.extend([segsHead[0][0][0], segsHead[0][0][1], segsHead[1], layers.get(segsHead[2])[0]])
        for seg in model[1]:
            if segDim >= segMaxDim:
                break
            segsData.extend([seg[0][1][0], seg[0][1][1], seg[1], layers.get(seg[2])[0]])
            segDim += 1
        while segDim < segMaxDim:
            segsData.extend([0, 0, 0, 0])
            segDim += 1
        data.extend(segsData)
        for nPin in model[2]:
            #TODO:在这里写入端接电阻电容的值by无源器件的名字
            #TODO：通过网络名判断此条传输线上的电压大小
            if nPin in planeNames:
                volt = -1
        data.extend([res, capacity, volt])
        _data = copy.deepcopy(data)
        datas.append(_data)
    pd.DataFrame(datas).to_csv(outputPath, index = False, header = False)
    return pd.DataFrame(datas)

