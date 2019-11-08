from collections import OrderedDict
import operator

class LRU(OrderedDict):
    'Limit size, evicting the least recently looked-up key when full'

    def __init__(self, maxsize=128, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]

def to_bit_string(i):
    return bin(i)[2:].rjust(160, '0')

def shared_prefix(args):
    i = 0
    while i < min(map(len, args)):
        if len(set(map(operator.itemgetter(i), args))) != 1:
            break
        i += 1
    return args[0][:i]

def prefix(nums):
    return len(shared_prefix([to_bit_string(i) for i in nums]))

if __name__ == '__main__':
    print(prefix([0xAC07,0xFFFFFFFFFFFFFFFF]))

