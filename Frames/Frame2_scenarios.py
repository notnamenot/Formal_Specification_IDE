import re
from tkinter import *
from tkinter.messagebox import showinfo

from Helpers.State import USE_CASES, NAME, ID, STEPS, TEXT, SELECTED_WORDS, EXTEND, INCLUDE


class FrameScenarios(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master=master, text="Scenarios", *args, **kwargs)

        self.state = state

        self.scenarios_frames = []

        self.btn_ready = Button(self, text="Ready!", width=50, state=DISABLED, command=self.ready_clicked)
        self.btn_ready.pack(side=BOTTOM)

        # self.frame_input_scenario = Frame(self)
        # self.frame_input_scenario.pack(side=BOTTOM)
        #
        # # input_scenario_id = Entry(frame_input_scenario, width=3, borderwidth=3)
        # # input_scenario_id.grid(row=0, column=0)
        # # input_scenario_id.insert(0, "UC")
        #
        # self.input_scenario_name = Entry(self.frame_input_scenario, width=50, borderwidth=3)
        # self.input_scenario_name.grid(row=0, column=0)
        # self.input_scenario_name.insert(0, "Enter scenario...")
        #
        # self.btn_add_scenario = Button(self.frame_input_scenario, text="Add", command=self.add_scenario_clicked)
        # self.btn_add_scenario.grid(row=0, column=1)

    def ready_clicked(self):
        err_msg = self.validate_state()
        if err_msg:
            showinfo(title='Error', message=err_msg)
            return

        self.master.add_frame3_flowchart()

    def validate_state(self):  # should be in State class??
        for uc in self.state.curr_uc_diagram[USE_CASES]:
            if not uc["steps"]:
                return "Fill in all scenarios!"

            for step in uc["steps"]:
                if not step["selected_words"]:
                    return "Choose activity in each step!"

            for uc_to_extend in uc[EXTEND]:
                for step in uc[STEPS]:
                    #  re.fullmatch(pattern, string, flags=0)¶
                    if re.fullmatch(rf"<<extend>> if \w+ then {uc_to_extend}", step[TEXT]):
                        break
                else:
                    return f"Extend {uc_to_extend} from {uc[NAME]} not provided!\nUse valid step pattern:\n<<extend>> if <cond> then {uc_to_extend}"

            for uc_to_include in uc[INCLUDE]:
                for step in uc[STEPS]:
                    #  re.fullmatch(pattern, string, flags=0)¶
                    if re.fullmatch(rf"<<include>> {uc_to_include}", step[TEXT]):
                        break
                else:
                    return f"Include {uc_to_include} from {uc[NAME]} not provided!\nUse valid step pattern:\n<<include>> {uc_to_include}"

        return ""

    # def add_scenario_clicked(self):
    #     scenario = self.input_scenario_name.get().strip()
    #     # id = input_scenario_id.get().strip()
    #
    #     if not scenario or not self.state.curr_uc_diagram:  # if empty input or diagram not chosen TODO pokazać frame scenarios dopiero po imporcie plików
    #         return
    #
    #     self.input_scenario_name.delete(0, END)
    #     self.input_scenario_name.insert(0, "Enter scenario...")
    #     # input_scenario_id.delete(0, END)
    #
    #     self.add_scenario_frame(scenario, <powinno być kolejne id>)
    #     self.state.add_use_cases([scenario])


    def add_scenario_frame(self, name, id):
        frame_scenario = Scenario(self, name, id)
        frame_scenario.pack(fill=X, pady=(0, 10), padx=5)
        self.scenarios_frames.append(frame_scenario)
        return frame_scenario

    def refresh(self):
        # print("from refresh\nall\n", self.state.all_uc_diagrams, "\ncurr diag\n", self.state.curr_uc_diagram, "\ncurr uc\n", self.state.curr_uc)
        # 1. remove old scenarios
        for scenario in reversed(self.scenarios_frames):
            scenario.destroy()
            self.scenarios_frames.pop()

        # 2. add new scenarios
        if self.state.curr_uc_diagram:
            for use_case in self.state.curr_uc_diagram[USE_CASES]:
                frame_scenario = self.add_scenario_frame(use_case[NAME], use_case[ID])
                for step in use_case[STEPS]:
                    frame_scenario.add_step_frame(step[TEXT], step[SELECTED_WORDS])

        # 3. set curr scenario and focus on first scenario
        if self.scenarios_frames:
            self.btn_ready.configure(state=NORMAL)
            self.scenarios_frames[0].scenario_clicked(Event)
        else:
            self.btn_ready.configure(state=DISABLED)


