import pygraphviz as pgv

from State import SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE

COLOR_SEQUENCE_BORDER = "#245c8a"
COLOR_SEQUENCE_FILL = "#3485c7"
COLOR_BRANCH_BORDER = "#227a22"
COLOR_BRANCH_FILL = "#3acf3a"
COLOR_BRANCHRE_BORDER = "#0b3b0b"
COLOR_BRANCHRE_FILL = "#156b15"
COLOR_CONCUR_BORDER = "#db6f3d"
COLOR_CONCUR_FILL = "#ff8045"
COLOR_CONCURRE_BORDER = "#703012"
COLOR_CONCURRE_FILL = "#9e4419"
COLOR_START_STOP_BORDER = "#747575"
COLOR_START_STOP_FILL = "#989a9c"
COLOR_PLAIN_NODE_BORDER = "#3d6fa1"
COLOR_PLAIN_NODE_FILL = "#74b1ed"

class Flowchart(pgv.AGraph):
    def __init__(self, *args):
        super().__init__(strict=False, directed=True, *args)

        self.graph_attr["rankdir"] = "TB"
        self.graph_attr["ranksep"] = "0.2"
        # self.graph_attr["splines"] = "ortho"
        # self.graph_attr["splines"] = "True"
        self.graph_attr["bgcolor"] = "transparent"

        self.node_attr["shape"] = "box"
        self.node_attr["style"] = "filled,rounded"
        self.node_attr["fillcolor"] = COLOR_PLAIN_NODE_FILL
        self.node_attr["color"] = COLOR_PLAIN_NODE_BORDER

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
        super().add_node(label, shape='box', label=label, color=COLOR_SEQUENCE_BORDER, fillcolor=COLOR_SEQUENCE_FILL)

    def add_branch_node(self, label):
        super().add_node(label, shape='diamond', label=label, color=COLOR_BRANCH_BORDER, fillcolor=COLOR_BRANCH_FILL)

    def add_branchre_node(self, label):
        super().add_node(label, shape='box', label=label, color=COLOR_BRANCHRE_BORDER, fillcolor=COLOR_BRANCHRE_FILL)

    def add_concur_node(self, label):
        super().add_node(label, shape='box', label=label, color=COLOR_CONCUR_BORDER, fillcolor=COLOR_CONCUR_FILL)

    def add_concurre_node(self, label):
        super().add_node(label, shape='box', label=label, color=COLOR_CONCURRE_BORDER, fillcolor=COLOR_CONCURRE_FILL)

    def add_end_nodes(self):
        end_nodes = [node for node, out_degree in self.out_degree(self.nodes(), with_labels=True).items() if out_degree == 0]
        for i, node in enumerate(end_nodes):
            s = f"end{i}"
            super().add_node(s, label="end", shape='ellipse', color=COLOR_START_STOP_BORDER, fillcolor=COLOR_START_STOP_FILL)
            self.add_edge(node, s)

    def add_start_nodes(self):
        start_nodes = [node for node, in_degree in self.in_degree(self.nodes(), with_labels=True).items() if in_degree == 0]
        for i, node in enumerate(start_nodes):
            s = f"start{i}"
            super().add_node(s, label="start", shape='ellipse', color=COLOR_START_STOP_BORDER, fillcolor=COLOR_START_STOP_FILL)
            self.add_edge(s, node)

