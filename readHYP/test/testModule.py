<<<<<<< HEAD
import re
import pandas as pd
s = "R=Up10.2"
test = re.findall(r'[^=]*\.[^\)]*', s)[0]
_test = test.split('.')

l = [1,2,3]
# print(l)
pp = (0,1,2,3,4)
temp = pd.DataFrame([[1,2,3,4],[4,5,6,7]])
l.extend([4,5,6,7])

test = "{STACKUP\n"

print(test[1:-1] == "STACKUP")


test = {'a':123, 'b':456}
for i in test.keys():
    print(i)

nPins = {"a": 123, "b":456}
nPins.pop("a")
print(nPins)
=======
import re
import pandas as pd
s = "R=Up10.2"
test = re.findall(r'[^=]*\.[^\)]*', s)[0]
_test = test.split('.')

l = [1,2,3]
# print(l)
pp = (0,1,2,3,4)
temp = pd.DataFrame([[1,2,3,4],[4,5,6,7]])
l.extend([4,5,6,7])

test = "{STACKUP\n"

print(test[1:-1] == "STACKUP")


test = {'a':123, 'b':456}
for i in test.keys():
    print(i)

nPins = {"a": 123, "b":456}
nPins.pop("a")
print(nPins)
>>>>>>> 43888ac89e41450472c750f6e8d67c4bfa5e6ee8
