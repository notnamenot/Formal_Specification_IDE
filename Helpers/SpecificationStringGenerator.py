import json
from io import StringIO
from Helpers.State import WORD, COND,  ALT, LOOP

class SpecificationStringGenerator:
    def __init__(self, connections):

        io = StringIO(json.dumps(connections, cls=SetEncoder, indent=4))
        self.connections = json.load(io)

        self.leaves = []

        #flag to expression
        self.last_printed = ''
        self.left_par = 0
        self.right_par = 0

    def create_specification_string2(self):

        # simplify Cond
        new_conds = {}
        for cond in self.connections[COND]:
            words = []
            for e in self.connections[COND][cond]:
                words.append(e[WORD])
            new_conds[cond] = words
        self.connections[COND] = new_conds

        # simplify Alt
        new_alts = {}
        for alt in self.connections[ALT]:
            words = []
            for e in self.connections[ALT][alt]:
                words.append(e[WORD])
            new_alts[alt] = words
        self.connections[ALT] = new_alts

        # finding all nodes and self.connections
        nodes = {}
        for conn_type in self.connections:
            print(self.connections[conn_type])
            for key_key in self.connections[conn_type]:
                if key_key in nodes:
                    nodes[key_key] = nodes[key_key] + self.connections[conn_type][key_key]
                else:
                    nodes[key_key] = self.connections[conn_type][key_key]
            # nodes = nodes | self.connections[conn_type]
        print("nodes\n", nodes)

        # finding root
        root = set(nodes).difference(*nodes.values()).pop()
        # print(root)

        # finding leaves and adding empty targets

        for node in nodes:
            for sub_node in nodes[node]:
                if sub_node not in nodes:
                    self.leaves.append(sub_node)
        for leaf in self.leaves:
            nodes[leaf] = []

        print("nodes after leaves\n",nodes)

        with open('../output.txt', 'w') as f:
            visited = set()  # Set to keep track of visited nodes.
            self.dfs(visited, nodes, root, f)
            if self.left_par != self.right_par:
                print(')', end='', file=f)
                self.right_par += 1
            print("\n", file=f)

        with open('../output.txt', 'r') as f:
            specification_string = f.read()
        return specification_string.strip()


    def dfs(self, visited, graph, node, f):
        if node not in visited:
            for connection in self.connections:
                if node in self.connections[connection]:
                    if connection != LOOP:
                        print(connection + "(", end='', file=f)
                        self.last_printed = '('
                        self.left_par += 1
                else:
                    print('', end='', file=f)
                    self.last_printed = ' '
            if node in graph[node]:
                print(LOOP+'(' + node + ')', end='', file=f)
                self.last_printed = ')'
            else:
                print(node, end='', file=f)
                self.last_printed = node
            visited.add(node)
            for neighbour in graph[node]:
                if neighbour != node:
                    print(',', end='', file=f)
                    self.last_printed = ','
                    self.dfs(visited, graph, neighbour, f)
                    if neighbour not in visited:
                        print(')', end='', file=f)
                        self.last_printed = ')'
                        self.right_par += 1
                else:
                    print(')', end='', file=f)
                    self.last_printed = ')'
                    self.right_par += 1
            # if node in visited and self.last_printed != ')':
            #    print(')', end='', file=f)
            #   self.last_printed = ')'
            #    self.right_par += 1
        else:
            if node in self.leaves:
                print(node, end='', file=f)
                self.last_printed = node
            print(')', end='', file=f)
            self.last_printed = ')'
            self.right_par += 1

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
