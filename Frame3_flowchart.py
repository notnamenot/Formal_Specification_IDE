from tkinter import *
from tkinter.ttk import *

from State import STEPS, SELECTED_WORDS, CONNECTIONS, SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE


class FrameFlowchart(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master=master, text="Workflow Diagram", *args, **kwargs)

        self.state = state
        self.steps = state.curr_uc[STEPS]
        self.selected_words = [step[SELECTED_WORDS][0] for step in self.steps]
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

        # Adding combobox drop down list
        # connectionchoosen['values'] = (' Sequence',
        #                                ' Branch',
        #                                ' BranchRe',
        #                                ' Concur',
        #                                ' ConcurRe'
        #                                )

        self.sv_to = StringVar()
        self.sv_to.trace_add('write', self.check_can_add)
        self.cb_to = Combobox(self.frame_add_connection, width=20,
                              textvariable=self.sv_to, state="readonly",
                              values=self.selected_words)
        self.cb_to.pack(side=LEFT)
        # self.cb_to.current(0)
        #self.cb_to.bind('<<ComboboxSelected>>', self.check_can_add)

        self.reset_add_conn_frame()

        self.btn_add_conn = Button(self.frame_add_connection, text="Add", command=self.add_conn_clicked, state=DISABLED)
        self.btn_add_conn.pack(side=LEFT)

    def reset_add_conn_frame(self):
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

        print(sv_from, sv_to, sv_conn)
        if sv_from != "from activity" and sv_to != "to activity" and sv_conn != "connection type":
            self.btn_add_conn.config(state=NORMAL)

    def add_conn_clicked(self):

        sv_from = self.sv_from.get()
        sv_conn = self.sv_conn.get()
        sv_to = self.sv_to.get()

        if sv_conn in [SEQUENCE, BRANCH, CONCUR]:
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_from].append(sv_to)
        elif sv_conn in [BRANCHRE, CONCURRE]:
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_to].append(sv_from)

        self.reset_add_conn_frame()
        self.btn_add_conn.config(state=DISABLED)

        print(self.state.curr_uc)
        #TODO reprint flowchart i save conn


    def create_connections_types_widgets(self):
        self.lbl_start = Label(self, text="Start", bg="#eddeb4", padx=8, pady=8, width=8)
        self.lbl_start.pack(side=LEFT, anchor=NW)

        self.lbl_seq = Label(self, text="Sequence", bg="#8aaceb", padx=8, pady=8, width=8)
        self.lbl_seq.pack(side=LEFT, anchor=NW)

        self.lbl_branch = Label(self, text="Branch", bg="#6df776", padx=8, pady=8, width=8)
        self.lbl_branch.pack(side=LEFT, anchor=NW)

        self.lbl_branch_re = Label(self, text="BranchRe", bg="#5acc61", padx=8, pady=8, width=8)
        self.lbl_branch_re.pack(side=LEFT, anchor=NW)

        self.lbl_concur = Label(self, text="Concur", bg="#eb9f73", padx=8, pady=8, width=8)
        self.lbl_concur.pack(side=LEFT, anchor=NW)

        self.lbl_concur_re = Label(self, text="ConcurRe", bg="#cc845a", padx=8, pady=8, width=8)
        self.lbl_concur_re.pack(side=LEFT, anchor=NW)

        self.lbl_end = Label(self, text="End", bg="#eddeb4", padx=8, pady=8, width=8)
        self.lbl_end.pack(side=LEFT, anchor=NW)


