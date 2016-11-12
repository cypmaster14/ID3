from Data import Data
from Tree import learn

d = Data()

d.load_from_file("tennis.data", 4)
d._set_debug(["outlook", "temperature", "humidity", "wind", ])

tree = learn(d)

print tree.debug(0)
# print tree.decide(["low","high","2","4","med","low"])
# print tree.decide(["low","low","2","more","small","high"])



# print d.get_all_entropy()
