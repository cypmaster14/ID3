from Data import Data
from Tree import getID3Tree

d = Data()

d.load_from_file("tennis.data", 4)
d.set_atribute(["outlook", "temperature", "humidity", "wind"])
tree = getID3Tree(d)

print tree.printTree(0)
print tree.decide(["sunny", "cool", "high", "strong"])
