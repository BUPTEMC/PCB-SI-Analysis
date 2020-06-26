<<<<<<< HEAD
import HYPF2D as C
import HYPF2D_Iter as CC
import re

segs = {
        (0, 0): [((1, 0), 1, 1)],
        (1, 0): [((0, 0), 1, 1), ((2, 1), 1, 1)],
        (2, 1): [((3, 2), 1, 1)],
        (2, 2): [((1, 2), 1, 1)],
        (1, 2): [((2, 2), 1, 1)],
        (3, 2): [((2, 1), 1, 1), ((3, 3), 1, 1), ((4, 2), 1, 1)],
        (4, 2): [((3, 2), 1, 1)],
        (5, 0): [((4, 1), 1, 1)],
        (3, 3): [((3, 2), 1, 1)],
        (3, 4): [((3, 5), 1, 1)],
        (3, 5): [((3, 4), 1, 1)]
}
aPins = {
        (0, 0): ("U11", 1),
        (1, 2): ("U32.1", 1),
        (3, 5): ("FF22", 1)
    }

# (坐标：(器件名.引脚号，net)) 和 （器件名：[（坐标，net，引脚号）]）
nPins = {
        (3, 3): ("R32.1", 1),
        (3, 4): ("R32.2", 1),
        (4, 2): ("C1.1", 1),
        (4, 1): ("C1.2", "gnd"),
        (2, 1): ("C9.1", 1),
        (2, 2): ("C9.2", 1),
        "C9": [((2, 1), 1, 1), ((2, 2), 1, 2)],
        "R32": [((3, 3), 1, 1), ((3, 4), 1, 2)],
        "C1": [((4, 1), "gnd", 2), ((4, 2), 1, 1)]
}
names = ["gnd"]

model1 = []
model2 = []
_model = []
models = []
plane = C.findVCCGND(model1, (0, 0), segs, aPins, nPins, names)
# print(plane)
signals = C.findAPin(models, model2, (0, 0), segs, aPins, nPins)
# print(signals)
models = C.genModel(signals, plane)
# print(models)
# finalModels = C.generateModels(aPins, nPins, segs, names)

# _models = C.sortModels(aPins, nPins, segs, names)
# print(_models)

# _line = "(SIGNAL L=Top T=0.0014)"
# _line = re.split(r'[ ](?![^=]*\")', _line)
# print(_line)

# models = CC.findAPinPath(segs, aPins, nPins)
models = CC.findAPinPath((0, 0), [], aPins, nPins, segs)
# terminate = CC.findVCCAndGNDPath((0,0),[],aPins, nPins, segs, names)
print(models)
# print(signals[1])
=======
import HYPF2D as C
import HYPF2D_Iter as CC
import re

segs = {
        (0, 0): [((1, 0), 1, 1)],
        (1, 0): [((0, 0), 1, 1), ((2, 1), 1, 1)],
        (2, 1): [((3, 2), 1, 1)],
        (2, 2): [((1, 2), 1, 1)],
        (1, 2): [((2, 2), 1, 1)],
        (3, 2): [((2, 1), 1, 1), ((3, 3), 1, 1), ((4, 2), 1, 1)],
        (4, 2): [((3, 2), 1, 1)],
        (5, 0): [((4, 1), 1, 1)],
        (3, 3): [((3, 2), 1, 1)],
        (3, 4): [((3, 5), 1, 1)],
        (3, 5): [((3, 4), 1, 1)]
}
aPins = {
        (0, 0): ("U11", 1),
        (1, 2): ("U32.1", 1),
        (3, 5): ("FF22", 1)
    }

# (坐标：(器件名.引脚号，net)) 和 （器件名：[（坐标，net，引脚号）]）
nPins = {
        (3, 3): ("R32.1", 1),
        (3, 4): ("R32.2", 1),
        (4, 2): ("C1.1", 1),
        (4, 1): ("C1.2", "gnd"),
        (2, 1): ("C9.1", 1),
        (2, 2): ("C9.2", 1),
        "C9": [((2, 1), 1, 1), ((2, 2), 1, 2)],
        "R32": [((3, 3), 1, 1), ((3, 4), 1, 2)],
        "C1": [((4, 1), "gnd", 2), ((4, 2), 1, 1)]
}
names = ["gnd"]

model1 = []
model2 = []
_model = []
models = []
plane = C.findVCCGND(model1, (0, 0), segs, aPins, nPins, names)
# print(plane)
signals = C.findAPin(models, model2, (0, 0), segs, aPins, nPins)
# print(signals)
models = C.genModel(signals, plane)
# print(models)
# finalModels = C.generateModels(aPins, nPins, segs, names)

# _models = C.sortModels(aPins, nPins, segs, names)
# print(_models)

# _line = "(SIGNAL L=Top T=0.0014)"
# _line = re.split(r'[ ](?![^=]*\")', _line)
# print(_line)

# models = CC.findAPinPath(segs, aPins, nPins)
models = CC.findAPinPath((0, 0), [], aPins, nPins, segs)
# terminate = CC.findVCCAndGNDPath((0,0),[],aPins, nPins, segs, names)
print(models)
# print(signals[1])
>>>>>>> 43888ac89e41450472c750f6e8d67c4bfa5e6ee8
