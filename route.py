from utils import LRU
import node
import utils

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

    def hasInRange(self, node):
        return self.range[0] <= node.id <= self.range[1]

    def isFull(self):
        return len(self._nodes) == self.size

    def getBucketFor(self, node):
        return node.id < self.range[1]

    def prefix(self):
        return utils.prefix(self._nodes.keys())

    def __str__(self):
        strs = "\n".join([str(n) for n in self.getNodes()])
        return strs +'\n'

class RouteTable:
    def __init__(self, bucket_size, this):
        self._buckets = [KBucket(node.Node.min_nodeid, node.Node.max_nodeid, bucket_size)]
        self._this = this

    def addNode(self, node):
        index = self.getBucketFor(node)
        bucket = self._buckets[index]

        if not bucket.isFull():
            bucket.addNode(node)
        elif bucket.getBucketFor(self._this):
            one, two = bucket.split()
            if one.getBucketFor(node):
                one.addNode(node)
            else:
                two.addNode(node)
            self._buckets[index] = one
            self._buckets.insert(index + 1, two)
        else:
            # test node online
            pass

    def getBucketFor(self, node):
        for index, bucket in enumerate(self._buckets):
            if bucket.getBucketFor(node):
                return index

    def __str__(self):
        strs = "\n".join([ str(k) + '\n' + str(v) for k, v in enumerate(self._buckets)])
        return strs

if __name__ == '__main__':
    this = node.Node.this('config.json', 'localhost', 12345)
    print(this)

    table = RouteTable(20, this)

    for _ in range(100):
        node1 = node.newNode()
        table.addNode(node1)

    print(table)


