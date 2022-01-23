import json
from tkinter import *
from tkinter.ttk import *

from PIL import ImageTk, Image
import io

from Flowchart import Flowchart
from GeneratorFormulLogicznych.GeneratorFormulLogicznychMain import GenerateLogicalSpecification
from SpecificationStringGenerator import SpecificationStringGenerator
from State import STEPS, SELECTED_WORDS, CONNECTIONS, WORD, COND_TEXT, SEQUENCE, COND, BRANCHRE, PARA, CONCURRE, ALT, \
    LOOP, SPECIFICATION_STRING, INCLUDE, EXTEND


class FrameFlowchart(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master=master, text="Workflow Diagram", *args, **kwargs)

        self.state = state

        self.frame_add_connection = Frame(self)
        self.frame_add_connection.pack(side=TOP)

        self.sv_from = StringVar()
        # registering the observer
        self.sv_from.trace_add('write', self.check_can_add)
        self.sv_from.trace_add('write', self.set_loop_to)   # wykona się przed check_can_add
        self.cb_from = Combobox(self.frame_add_connection, width=15,
                                textvariable=self.sv_from, state="readonly")
        self.cb_from.pack(side=LEFT)
        #self.cb_from.bind('<<ComboboxSelected>>', self.check_can_add)

        self.sv_conn = StringVar()
        self.sv_conn.trace_add('write', self.check_can_add)
        self.sv_conn.trace_add('write', self.set_cond_widgets)  # wykona się przed check_can_add
        self.sv_conn.trace_add('write', self.set_loop_to)  # wykona się przed check_can_add
        self.conn_types = [SEQUENCE,
                           COND,
                           # BRANCHRE,
                           PARA,
                           # CONCURRE,
                           ALT,
                           LOOP
                           ]
        self.cb_conn_type = Combobox(self.frame_add_connection, width=15,
                                     textvariable=self.sv_conn, state="readonly",
                                     values=self.conn_types)
        self.cb_conn_type.pack(side=LEFT)
        #self.cb_conn_type.bind('<<ComboboxSelected>>', self.check_can_add)  # check_can_add(self, event):

        #  FRAME COND

        self.frame_cond = Frame(self.frame_add_connection)

        # self.sv_cond_T = StringVar()
        # self.sv_cond_T.set("True")
        # self.inp_cond_T = Entry(self.frame_cond, textvariable=self.sv_cond_T, width=6, state="readonly")
        # self.inp_cond_T.pack(side=LEFT)

        self.sv_to_cond_T = StringVar()
        self.sv_to_cond_T.trace_add('write', self.check_can_add)
        self.cb_to_cond_T = Combobox(self.frame_cond, width=18, textvariable=self.sv_to_cond_T, state="readonly")
        self.cb_to_cond_T.pack(side=LEFT)

        # self.sv_cond_F = StringVar()
        # self.sv_cond_F.set("False")
        # self.inp_cond_F = Entry(self.frame_cond, textvariable=self.sv_cond_F, width=6, state="readonly")
        # self.inp_cond_F.pack(side=LEFT)

        self.sv_to_cond_F = StringVar()
        self.sv_to_cond_F.trace_add('write', self.check_can_add)
        self.cb_to_cond_F = Combobox(self.frame_cond, width=18, textvariable=self.sv_to_cond_F, state="readonly")
        self.cb_to_cond_F.pack(side=LEFT)

        # self.sv_cond = StringVar()
        # self.sv_cond.trace_add('write', self.check_can_add)  # self.sv_cond.trace('w', self.check_can_add)
        # self.inp_cond = Entry(self.frame_add_connection, textvariable=self.sv_cond, width=10)

        #  END FRAME COND

        self.sv_to = StringVar()
        self.sv_to.trace_add('write', self.check_can_add)
        self.cb_to = Combobox(self.frame_add_connection, width=15,
                              textvariable=self.sv_to, state="readonly")
        self.cb_to.pack(side=LEFT)
        # self.cb_to.current(0)
        #self.cb_to.bind('<<ComboboxSelected>>', self.check_can_add)

        self.btn_add_conn = Button(self.frame_add_connection, text="Add", command=self.add_conn_clicked)
        self.btn_add_conn.pack(side=LEFT)

        self.reset_conn_widgets()

        self.panel = Label(self)
        self.panel.pack(side=TOP)

        self.btn_save = Button(self, text="Save", command=self.save_clicked)

        self.sv_specification_string = StringVar()
        self.lbl_specification_string = Label(self, textvariable=self.sv_specification_string)
        self.lbl_specification_string.pack(side=TOP)
        
        self.sv_logical_formulas = StringVar()
        self.lbl_logical_formulas = Label(self, textvariable=self.sv_logical_formulas)
        self.lbl_logical_formulas.pack(side=TOP)

        self.blocks = Label(self)
        self.blocks.pack(side=BOTTOM)
        self.draw_blocks()

    def reset_conn_widgets(self):
        self.sv_from.set("from activity")
        self.sv_conn.set("connection type")
        self.sv_to.set("to activity")
        self.sv_to_cond_T.set("to activity on True")
        self.sv_to_cond_F.set("to activity on False")
        if self.frame_cond.winfo_ismapped():
            self.frame_cond.pack_forget()
        # self.sv_cond.set("condition")
        # if self.inp_cond.winfo_ismapped():
        #     self.inp_cond.pack_forget()
        self.btn_add_conn.config(state=DISABLED)

    #def check_can_add(self, event): self.cb_conn_type.bind('<<ComboboxSelected>>', self.check_can_add)
    #def check_can_add(self):
    def check_can_add(self, var, indx, mode):
        #print(f"Traced variable {var} {indx} {mode}")
        sv_from = self.sv_from.get()
        sv_conn = self.sv_conn.get()
        sv_to = self.sv_to.get()
        sv_to_cond_T = self.sv_to_cond_T.get()
        sv_to_cond_F = self.sv_to_cond_F.get()
        # sv_cond = self.inp_cond.get().strip()

        if sv_from != "from activity" and sv_conn != "connection type":
            if (self.frame_cond.winfo_ismapped() and sv_to_cond_T != "to activity on True" and sv_to_cond_F != "to activity on False") or (not self.frame_cond.winfo_ismapped() and sv_to != "to activity"):
            # if not self.inp_cond.winfo_ismapped() or (self.inp_cond.winfo_ismapped() and sv_cond != "condition" and sv_cond != ""):
                self.btn_add_conn.config(state=NORMAL)
            else:
                self.btn_add_conn.config(state=DISABLED)

    def set_loop_to(self, var, indx, mode):
        if self.sv_conn.get() == LOOP:
            selected_words = [self.sv_from.get()]
            self.cb_to.config(values=selected_words)
            self.sv_to.set(self.sv_from.get())
        else:
            self.reset_cb()

    def set_cond_widgets(self, var, indx, mode):
        if self.sv_conn.get() == COND:
            if not self.frame_cond.winfo_ismapped():
                self.btn_add_conn.pack_forget()  # forget()
                self.cb_to.pack_forget()
                self.frame_cond.pack(side=LEFT)
                self.frame_cond.wait_visibility()  # żeby winfo_ismapped()self załapało
                # self.cb_to.pack(side=LEFT)
                self.btn_add_conn.pack(side=LEFT)
        else:
            if self.frame_cond.winfo_ismapped():
                self.frame_cond.pack_forget()
                self.btn_add_conn.pack_forget()
                self.cb_to.pack(side=LEFT)
                self.btn_add_conn.pack(side=LEFT)
        # if not self.inp_cond.winfo_ismapped():
        #         self.btn_add_conn.pack_forget()  # forget()
        #         self.cb_to.pack_forget()
        #         self.inp_cond.pack(side=LEFT)
        #         self.inp_cond.wait_visibility()  # żeby winfo_ismapped()self załapało
        #         self.cb_to.pack(side=LEFT)
        #         self.btn_add_conn.pack(side=LEFT)
        # else:
        #     if self.inp_cond.winfo_ismapped():
        #         self.inp_cond.pack_forget()

    def add_conn_clicked(self):
        self.update_state()
        self.reset_conn_widgets()
        self.redraw_flowchart()
        # self.show_btn_save()
        self.refresh_generated_specification()


    def update_state(self):
        sv_from = self.sv_from.get()
        sv_conn = self.sv_conn.get()
        sv_to = self.sv_to.get()
        # sv_cond = self.inp_cond.get().strip()
        sv_to_cond_T = self.sv_to_cond_T.get()
        sv_to_cond_F = self.sv_to_cond_F.get()

        if sv_conn in [COND]:
            to_list = self.state.curr_uc[CONNECTIONS][sv_conn][sv_from]
            to_list.append({WORD: sv_to_cond_T, COND_TEXT: "True"})
            to_list.append({WORD: sv_to_cond_F, COND_TEXT: "False"})
            unique_to_list = list({v[WORD]: v for v in to_list}.values())   # https://stackoverflow.com/questions/11092511/python-list-of-unique-dictionaries
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_from] = unique_to_list
        elif sv_conn in [SEQUENCE, PARA, ALT, LOOP]:
            self.state.curr_uc[CONNECTIONS][sv_conn][sv_from].add(sv_to)  # append jest do listy a mamy set
        # elif sv_conn in [BRANCHRE, CONCURRE]:
        #     self.state.curr_uc[CONNECTIONS][sv_conn][sv_to].add(sv_from)

        generated_string = self.generate_specification_string()
        self.state.curr_uc[SPECIFICATION_STRING] = generated_string

        print("after add connections", self.state.curr_uc)


    def generate_specification_string(self):
        # json_object = json.dumps(self.state.curr_uc, cls=SetEncoder, indent=4)
        # jsonFile = open("data.json", "w")
        # jsonFile.write(json_object)
        # jsonFile.close()
        #
        # self.create_specification_string()
        #
        # specification_string = ''
        # with open('output.txt', 'r') as f:
        #     specification_string = f.read()
        #
        #
        # return specification_string.strip()
        specificationStringGenerator = SpecificationStringGenerator(self.state.curr_uc[CONNECTIONS])
        return specificationStringGenerator.create_specification_string2()


    def draw_blocks(self):
        g = Flowchart()
        g.graph_attr["rankdir"] = "LR"
        g.edge_attr["style"] = "invis"
        # g.graph_attr["splines"] = "ortho"
        # g.graph_attr["rotate"] = "90"
        # g.graph_attr["ratio"] = "0.5"
        g.add_conn_first_node(SEQUENCE, SEQUENCE)
        g.add_conn_first_node(COND, COND)
        # g.add_conn_first_node(BRANCHRE, BRANCHRE)
        g.add_conn_first_node(PARA, PARA)
        # g.add_conn_first_node(CONCURRE, CONCURRE)
        g.add_conn_first_node(ALT, ALT)
        g.add_conn_first_node(LOOP, LOOP)
        g.add_edge(SEQUENCE, COND)
        # g.add_edge(COND, BRANCHRE)
        g.add_edge(COND, PARA)
        # g.add_edge(BRANCHRE, PARA)
        # g.add_edge(PARA, CONCURRE)
        g.add_edge(PARA, ALT)
        g.add_edge(ALT, LOOP)
        g.layout(prog='dot')
        byte_arr = g.draw(path=None, format='png')
        image = ImageTk.PhotoImage(image=Image.open(io.BytesIO(byte_arr)))
        self.blocks.configure(image=image)
        self.blocks.image = image

    def redraw_flowchart(self):
        g = Flowchart()

        self.add_nodes(g)
        self.add_edges(g)
        g.add_start_nodes()
        g.add_end_nodes()

        # g.layout()  # engine='dot'
        g.layout(prog='dot')  # ładnie z góry na dół
        # https://stackoverflow.com/a/18610140/12615981 draw without saving
        g.draw("file2.png")

        img = ImageTk.PhotoImage(image=Image.open("file2.png"))

        self.panel.configure(image=img)
        self.panel.image = img

    def add_nodes(self, g):  # TODO co jeśli jeden node jest np. zarówno rebranch i concur??
        for conn_type, value_dict in self.state.curr_uc[CONNECTIONS].items():  #key, value
            if self.state.curr_uc[CONNECTIONS][conn_type]:  # if not empty
                if conn_type in [SEQUENCE, COND, PARA, ALT, LOOP]:  # BRANCHRE, CONCURRE,
                    for from_ in self.state.curr_uc[CONNECTIONS][conn_type]:
                        g.add_conn_first_node(conn_type, from_)

    def add_edges(self, g):
        for conn_type, value_dict in self.state.curr_uc[CONNECTIONS].items():  #key, value
            if self.state.curr_uc[CONNECTIONS][conn_type]:  # if not empty
                if conn_type in [COND]:
                    for from_, to_list in self.state.curr_uc[CONNECTIONS][conn_type].items():
                        for to in to_list:
                            g.add_edge(from_, to[WORD], label=to[COND_TEXT])
                elif conn_type in [SEQUENCE, PARA, ALT, LOOP]:
                    for from_, to_list in self.state.curr_uc[CONNECTIONS][conn_type].items():
                        for to in to_list:
                            g.add_edge(from_, to)

                # elif conn_type in [BRANCHRE, CONCURRE]:
                #     for to, from_list in self.state.curr_uc[CONNECTIONS][conn_type].items():
                #         for from_ in from_list:
                #             g.add_edge(from_, to)

    def refresh(self):
        self.reset_cb()
        self.reset_conn_widgets()
        self.refresh_generated_specification()
        if self.state.curr_uc_connections_exist():
            self.redraw_flowchart()
            # self.show_btn_save()
        else:
            self.panel.configure(image="")
            self.hide_btn_save()

    def refresh_generated_specification(self):
        cur_specification_string = self.state.curr_uc[SPECIFICATION_STRING]
        self.sv_specification_string.set(cur_specification_string)
        self.sv_logical_formulas.set('')
        if cur_specification_string != '':
            try:
                formulas = GenerateLogicalSpecification(cur_specification_string)
                self.sv_logical_formulas.set(formulas)
            except:
                self.sv_logical_formulas.set("Logical formulas generation error!")

    def reset_cb(self):
        # if STEPS not in self.state.curr_uc:
        #     return
        # selected_words = [step[SELECTED_WORDS][0] for step in self.state.curr_uc[STEPS] if step[SELECTED_WORDS]]  #if step[SELECTED_WORDS] != []
        selected_words = []
        if STEPS in self.state.curr_uc:
            for step in self.state.curr_uc[STEPS]:
                selected_words.extend(step[SELECTED_WORDS])
            selected_words.extend(self.state.curr_uc[INCLUDE])
            selected_words.extend(self.state.curr_uc[EXTEND])
        self.cb_from.config(values=selected_words)
        self.cb_to.config(values=selected_words)
        self.cb_to_cond_T.config(values=selected_words)
        self.cb_to_cond_F.config(values=selected_words)

    def show_btn_save(self):
        if not self.btn_save.winfo_ismapped():
            self.btn_save.pack(side=BOTTOM, fill=X)

    def hide_btn_save(self):
        if self.btn_save.winfo_ismapped():
            self.btn_save.pack_forget()

    def save_clicked(self):
        pass

