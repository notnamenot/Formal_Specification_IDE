from tkinter import *
from tkinter.ttk import *

from PIL import ImageTk, Image

from Flowchart import Flowchart
from State import STEPS, SELECTED_WORDS, CONNECTIONS, WORD, COND, SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE


class FrameFlowchart(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master=master, text="Workflow Diagram", *args, **kwargs)

        self.state = state
        selected_words = [step[SELECTED_WORDS][0] for step in self.state.curr_uc[STEPS]]

        self.frame_add_connection = Frame(self)
        self.frame_add_connection.pack(side=TOP)

        self.sv_from = StringVar()
        # registering the observer
        self.sv_from.trace_add('write', self.check_can_add)
        self.cb_from = Combobox(self.frame_add_connection, width=20,
                                textvariable=self.sv_from, state="readonly",
                                values=selected_words)
        self.cb_from.pack(side=LEFT)
        #self.cb_from.bind('<<ComboboxSelected>>', self.check_can_add)

        self.sv_conn = StringVar()
        self.sv_conn.trace_add('write', self.check_can_add)
        self.sv_conn.trace_add('write', self.check_branch_cond)  # pierwsze?
        self.conn_types = [SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE]
        self.cb_conn_type = Combobox(self.frame_add_connection, width=20,
                                     textvariable=self.sv_conn, state="readonly",
                                     values=self.conn_types)
        self.cb_conn_type.pack(side=LEFT)
        #self.cb_conn_type.bind('<<ComboboxSelected>>', self.check_can_add)  # check_can_add(self, event):

        self.sv_cond = StringVar()
        self.sv_cond.trace_add('write', self.check_can_add)  # self.sv_cond.trace('w', self.check_can_add)
        self.inp_cond = Entry(self.frame_add_connection, textvariable=self.sv_cond, width=10)

        self.sv_to = StringVar()
        self.sv_to.trace_add('write', self.check_can_add)
        self.cb_to = Combobox(self.frame_add_connection, width=20,
                              textvariable=self.sv_to, state="readonly",
                              values=selected_words)
        self.cb_to.pack(side=LEFT)
        # self.cb_to.current(0)
        #self.cb_to.bind('<<ComboboxSelected>>', self.check_can_add)

        self.btn_add_conn = Button(self.frame_add_connection, text="Add", command=self.add_conn_clicked)
        self.btn_add_conn.pack(side=LEFT)

        self.reset_conn_widgets()

        self.panel = Label(self)
        self.panel.pack(side=TOP)

    def reset_conn_widgets(self):
        self.sv_from.set("from activity")
        self.sv_conn.set("connection type")
        self.sv_to.set("to activity")
        self.sv_cond.set("condition")
        if self.inp_cond.winfo_ismapped():
            self.inp_cond.pack_forget()
        self.btn_add_conn.config(state=DISABLED)

    #def check_can_add(self, event): self.cb_conn_type.bind('<<ComboboxSelected>>', self.check_can_add)
    #def check_can_add(self):
    def check_can_add(self, var, indx, mode):
        #print(f"Traced variable {var} {indx} {mode}")
        sv_from = self.sv_from.get()
        sv_conn = self.sv_conn.get()
        sv_to = self.sv_to.get()
        sv_cond = self.inp_cond.get()

        if sv_from != "from activity" and sv_to != "to activity" and sv_conn != "connection type":
            if not self.inp_cond.winfo_ismapped() or (self.inp_cond.winfo_ismapped() and sv_cond != "condition" and sv_cond != ""):
                self.btn_add_conn.config(state=NORMAL)
            else:
                self.btn_add_conn.config(state=DISABLED)

    def check_branch_cond(self, var, indx, mode):
        if self.sv_conn.get() == BRANCH:
            if not self.inp_cond.winfo_ismapped():
                self.btn_add_conn.pack_forget()  # forget()
                self.cb_to.pack_forget()
                self.inp_cond.pack(side=LEFT)
                self.inp_cond.wait_visibility()  # żeby winfo_ismapped()self załapało
                self.cb_to.pack(side=LEFT)
                self.btn_add_conn.pack(side=LEFT)
        else:
            if self.inp_cond.winfo_ismapped():
                self.inp_cond.pack_forget()

    def add_conn_clicked(self):
        sv_from = self.sv_from.get()
        sv_conn = self.sv_conn.get()
        sv_to = self.sv_to.get()
        sv_cond = self.inp_cond.get()

        if sv_conn in [BRANCH]:
            to_list = self.state.curr_uc[CONNECTIONS][sv_conn][sv_from]
            to_list.append({WORD: sv_to, COND: sv_cond})
            unique_to_list = list({v[WORD]: v for v in to_list}.values())   # https://stackoverflow.com/questions/11092511/python-list-of-unique-dictionaries
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_from] = unique_to_list
        elif sv_conn in [SEQUENCE, CONCUR]:
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_from].add(sv_to)  # append jest do listy a mamy set
        elif sv_conn in [BRANCHRE, CONCURRE]:
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_to].add(sv_from)

        print("after add connections", self.state.curr_uc)

        self.reset_conn_widgets()

        self.redraw_flowchart()

    def redraw_flowchart(self):
        if not self.state.curr_uc_connections_exist():   # curr_uc nie ma jeszcze connections, ale inne uc mogą już mieć
            self.panel.configure(image="")
            return

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

    def add_nodes(self, g):  # TODO co jeśli jeden node jest np. zarówno rebranch i concur??
        for conn_type, value_dict in self.state.curr_uc[CONNECTIONS].items():  #key, value
            if self.state.curr_uc[CONNECTIONS][conn_type]:  # if not empty
                if conn_type in [SEQUENCE, BRANCH, BRANCHRE, CONCUR, CONCURRE]:
                    for from_ in self.state.curr_uc[CONNECTIONS][conn_type]:
                        g.add_conn_first_node(conn_type, from_)

    def add_edges(self, g):
        for conn_type, value_dict in self.state.curr_uc[CONNECTIONS].items():  #key, value
            if self.state.curr_uc[CONNECTIONS][conn_type]:  # if not empty
                if conn_type in [BRANCH]:
                    for from_, to_list in self.state.curr_uc[CONNECTIONS][conn_type].items():
                        for to in to_list:
                            g.add_edge(from_, to[WORD], label=to[COND])
                if conn_type in [SEQUENCE, CONCUR]:
                    for from_, to_list in self.state.curr_uc[CONNECTIONS][conn_type].items():
                        for to in to_list:
                            g.add_edge(from_, to)
                elif conn_type in [BRANCHRE, CONCURRE]:
                    for to, from_list in self.state.curr_uc[CONNECTIONS][conn_type].items():
                        for from_ in from_list:
                            g.add_edge(from_, to)

    def refresh(self):
        selected_words = [step[SELECTED_WORDS][0] for step in self.state.curr_uc[STEPS]]  #if step[SELECTED_WORDS] != []
        self.cb_from.config(values=selected_words)
        self.cb_to.config(values=selected_words)
        self.reset_conn_widgets()
        self.redraw_flowchart()

