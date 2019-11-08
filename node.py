import json
import nacl.utils
import nacl.encoding

def loadID(path):
    cf = open(path, 'r')
    config = json.load(cf)
    if not 'id' in config:
        idbytes = nacl.utils.random(size = 20)
        idstr = nacl.encoding.HexEncoder.encode(idbytes)
        config['id'] = idstr.decode()
        idint = int(idstr, base=16)
        wconfig = open(path, "w+")
        json.dump(config, wconfig)
        return idint
    else:
        idint = int(config['id'], base=16)
        return idint

def newNode():
    idbytes = nacl.utils.random(size = 20)
    idstr = nacl.encoding.HexEncoder.encode(idbytes)
    idint = int(idstr, base=16)
    return Node(idint, "localhost", 1234)

class Node:
    def __init__(self, _id, _address, _port):
        self.id = _id
        self.address = str(_address)
        self.port = int(_port)

    def distance(self, node):
        return self._id ^ node._id

    def __str__(self):
        return "(%s, %s, %d)" % (hex(self.id), self.address, self.port)

Node.max_nodeid = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
Node.min_nodeid = 0x0

if __name__ == '__main__':
    idint = loadID('config.json')
    print(idint)

    node = Node(idint, "localhost", 12345)
    print(node)

