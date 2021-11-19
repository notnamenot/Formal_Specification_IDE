from tkinter import *


class FrameScenarios(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master=master, text="Scenarios", *args, **kwargs)

        self.state = state

        self.scenarios = []

        self.frame_input_scenario = Frame(self)
        self.frame_input_scenario.pack(side=BOTTOM)

        # input_scenario_id = Entry(frame_input_scenario, width=3, borderwidth=3)
        # input_scenario_id.grid(row=0, column=0)
        # input_scenario_id.insert(0, "UC")

        self.input_scenario_name = Entry(self.frame_input_scenario, width=50, borderwidth=3)
        self.input_scenario_name.grid(row=0, column=0)
        self.input_scenario_name.insert(0, "Enter scenario...")

        self.btn_add_scenario = Button(self.frame_input_scenario, text="Add", command=self.add_scenario_clicked)
        self.btn_add_scenario.grid(row=0, column=1)

    def add_scenario_clicked(self):
        scenario = self.input_scenario_name.get().strip()
        # id = input_scenario_id.get().strip()

        if not scenario or not self.state.curr_uc_diagram:  # if empty input or diagram not chosen TODO pokazać kolumne scenarios dopiero po imporcie plików
            return

        self.input_scenario_name.delete(0, END)
        self.input_scenario_name.insert(0, "Enter scenario...")
        # input_scenario_id.delete(0, END)

        self.add_scenario_frame(scenario)

        self.state.add_use_cases([scenario])

        # TODO możliwość zmiany kolejnoości - ruszanie framem - przyciski w górę i w dół

    def add_scenario_frame(self, name):
        frame_scenario = Scenario(self, name)
        frame_scenario.bind('<Button-1>', lambda e: frame_scenario.scenario_clicked(e, name))

        frame_scenario.pack(fill=X, pady=(0, 10), padx=5)
        self.scenarios.append(frame_scenario)
        return frame_scenario

    def refresh(self):
        print("from refresh\nall\n", self.state.all_uc_diagrams, "\ncurr diag\n", self.state.curr_uc_diagram, "\ncurr uc\n", self.state.curr_uc)
        # 1. remove current scenarios
        for s in range(len(self.scenarios)):
            self.scenarios[s].destroy()  # pack_forget

        for i, scenario in reversed(list(enumerate(self.scenarios))):
            scenario.destroy()
            self.scenarios.pop()

        # 2. Add new scenarios
        for obj in self.state.curr_uc_diagram["use_cases"]:
            frame_scenario = self.add_scenario_frame(obj['name'])
            for step in obj["steps"]:
                frame_scenario.add_step_frame(step["text"], step["selected_words"])





