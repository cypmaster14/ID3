from Data import create_from_other
from copy import deepcopy


class Node:
    def __init__(self):
        self.name = None
        self.param = None
        self.children = {}  # pair value : child

    def decide(self, instance):
        if self.children:  # is not a leaf
            for k, v in self.children.items():
                if instance[self.param] == k:
                    break
            del instance[self.param]
            return v.decide(instance)
        else:
            return self.value

    def printTree(self, lvl):
        if self.children == None:
            return ("-" * lvl) + str(self.value) + "\n"
        else:
            s = ""
            for k, v in self.children.items():
                s += ("-" * lvl) + str(self.name) + "=" + str(k) + ":\n" + v.printTree(lvl + 1)
            return s


def getID3Tree(data):
    node = Node()
    if data.is_final():
        node.children = None
        node.value = sorted(data.counter.items(), key=lambda c: [1], reverse=True)[0][0]
    else:
        node.param = data.get_best_param()
        node.name = data.atribute[node.param]
        for value in sorted(set(data.instante[node.param])):
            node.children[value] = getID3Tree(create_from_other(data, node.param, value))
    return node
