import HYPF2D as C

path = "../files/SampleAD-02-AD.HYP"
path2 = "../files/demo.hyp"
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
segs, aPins, nPins = C.getSegsAndPins(path2, csvPath2)
# models = C.generateModels(aPins, nPins, segs, planeNames2)
models = C.sortModels(aPins, nPins, segs, planeNames2)
# print(models[0][1][0])
C.readHYP2File(path2, csvPath2, outputPath, planeNames2)
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

