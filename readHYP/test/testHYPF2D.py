import HYPF2D as C
import HYPF2D_Iter as CC

path = "../files/SampleAD-02-AD.HYP"
path2 = "../files/demo.hyp"
path3 = "../files/hyp/SampleAD-01.HYP"
csvPath = "../files/test.csv"
csvPath2 = "../files/test2.csv"
outputPath = "../files/out.csv"
planeNames = ['VOUT2', 'D+4.5V', '+3.3VA_VCCT', '+3.3VA_VCCR', 'VCCINT','INTVCC', 'DVDD+2.5V', 'DV+24V', 'DVDD+1.5V', 'GND', 'DVDD+3.3V']
planeNames2 = ['vcc','gnd']
# layers, _ = C.getLayersInfo(path2, 12)
# print(layers)
# devices, _ = C.getDevicesInfo(path2)
# print(devices)
# pins = C.getActiveAndNegtivePins(csvPath)
# segs, aPins, nPins = C.getSegsAndPins(path, csvPath)
# nets = C.getNetNames(path2)
# segs, aPins, nPins = C.getSegsAndPins(path, csvPath)
# models = C.generateModels(aPins, nPins, segs, planeNames2)
# models = CC.sortModels(aPins, nPins, segs, planeNames)
# print(models)
# models1 = CC.findAllAPinPath(segs, aPins, nPins)
# models2 = C.sortModels(aPins, nPins, segs, planeNames)
# print(len(models1))
# print(len(models2))
# print(models[0][1][0])
# C.readHYP2File(path2, csvPath2, outputPath, planeNames2)
# model = [(('3.2500', '0.7000'), 'U4.15')]
# models = []
# key = model[0][0]
# ll = C.findAPin(models, model, key, segs, aPins, nPins)
# print(ll)
# pins = C.getActiveAndNegtivePins(csvPath2)
# print(aPins)
# print(models)
# print(aPins.get((5.2250, 0.8750)))
# print(devices)
# models = C.readHYP2File(path2, csvPath2, "", planeNames2)
# for model in models:
#     print(model)
#     pass
    # print(model)
# print(len(models))

net = CC.getNetNames(path3)
print(net)