# TODO checkbox na scenariuszu do którego robimy flowchart?
class Scenario(LabelFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, relief="flat", highlightthickness=1, *args, **kwargs)
        self.id = ""
        self.name = name

        self.step_frames = []  # TODO trzebaby pamiętać przy usuwaniu stepa żeby stąd też czyścić
        # self.selected_verbs = []

        self.frame_id_name = LabelFrame(self, relief="flat")  # relief="ridge"
        self.frame_id_name.pack(fill=X)
        self.frame_id_name.rowconfigure(1, weight=1)  # szerokość kolumny 1
        self.frame_id_name.columnconfigure(1, weight=1)  # szerokość kolumny 1
        self.frame_id_name.bind('<Button-1>', lambda e: self.scenario_clicked(e, name))

        self.lbl_scenario_id = Label(self.frame_id_name, text=self.id + "    ")
        self.lbl_scenario_id.grid(row=0, column=0, sticky=N + S)
        self.lbl_scenario_id.bind('<Button-1>', lambda e: self.scenario_clicked(e, name))
        self.lbl_scenario_name = Label(self.frame_id_name, text=name, font=("Arial", 12))
        self.lbl_scenario_name.grid(row=0, column=1, sticky=N + S)
        self.lbl_scenario_name.bind('<Button-1>', lambda e: self.scenario_clicked(e, name))

        self.btn_add_step = Button(self, text="Add", command=self.click_add_step)
        self.btn_add_step.pack(side=BOTTOM, fill=X)
        self.btn_add_step.bind('<Button-1>', lambda e: self.scenario_clicked(e, name))

        self.frame_enter_step = Frame(self)
        self.frame_enter_step.pack(side=BOTTOM, fill=X)
        self.frame_enter_step.bind('<Button-1>', lambda e: self.scenario_clicked(e, name))

        self.lbl_next_step_id = Label(self.frame_enter_step, text="1.")
        self.lbl_next_step_id.pack(side=LEFT)
        self.lbl_next_step_id.bind('<Button-1>', lambda e: self.scenario_clicked(e, name))

        self.inp_step = Entry(self.frame_enter_step)
        # self.inp_step.insert(0, f'{self.number_of_steps+1}.')  # f'{len(self.step_frames)+1}.'
        # self.inp_step.insert(0, 'Enter step..')  # f'{len(self.step_frames)+1}.'
        self.inp_step.pack(side=LEFT, fill=X, expand=True)
        self.inp_step.bind('<Button-1>', lambda e: self.scenario_clicked(e, name))

    # def scenario_clicked(self, event, uc_name):
    def scenario_clicked(self, event, name=""):
        # print("scenario_clicked", self.name)
        self.master.state.set_curr_uc(self.name)
        # print("cuc",self.master.state.curr_uc)
        # event.widget.config(bg='red')
        # event.widget.master.config(bg='red')
        # self.config(bg='red')
        self.focus_force()
        for scenario in self.master.scenarios:
            scenario.config(relief="flat")
        self.config(relief="groove") #borderwidth=5, highlightbackground= "green",highlightthickness=1

    def click_add_step(self):
        # print("click_add_step")
        step_text = self.inp_step.get().strip()

        if not step_text:  # if empty
            return

        self.inp_step.delete(0, END)

        self.add_step_frame(step_text, [])

        self.master.state.add_step(step_text)
        # print("tututu")
        # print(self.master.state.curr_uc,"\n",self.master.state.curr_uc_diagram,"\n",self.master.state.all_uc_diagrams)

    def add_step_frame(self, step_text, selected_words):
        step_frame = Step(self, step_text, selected_words)
        step_frame.bind('<Button-1>', lambda e: self.scenario_clicked(e))
        step_frame.pack(fill=X)
        self.step_frames.append(step_frame)
        self.set_lbl_next_step_id_text()


    def set_lbl_next_step_id_text(self):
        self.lbl_next_step_id.config(text=f"{len(self.step_frames)+1}.")

    def delete_step(self, idx):
        self.step_frames.pop(idx)
        self.set_lbl_next_step_id_text()
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
        self.lbl_id.bind('<Button-1>', lambda e: self.master.scenario_clicked(e))
        self.lbl_id.pack(side=LEFT)


        for i in range(len(words)+1):
            if i == len(words):  # delete button jest na końcu
                # self.master.step_frames.remove(self)
                text = "Delete"
                btn = DeleteStepButton(self, text=text)
                btn.bind('<Button-1>', lambda e: self.master.scenario_clicked(e))
                btn.pack(side=RIGHT)
            else:
                text = words[i]
                btn = StepWordButton(self, text=text)
                if text in selected_words:
                    btn.config(bg="yellow")
                btn.bind('<Button-1>', lambda e: self.master.scenario_clicked(e))
                btn.pack(side=LEFT)

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
            self.master.master.master.state.add_selected_word(self.master.id, self['text'])
            # self.master.master.selected_verbs.append(self['text'])  # self.master - Step, self.master.master - scenario

        elif self['bg'] == 'yellow':
            self['bg'] = 'white'
            self.master.master.master.state.remove_selected_word(self.master.id, self['text'])
            # self.master.master.selected_verbs.remove(self['text'])  # self.master - Step, self.master.master - scenario

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
                # self.master.master.selected_verbs.remove(item['text'])  # self.master.master = Scenario
        self.master.master.delete_step(self.master.id - 1)  # self.master - Step,   self.master.master - Scenario
        self.master.master.master.state.delete_step(self.master.id)
        self.master.destroy()  # self.master = Step

        # print("selected_verbs after delete: ", self.master.master.selected_verbs)
        print("selected_verbs after delete: ", self.master.master.master.state.curr_uc)