class Scenario(LabelFrame):
    def __init__(self, master, name, id,  *args, **kwargs):
        super().__init__(master=master, relief="flat", highlightthickness=1, *args, **kwargs)
        self.id = id
        self.name = name

        self.step_frames = []  # pamiętać przy usuwaniu stepa żeby stąd też czyścić

        self.frame_id_name = LabelFrame(self, relief="flat")  # relief="ridge"
        self.frame_id_name.pack(fill=X)
        self.frame_id_name.rowconfigure(1, weight=1)
        self.frame_id_name.columnconfigure(1, weight=1)

        self.lbl_scenario_id = Label(self.frame_id_name, text=self.id + "  ", font=("Arial", 12))
        # self.lbl_scenario_id.grid(row=0, column=0, sticky=N + S)
        self.lbl_scenario_name = Label(self.frame_id_name, text=self.name, font=("Arial", 12))
        self.lbl_scenario_name.grid(row=0, column=1, sticky=N+S)

        self.btn_add_step = Button(self, text="Add", command=self.add_step_clicked)
        self.btn_add_step.pack(side=BOTTOM, fill=X)

        self.frame_enter_step = Frame(self)
        self.frame_enter_step.pack(side=BOTTOM, fill=X)

        self.lbl_next_step_id = Label(self.frame_enter_step, text="1.")
        self.lbl_next_step_id.pack(side=LEFT)

        self.inp_step = Entry(self.frame_enter_step)
        # self.inp_step.insert(0, f'{self.number_of_steps+1}.')  # f'{len(self.step_frames)+1}.'
        # self.inp_step.insert(0, 'Enter step..')  # f'{len(self.step_frames)+1}.'
        self.inp_step.pack(side=LEFT, fill=X, expand=True)
        self.inp_step.bind('<Return>', self.on_enter_clicked)

        self.bind_LMB_click(self)

    def bind_LMB_click(self, widget):   # Binds an event to a widget and all its descendants
        widget.bind('<Button-1>', lambda e: self.scenario_clicked(e))
        for child in widget.children.values():
            self.bind_LMB_click(child)

    def scenario_clicked(self, event):
        # print("scenario clicked", event.widget)
        self.master.state.set_curr_uc(self.name)
        self.focus_force()
        for scenario in self.master.scenarios_frames:
            scenario.config(relief="flat")
        self.config(relief="groove")  # borderwidth=5, highlightbackground="green", highlightthickness=1

        self.master.master.on_refresh_frame3_flowchart()

    def on_enter_clicked(self, event):
        self.add_step_clicked()

    def add_step_clicked(self):
        step_text = self.inp_step.get().strip()

        if not step_text:  # if empty
            return

        self.inp_step.delete(0, END)
        self.add_step_frame(step_text, [])
        self.master.state.add_step(step_text)
        # print(self.master.state.curr_uc,"\n",self.master.state.curr_uc_diagram,"\n",self.master.state.all_uc_diagrams)
        self.master.state.remove_connections()  # remove all connections from current UC
        self.master.master.remove_frame3_flowchart()

    def add_step_frame(self, step_text, selected_words):
        step_frame = Step(self, step_text, selected_words)
        step_frame.pack(fill=X)
        self.step_frames.append(step_frame)
        self.set_lbl_next_step_id()

    def set_lbl_next_step_id(self):
        self.lbl_next_step_id.config(text=f"{len(self.step_frames)+1}.")

    def delete_step(self, idx):
        self.step_frames.pop(idx)
        self.set_lbl_next_step_id()
        self.renumerate_steps()

    def renumerate_steps(self):
        if self.step_frames:  # if not empty
            for i, step in enumerate(self.step_frames):
                step.change_id(i+1)


class Step(Frame):
    def __init__(self, master, text, selected_words, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.text = text
        self.id = len(master.step_frames)+1
        words = text.split()

        self.lbl_id = Label(self, text=f"{self.id}.")
        self.lbl_id.pack(side=LEFT)

        for i in range(len(words)+1):
            if i == len(words):  # delete button jest na końcu
                text = "Delete"
                btn = DeleteStepButton(self, text=text)
                btn.pack(side=RIGHT)
            else:
                text = words[i]
                btn = StepWordButton(self, text=text)
                if text in selected_words:
                    btn.config(bg="yellow")
                btn.pack(side=LEFT)

        self.master.bind_LMB_click(self)

    def change_id(self, new_id):
        self.id = new_id
        self.lbl_id.config(text=f"{self.id}.")


class StepWordButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command=self.click_function)
        self.config(background='white')
        # self.config(background=self.master.cget("bg"))
        self.config(borderwidth=0)

    def click_function(self):
        if self['bg'] == 'white':
            self['bg'] = 'yellow'
            self.master.master.master.state.add_selected_word(self.master.id, self['text']) # self.master - Step, self.master.master - Scenario, self.master.master.master - FrameScenarios
        elif self['bg'] == 'yellow':
            self['bg'] = 'white'
            self.master.master.master.state.remove_selected_word(self.master.id, self['text'])

        self.master.master.master.state.remove_connections()
        self.master.master.master.master.remove_frame3_flowchart()
        # print("selected_verbs word clicked: ", self.master.master.selected_verbs)
        print("selected_verbs word clicked: ", self.master.master.master.state.curr_uc)


class DeleteStepButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command=self.click_function)
        self.config(background='#827675')

    def click_function(self):
        for item in self.master.winfo_children():
            if item['bg'] == 'yellow':
                self.master.master.master.state.remove_selected_word(self.master.id, item["text"])
        self.master.master.delete_step(self.master.id - 1)  # self.master - Step,   self.master.master - Scenario,   self.master.master.master - FrameScenarios, self.master.master.master.master - Application TRAGEZA :(
        self.master.master.master.state.delete_step(self.master.id)
        self.master.master.master.state.remove_connections()  # remove all connections from current UC
        self.master.master.master.master.remove_frame3_flowchart()


        self.master.destroy()  # self.master = Step

        # print("selected_verbs after delete: ", self.master.master.selected_verbs)
        print("selected_verbs after delete: ", self.master.master.master.state.curr_uc)

