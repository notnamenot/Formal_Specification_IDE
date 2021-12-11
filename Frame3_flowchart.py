from tkinter import *
from tkinter.ttk import *
# import pydot
import pygraphviz as pgv
# import graphviz

from PIL import ImageTk, Image

from Flowchart import Flowchart
from State import STEPS, SELECTED_WORDS, CONNECTIONS, SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE


class FrameFlowchart(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master=master, text="Workflow Diagram", *args, **kwargs)

        self.state = state
        self.selected_words = [step[SELECTED_WORDS][0] for step in state.curr_uc[STEPS]]
        print("selected_words", self.selected_words)

        self.frame_add_connection = Frame(self)
        self.frame_add_connection.pack(side=TOP)

        self.sv_from = StringVar()
        # registering the observer
        self.sv_from.trace_add('write', self.check_can_add)
        self.cb_from = Combobox(self.frame_add_connection, width=20,
                                textvariable=self.sv_from, state="readonly",
                                values=self.selected_words)
        self.cb_from.pack(side=LEFT)
        #self.cb_from.bind('<<ComboboxSelected>>', self.check_can_add)


        self.sv_conn = StringVar()
        # registering the observer
        self.sv_conn.trace_add('write', self.check_can_add) # TODO if Branch add selection of cond
        #self.conn_types = ['Sequence', 'Branch', 'BranchRe', 'Concur', 'ConcurRe']
        self.conn_types = [SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE]
        self.cb_conn_type = Combobox(self.frame_add_connection, width=20,
                                     textvariable=self.sv_conn, state="readonly",
                                     values=self.conn_types)
        self.cb_conn_type.pack(side=LEFT)
        #self.cb_conn_type.bind('<<ComboboxSelected>>', self.check_can_add)  # check_can_add(self, event):

        self.sv_to = StringVar()
        self.sv_to.trace_add('write', self.check_can_add)
        self.cb_to = Combobox(self.frame_add_connection, width=20,
                              textvariable=self.sv_to, state="readonly",
                              values=self.selected_words)
        self.cb_to.pack(side=LEFT)
        # self.cb_to.current(0)
        #self.cb_to.bind('<<ComboboxSelected>>', self.check_can_add)

        self.reset_comboboxes()

        self.btn_add_conn = Button(self.frame_add_connection, text="Add", command=self.add_conn_clicked, state=DISABLED)
        self.btn_add_conn.pack(side=LEFT)

        self.panel = Label(self)
        self.panel.pack(side=TOP)

    def reset_comboboxes(self):
        self.sv_from.set("from activity")
        self.sv_conn.set("connection type")
        self.sv_to.set("to activity")

    #def check_can_add(self, event): self.cb_conn_type.bind('<<ComboboxSelected>>', self.check_can_add)
    #def check_can_add(self):
    def check_can_add(self, var, indx, mode):
        #print(f"Traced variable {var} {indx} {mode}")
        sv_from = self.sv_from.get()
        sv_conn = self.sv_conn.get()
        sv_to = self.sv_to.get()

        #print(sv_from, sv_to, sv_conn)
        if sv_from != "from activity" and sv_to != "to activity" and sv_conn != "connection type":
            self.btn_add_conn.config(state=NORMAL)

    def add_conn_clicked(self):
        sv_from = self.sv_from.get()
        sv_conn = self.sv_conn.get()
        sv_to = self.sv_to.get()

        if sv_conn in [SEQUENCE, BRANCH, CONCUR]:
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_from].add(sv_to)  # append jest do listy a mamy set
        elif sv_conn in [BRANCHRE, CONCURRE]:
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_to].add(sv_from)

        self.reset_comboboxes()
        self.btn_add_conn.config(state=DISABLED)

        print(self.state.curr_uc)

        self.redraw_flowchart()

    def redraw_flowchart(self):
        g = Flowchart()

        self.add_nodes(g)
        self.add_edges(g)
        g.add_start_nodes()
        g.add_end_nodes()

        g.layout()  # engine='dot'
        g.draw("file2.png")

        img = ImageTk.PhotoImage(image=Image.open("file2.png"))

        self.panel.configure(image=img)
        self.panel.image = img

    def add_nodes(self, g):
        for conn_type, value_dict in self.state.curr_uc[CONNECTIONS].items():  #key, value
            if self.state.curr_uc[CONNECTIONS][conn_type]:  # if not empty
                if conn_type in [SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE]:
                    for from_ in self.state.curr_uc[CONNECTIONS][conn_type]:
                        # g.node(from_, shape='box')
                        g.add_conn_first_node(conn_type, from_)

    def add_edges(self, g):
        for conn_type, value_dict in self.state.curr_uc[CONNECTIONS].items():  #key, value
            if self.state.curr_uc[CONNECTIONS][conn_type]:  # if not empty
                if conn_type in [SEQUENCE, BRANCH, CONCUR]:
                    for from_, to_list in self.state.curr_uc[CONNECTIONS][conn_type].items():
                        for to in to_list:
                            g.add_edge(from_, to)
                elif conn_type in [BRANCHRE, CONCURRE]:
                    for to, from_list in self.state.curr_uc[CONNECTIONS][conn_type].items():
                        for from_ in from_list:
                            g.add_edge(from_, to)

    def refresh(self):
        self.reset_comboboxes()
        self.redraw_flowchart()

