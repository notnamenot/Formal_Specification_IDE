import pygraphviz as pgv

from State import  SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE


class Flowchart(pgv.AGraph):
    def __init__(self, *args):
        super().__init__(strict=False, directed=True, *args)

        self.graph_attr["rankdir"] = "TB"
        self.graph_attr["ranksep"] = "0.2"

        self.node_attr["shape"] = "box"
        self.node_attr["style"] = "filled,rounded"
        self.node_attr["fillcolor"] = "#74b1ed"
        self.node_attr["color"] = "#3d6fa1"

    def add_conn_first_node(self, type, label):
        if type == SEQUENCE:
            self.add_sequence_node(label)
        elif type == BRANCH:
            self.add_branch_node(label)
        elif type == BRANCHRE:
            self.add_branchre_node(label)
        elif type == CONCUR:
            self.add_concur_node(label)
        elif type == CONCURRE:
            self.add_concurre_node(label)

    def add_sequence_node(self, label):
        super().add_node(label, shape='box', label=label, color="#245c8a", fillcolor="#3485c7")

    def add_branch_node(self, label):
        # super(Flowchart,self)
        # pgv.AGraph
        super().add_node(label, shape='diamond', label=label, color="#227a22", fillcolor="#3acf3a")

    def add_branchre_node(self, label):
        super().add_node(label, shape='box', label=label, color="#0b3b0b", fillcolor="#156b15")

    def add_concur_node(self, label):
        super().add_node(label, shape='box', label=label, color="#db6f3d", fillcolor="#ff8045")

    def add_concurre_node(self, label):
        super().add_node(label, shape='box', label=label, color="#703012", fillcolor="#9e4419")

    def add_end_nodes(self):

        end_nodes = [node for node, out_degree in self.out_degree(self.nodes(), with_labels=True).items() if out_degree == 0]
        for i, node in enumerate(end_nodes):
            s = f"end{i}"
            super().add_node(s, label="end", shape='ellipse', color="#747575", fillcolor="#989a9c")
            self.add_edge(node, s)

    def add_start_nodes(self):
        start_nodes = [node for node, in_degree in self.in_degree(self.nodes(), with_labels=True).items() if in_degree == 0]
        for i, node in enumerate(start_nodes):
            s = f"start{i}"
            super().add_node(s, label="start", shape='ellipse', color="#747575", fillcolor="#989a9c")
            self.add_edge(s, node)

