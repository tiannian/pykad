import route
import node
import queue
import random

class Swarm:
    def __init__(self, num):
        self.node = []
        self.route = []
        self.queue = []
        self.fnsended = {}
        self.fnrecved = {}
        self.fnhan = {}

        node0 = self.addNode(None)
        node0.port = 0

        for i in range(num):
            node1 = self.addNode(node0)
            node1.port = i + 1

    def addNode(self, n):
        node1 = node.newNode()
        table1 = route.RouteTable(20, node1)
        queue1 = queue.Queue()

        self.node.append(node1)
        self.route.append(table1)
        self.queue.append(queue1)

        if n != None:
            table1.addNode(n)
        return node1

    def tigger(self, i):
        print('togger n: %d' % (i))
        for i in range(len(self.node)):
            n = self.node[i]
            r = self.route[i]
            q = self.queue[i]

            if not q.empty():
                event = q.get()
                #  print(event, i)
                if event['from'] == i:
                    self.queue[event['to']].put(event)
                elif event['type'] == 'ping':
                    self.handle_ping(event['from'], event['to'])
                elif event['type'] == 'recv_ping':
                    self.handle_recv_ping(event['from'], i)
                elif event['type'] == 'find_node':
                    self.handle_find_node(event['from'], event['to'], event['data'])
                elif event['type'] == 'recv_find_node':
                    self.handle_recv_find_node(event['from'], event['to'], event['data'], event['target'], i)
            #  print("RouteTable size: %d/%d" %(r.nbucket(), r.nnode()))
        print()

    def ping(self, i, o):
        node0 = self.node[i]
        route0 = self.route[i]
        queue0 = self.queue[i]

        node1 = self.node[o]

        route0.addNode(node1)
        queue0.put({'type': 'ping', 'from': i, 'to': o})
        print('send `ping` from %d to %d' % (i, o))

    def handle_ping(self, f, t):
        print('recv `ping` from %d to %d' % (f,t))
        node0 = self.node[t]
        route0 = self.route[t]
        queue0 = self.queue[t]

        node1 = self.node[f]

        route0.addNode(node1)
        queue0.put({'type': 'recv_ping', 'from': t, 'to': f})
        print('send `recv ping` from %d to %d' % (t, f))

    def handle_recv_ping(self, f, t):
        print('recv `recv ping` op from %d to %d' % (f,t))
        node0 = self.node[t]
        route0 = self.route[t]
        queue0 = self.queue[t]

        node1 = self.node[f]

        route0.addNode(node1)

    def find_node(self, f, node, fnhan=None):
        node0 = self.node[f]
        route0 = self.route[f]
        queue0 = self.queue[f]

        target_nodes = route0.findNeighbors(node)
        if node.port != 1234:
            route0.addNode(node)

        self.fnhan[f] = fnhan

        for node1 in target_nodes:
            to = node1.port
            self.fnsended[node1.id] = True
            self.fnrecved[node1.id] = False
            queue0.put({'type': 'find_node', 'from': f, 'to': to, 'data': node})
            print('send `find node` from %d to %d' % (f, to))

    def handle_find_node(self, f, t, node):
        print('recv `find node` from %d to %d, data is %s' % (f,t,str(node)))
        node0 = self.node[t]
        route0 = self.route[t]
        queue0 = self.queue[t]

        target_nodes = route0.findNeighbors(node)
        route0.addNode(self.node[f])

        queue0.put({'type': 'recv_find_node', 'from': t, 'to': f, 'data': target_nodes, 'target': node})
        print('send `recv find node` from %d to %d, data is:' % (f,t))
        for node in target_nodes:
            print(node)
        print()

    def handle_recv_find_node(self, f, t, nodes, node, ti):
        print('recv `recv find node` from %d to %d, data is:' % (f,t))
        for node1 in nodes:
            print(node1)
        print()

        for node1 in nodes:
            if not node1.id in self.fnsended:
                self.fnsended[node1.id] = True
                self.queue[node1.port].put({'type': 'find_node', 'from': t, 'to': node1.port, 'data': node})
                self.fnrecved[node1.id] = False
                print('send `find node` from %d to %d' % (t, node1.port))

        from_node = self.node[f]
        if from_node.id in self.fnrecved:
            self.fnrecved[from_node.id] = True

        for k, v in enumerate(self.fnrecved):
            if not v:
                return

        print('find_node %d success' % (t))
        print(len(self.fnrecved.values()))
        if not self.fnhan[t] == None:
            self.fnhan[t](node, t, ti, len(self.fnrecved.values()))

    def bootstrap(self, i):
        self.find_node(i, self.node[i])

if __name__ == '__main__':
    swarm = Swarm(1000)
    
    for i in range(1000):
        swarm.bootstrap(i)
        swarm.tigger(i)

    for i in range(1000):
        swarm.tigger(i + 1000)

    random.seed(10)
    
    rem = {}
    
    result = {}

    others = {}

    def time(node, i, ti, other):
        print('find node: ',node)
        result[i] = ti - rem[i]
        others[i] = other

    for i in range(9000):
        cont = random.randint(0,2000)
        if cont < 1000:
            node0 = node.newNode()
            if swarm.fnhan[cont] == None:
                rem[cont] = i
                swarm.find_node(cont, node0, time)
                print('find node from ', cont, ' to ',node0)
        swarm.tigger(i + 2000)


    count = 0
    total = 0

    for d in result.values():
        if d > 0:
            count += 1
            total += d
    
    print('mean of time', total/count)

    import numpy as np

    print(np.mean(list(others.values())))

    size = []

    for route1 in swarm.route:
        size.append(route1.nnode())

    print(np.mean(size))

