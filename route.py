from utils import LRU
import node

class KBucket:
    def __init__(self, lower, upper, size):
        self.range = (lower, upper)
        self.size = size
        self._nodes = LRU(maxsize = size)

    def getNodes(self):
        return list(self._nodes.values())

    def addNode(self, node):
        self._nodes[node.id] = node

    def delNode(self, nodeid):
        self._nodes.move_to_end(nodeid, last=False)

    def split(self):
        midpoint = (self.range[0] + self.range[1]) / 2
        one = KBucket(self.range[0], midpoint, self.size)
        two = KBucket(midpoint + 1, self.range[1], self.size)
        for node in self._nodes.values():
            bucket = one if node.id <= midpoint else two
            bucket._nodes[node.id] = node
        return (one, two)

class RouteTable:
    def __init__():
        pass

if __name__ == '__main__':
    kbucket = KBucket(node.Node.min_nodeid, node.Node.max_nodeid, 4)

    node1 = node.newNode()
    kbucket.addNode(node1)

    node1 = node.newNode()
    kbucket.addNode(node1)

    node1 = node.newNode()
    kbucket.addNode(node1)

    node1 = node.newNode()
    kbucket.addNode(node1)

    for n in kbucket.getNodes():
        print(n)
    print("----------------------")

    (one, two) = kbucket.split()

    for n in one.getNodes():
        print(n)
    
    print("----------------------")

    for n in two.getNodes():
        print(n)

