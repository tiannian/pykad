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

    def __len__(self):
        return len(self._nodes.values())

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
        self.ksize = bucket_size

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

    def findNeighbors(self, node, k = None):
        k = k or self.ksize

        if self.nnode() < k:
            k = self.nnode()
        nodes = []

        for neighbor in TableTraverser(self, node):
            nodes.append(neighbor)
            if len(nodes) == k:
                break
        return nodes

    def __str__(self):
        strs = "\n".join(['KBucket index is:%s' % ( str(k) )+ '\n' + str(v) for k, v in enumerate(self._buckets)])
        return strs

    def nbucket(self):
        return len(self._buckets)

    def nnode(self):
        count = 0
        for bucket in self._buckets:
            count += len(bucket)
        return count

class TableTraverser(object):
    def __init__(self, table, startNode):
        index = table.getBucketFor(startNode)
        self.currentNodes = table._buckets[index].getNodes()
        self.leftBuckets = table._buckets[:index]
        self.rightBuckets = table._buckets[(index + 1):]
        self.left = True

    def __iter__(self):
        return self

    def __next__(self):
        """
        Pop an item from the left subtree, then right, then left, etc.
        """
        if len(self.currentNodes) > 0:
            return self.currentNodes.pop()

        if self.left and len(self.leftBuckets) > 0:
            self.currentNodes = self.leftBuckets.pop().getNodes()
            self.left = False
            return next(self)

        if len(self.rightBuckets) > 0:
            self.currentNodes = self.rightBuckets.pop(0).getNodes()
            self.left = True
            return next(self)

        raise StopIteration

if __name__ == '__main__':
    this = node.Node.this('config.json', 'localhost', 12345)

    table = RouteTable(20, this)
    print(table)

#      for _ in range(0):
    #      node1 = node.newNode()
    #      table.addNode(node1)
    #
    #  node1 = node.newNode()
    #  print(table.findNeighbors(node1))
#

    #  print(table)




