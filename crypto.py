import os.path
import json
import nacl.encoding
import nacl.signing
import nacl.utils

def loadID(path):
    if os.path.exists(path):
        idf = open(path)
        config = json.load(idf)
        seed = None
        if config['private_key'] == None:
            seed = nacl.utils.random()
            config['private_key'] = nacl.encoding.HexEncoder.encode(seed)
            cwriter = open(path, "w+")
            json.dump(config, cwriter)
        else:
            seed = nacl.encoding.HexEncoder.decode(config['private_key'])
        pass
    else:
        raise "Can't find config file."
