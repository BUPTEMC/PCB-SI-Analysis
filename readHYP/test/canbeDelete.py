<<<<<<< HEAD
import HYPF2D as C

hyp5 = "../files/HYP2/demo2.hyp"
csv5 = "../files/HYP2/demo2.csv"

nets = C.getNetNames("../files/HYP2/mainboard.hyp")
print(nets)
pins = C.getActiveAndNegtivePins("../files/HYP2/demo2.csv")
segs, aPins, nPins = C.getSegsAndPins(hyp5, csv5)
models = C.sortModels(aPins, nPins, segs, ['vcc', 'gnd'])
layers, _ = C.getLayersInfo(hyp5, 11)
# print(layers)


def check(models):
    for idx, model in enumerate(models):
        # print(model[1][0])
        if model[1][0] is None:
            return idx
        else:
            segHead = model[1][0]
            print(segHead[0][0][0], segHead[0][0][1])


# check(models)

# C.readHYP2File(hyp5, csv5, "../files/HYP2/output/demo.csv", ['vcc', 'gnd'])
# print(models)
=======
import HYPF2D as C

hyp5 = "../files/HYP2/demo2.hyp"
csv5 = "../files/HYP2/demo2.csv"

nets = C.getNetNames("../files/HYP2/mainboard.hyp")
print(nets)
pins = C.getActiveAndNegtivePins("../files/HYP2/demo2.csv")
segs, aPins, nPins = C.getSegsAndPins(hyp5, csv5)
models = C.sortModels(aPins, nPins, segs, ['vcc', 'gnd'])
layers, _ = C.getLayersInfo(hyp5, 11)
# print(layers)


def check(models):
    for idx, model in enumerate(models):
        # print(model[1][0])
        if model[1][0] is None:
            return idx
        else:
            segHead = model[1][0]
            print(segHead[0][0][0], segHead[0][0][1])


# check(models)

# C.readHYP2File(hyp5, csv5, "../files/HYP2/output/demo.csv", ['vcc', 'gnd'])
# print(models)
>>>>>>> 43888ac89e41450472c750f6e8d67c4bfa5e6ee8
