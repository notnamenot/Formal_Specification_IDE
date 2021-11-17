from tkinter import *


class FrameScenarios(LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, text="Scenarios", *args, **kwargs)

        self.scenarios = []

        self.frame_input_scenario = Frame(self)
        self.frame_input_scenario.pack()

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

        if not scenario:  # if empty
            return

        self.input_scenario_name.delete(0, END)
        # input_scenario_id.delete(0, END)

        frame_scenario = Scenario(self, scenario)
        frame_scenario.pack(fill=X, pady=(10, 0))
        self.scenarios.append(frame_scenario)

        # TODO możliwość zmiany kolejnoości - ruszanie framem


# TODO checkbox na scenariuszu do którego robimy flowchart?
class Scenario(Frame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id = ""
        # self.name = name
        self.step_frames = []  # TODO trzebaby pamiętać przy usuwaniu stepa żeby stąd też czyścić
        self.selected_verbs = []

        self.frame_id_name = LabelFrame(self, relief="flat")  # relief="ridge"
        self.frame_id_name.pack(fill=X)
        self.frame_id_name.rowconfigure(1, weight=1)  # szerokość kolumny 1
        self.frame_id_name.columnconfigure(1, weight=1)  # szerokość kolumny 1

        self.lbl_scenario_id = Label(self.frame_id_name, text=self.id + "    ")
        self.lbl_scenario_name = Label(self.frame_id_name, text=name, font=("Arial", 12))
        self.lbl_scenario_id.grid(row=0, column=0, sticky=N + S)
        self.lbl_scenario_name.grid(row=0, column=1, sticky=N + S)

        self.btn_add_step = Button(self, text="Add", command=self.click_add_step)
        self.btn_add_step.pack(side=BOTTOM, fill=X)

        self.frame_enter_step = Frame(self)
        self.frame_enter_step.pack(side=BOTTOM, fill=X)

        self.lbl_next_step_id = Label(self.frame_enter_step, text="1.")
        self.lbl_next_step_id.pack(side=LEFT)

        self.inp_step = Entry(self.frame_enter_step)
        # self.inp_step.insert(0, f'{self.number_of_steps+1}.')  # f'{len(self.step_frames)+1}.'
        self.inp_step.insert(0, 'Enter step..')  # f'{len(self.step_frames)+1}.'
        self.inp_step.pack(side=LEFT, fill=X, expand=True)

    def click_add_step(self):
        step_text = self.inp_step.get().strip()

        if not step_text:  # if empty
            return

        self.inp_step.delete(0, END)

        step_frame = Step(self, step_text)
        step_frame.pack(fill=X)
        self.step_frames.append(step_frame)
        self.set_lbl_next_step_id_text()

    def delete_step(self, idx):
        self.step_frames.pop(idx)
        self.set_lbl_next_step_id_text()
        self.renumerate_steps()

    def set_lbl_next_step_id_text(self):
        self.lbl_next_step_id.config(text=f"{len(self.step_frames)+1}.")

    def renumerate_steps(self):
        if self.step_frames:  # if not empty
            for i, step in enumerate(self.step_frames):
                step.change_id(i+1)


class Step(Frame):
    def __init__(self, master, text, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.id = len(master.step_frames)+1
        words = text.split()

        self.lbl_id = Label(self, text=f"{self.id}.")
        self.lbl_id.pack(side=LEFT)

        for i in range(len(words)+1):
            if i == len(words):  # delete button jest na końcu
                # self.master.step_frames.remove(self)
                text = "Delete"
                btn = DeleteStepButton(self, text=text)
                btn.pack(side=RIGHT)
            else:
                text = words[i]
                btn = StepWordButton(self, text=text)
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
            self.master.master.selected_verbs.append(self['text'])  # self.master - Step, self.master.master - scenario
        elif self['bg'] == 'yellow':
            self['bg'] = 'white'
            self.master.master.selected_verbs.remove(self['text'])  # self.master - Step, self.master.master - scenario

        print("selected_verbs word clicked: ", self.master.master.selected_verbs)


class DeleteStepButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command=self.click_function)
        self.config(background='#827675')

    def click_function(self):
        for item in self.master.winfo_children():
            if item['bg'] == 'yellow':
                self.master.master.selected_verbs.remove(item['text'])  # self.master.master = Scenario
        self.master.master.delete_step(self.master.id - 1)
        self.master.destroy()  # self.master = Step

        print("selected_verbs after delete: ", self.master.master.selected_verbs)

