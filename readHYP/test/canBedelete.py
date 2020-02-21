
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
            unit = (key, activePins.get(key)[0])
            plane.append(unit)
            temp.append(unit)
            plane = findVCCGND(plane, key, segs, activePins, negtivePins, planeNames)
            # [端接无源器件名，端接的网络名]
            terminateInfo = []
            # 有端接
            if plane is not None:
                for ele in plane:
                    if ele[-1] != 'seg':
                        terminateInfo.append(ele[-1].split('.')[0])
                        if ele[-2][0] == 'net':
                            terminateInfo.append(ele[-2])
                terminateInfo = list(set(terminateInfo))
            signals = findAPin(signals, temp, key, segs, activePins, negtivePins)
            for model in signals:
                aPinInfo = []
                segsInfo = []
                for ele in model:
                    if ele[-1] == 'seg':
                        segsInfo.append(ele)
                    else:
                        aPinInfo.append(ele)
                models.append([aPinInfo, segsInfo, terminateInfo])
    # models: [[aPins, segs, 端接情况],...]
    return models


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
