import asyncio
import json

class Protocol:
    def __init__(self, node, table):
        self._node = node
        self._table = table

    async def ping(self, node):
        (reader, writer) = await asyncio.open_connection(
                node.address, 
                node.port, 
                local_addr=(self._node.address, self._node.port)
                )
        data = {
                'code': 'ping',
                'from': {
                    'address': self._node.address,
                    'port': self._node.port
                    }
                }

        datastr = json.dumps(data)

        writer.write(datastr + '\n')
    
    async def find_node(self, node, target):
        (reader, writer) = await asyncio.open_connection(
                node.address, 
                node.port, 
                local_addr=(self._node.address, self._node.port)
                )
        data = {
                'code': 'find_node',
                'from': {
                    'address': self._node.address,
                    'port': self._node.port
                    },
                'data': target
                }

        datastr = json.dumps(data)

        writer.write(datastr + '\n')

        await writer.drain()

        recvstr = await reader.readline()


