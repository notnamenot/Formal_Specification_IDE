import json
from io import StringIO
from treelib import Node, Tree
from State import STEPS, SELECTED_WORDS, CONNECTIONS, WORD, COND_TEXT, SEQUENCE, COND, BRANCHRE, PARA, CONCURRE, ALT, \
    LOOP, SPECIFICATION_STRING

class SpecificationStringGenerator:
    def __init__(self, connections):

        io = StringIO(json.dumps(connections, cls=SetEncoder, indent=4))
        self.connections = json.load(io)

        self.leaves = []

        #flag to expression
        self.last_printed = ''
        self.left_par = 0
        self.right_par = 0

        # self.try_treelib()

    def create_specification_string2(self):

        # simplify Cond
        new_conds = {}
        for cond in self.connections[COND]:
            list = []
            for e in self.connections[COND][cond]:
                list.append(e[WORD])
            new_conds[cond] = list
        self.connections[COND] = new_conds

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

        with open('output.txt', 'w') as f:
            visited = set()  # Set to keep track of visited nodes.
            self.dfs(visited, nodes, root, f)
            if self.left_par != self.right_par:
                print(')', end='', file=f)
                self.right_par += 1
            print("\n", file=f)

        with open('output.txt', 'r') as f:
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


    # def create_specification_string(self):
    #
    #     data = json.load(open("data.json", "r"))
    #     self.connections = data['self.connections']
    #
    #     # simplify Cond
    #     new_conds = {}
    #     for cond in self.connections['Cond']:
    #         list = []
    #         for e in self.connections['Cond'][cond]:
    #             list.append(e['word'])
    #         new_conds[cond] = list
    #     self.connections['Cond'] = new_conds
    #
    #     # finding all nodes and self.connections
    #     nodes = {}
    #     for key in self.connections:
    #         print(self.connections[key])
    #         for key_key in self.connections[key]:
    #             if key_key in nodes:
    #                 nodes[key_key] = nodes[key_key] + self.connections[key][key_key]
    #             else:
    #                 nodes[key_key] = self.connections[key][key_key]
    #         # nodes = nodes | self.connections[key]
    #     print(nodes)
    #
    #     # finding root
    #     root = set(nodes).difference(*nodes.values()).pop()
    #     # print(root)
    #
    #     # finding leaves and adding empty targets
    #     leafs = []
    #     for node in nodes:
    #         for sub_node in nodes[node]:
    #             if sub_node not in nodes:
    #                 leafs.append(sub_node)
    #     for leaf in leafs:
    #         nodes[leaf] = []
    #
    #     # print(nodes)
    #
    #     def dfs(visited, graph, node, f):
    #         if node not in visited:
    #             for connection in self.connections:
    #                 if node in self.connections[connection]:
    #                     if connection != 'Loop':
    #                         print(connection + "(", end='', file=f)
    #                         self.last_printed = '('
    #                         self.left_par += 1
    #                 else:
    #                     print('', end='', file=f)
    #                     self.last_printed = ' '
    #             if node in graph[node]:
    #                 print('Loop(' + node + ')', end='', file=f)
    #                 self.last_printed = ')'
    #             else:
    #                 print(node, end='', file=f)
    #                 self.last_printed = node
    #             visited.add(node)
    #             for neighbour in graph[node]:
    #                 if neighbour != node:
    #                     print(',', end='', file=f)
    #                     self.last_printed = ','
    #                     dfs(visited, graph, neighbour, f)
    #                     if neighbour not in visited:
    #                         print(')', end='', file=f)
    #                         self.last_printed = ')'
    #                         self.right_par += 1
    #                 else:
    #                     print(')', end='', file=f)
    #                     self.last_printed = ')'
    #                     self.right_par += 1
    #             # if node in visited and self.last_printed != ')':
    #             #    print(')', end='', file=f)
    #             #   self.last_printed = ')'
    #             #    self.right_par += 1
    #         else:
    #             if node in leafs:
    #                 print(node, end='', file=f)
    #                 self.last_printed = node
    #             print(')', end='', file=f)
    #             self.last_printed = ')'
    #             self.right_par += 1
    #
    #     with open('output.txt', 'w') as f:
    #         visited = set()  # Set to keep track of visited nodes.
    #         dfs(visited, nodes, root, f)
    #         if self.left_par != self.right_par:
    #             print(')', end='', file=f)
    #             self.right_par += 1
    #         print("\n", file=f)




    # def try_treelib(self):
    #
    #     # simplify Cond
    #     new_conds = {}
    #     for cond in self.connections['Cond']:
    #         list = []
    #         for e in self.connections['Cond'][cond]:
    #             list.append(e['word'])
    #         new_conds[cond] = list
    #     self.connections['Cond'] = new_conds
    #
    #     # finding all nodes and self.connections
    #     nodes = {}
    #     for conn_type in self.connections:
    #         print(self.connections[conn_type])
    #         for key_key in self.connections[conn_type]:
    #             if key_key in nodes:
    #                 nodes[key_key] = nodes[key_key] + self.connections[conn_type][key_key]
    #             else:
    #                 nodes[key_key] = self.connections[conn_type][key_key]
    #         # nodes = nodes | self.connections[conn_type]
    #     print("nodes\n",nodes)
    #
    #     # finding root
    #     root = set(nodes).difference(*nodes.values()).pop()
    #     # print(root)
    #
    #     # finding leaves and adding empty targets
    #
    #     for node in nodes:
    #         for sub_node in nodes[node]:
    #             if sub_node not in nodes:
    #                 self.leaves.append(sub_node)
    #     for leaf in self.leaves:
    #         nodes[leaf] = []
    #
    #     print("node",nodes)
    #     tree = Tree()
    #     for from_, tos in nodes.items():
    #         if not tree.contains(from_):
    #             tree.create_node(from_, from_)
    #         for to in tos:
    #             if (not tree.contains(to)): #(to != from_) and
    #                 tree.create_node(to, to, from_)
    #             elif (to != from_):
    #                 n = tree.get_node(to)
    #                 n.update_bpointer(from_) # set parent, do niczego to, bo node może mieć więcej rodziców
    #

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
