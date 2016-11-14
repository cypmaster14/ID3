from Data import Data
from Tree import getID3Tree

d = Data()

# Code for play tennis

d.load_from_file("tennis.data", 4)
d.set_atribute(["outlook", "temperature", "humidity", "wind"])
tree = getID3Tree(d)

print(tree.printTree(0))
print(tree.decide(["sunny", "cool", "high", "strong"]))

# Code for car example

# d.load_from_file("car.data", 6)
# d.set_atribute(["buying", "maint", "doors", "persons", "lug_boot", "safety"])
#
# tree = getID3Tree(d)
#
# print(tree.printTree(0))
# print(tree.decide(["low", "high", "2", "4", "med", "low"]))
# print(tree.decide(["low", "low", "2", "more", "small", "high"]))
