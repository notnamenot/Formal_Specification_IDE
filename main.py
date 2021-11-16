# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
# import Image

MAX_WIDTH = 600
MAX_HEIGHT = 800

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class Scenario(Frame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id = ""
        # self.name = name
        # self.steps = []
        # self.step_frames = []

        self.selected_verbs = []

        self.frame_id_name = LabelFrame(self)
        self.frame_id_name.pack(fill=X)
        self.frame_id_name.rowconfigure(1, weight=1)  # szerokość kolumny 0
        self.frame_id_name.columnconfigure(1, weight=1)  # szerokość kolumny 0

        self.lbl_scenario_id = Label(self.frame_id_name, text=self.id + "    ")
        self.lbl_scenario_name = Label(self.frame_id_name, text=name, font=("Arial", 12))
        self.lbl_scenario_id.grid(row=0, column=0, sticky=N + S)
        self.lbl_scenario_name.grid(row=0, column=1, sticky=N + S)

        # self.btn_add_step = AddStepButton(self, text="Add")
        self.btn_add_step = Button(self, text="Add", command=self.click_add_step)
        self.btn_add_step.pack(side=BOTTOM, fill=X)

        self.inp_step = Entry(self)
        self.inp_step.insert(0, "Enter step...")
        self.inp_step.pack(side=BOTTOM, fill=X)

    def click_add_step(self):
        step_text = self.inp_step.get().strip()

        if not step_text:  # if empty
            return

        # words = step_text.split()

        self.inp_step.delete(0, END)

        step_frame = Step(self, step_text)
        # self.step_frames.append(step_frame)
        step_frame.pack(fill=X)


class Step(Frame):
    def __init__(self, master, text, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        # self.words = []
        # self.text = text
        words = text.split()

        for i in range(len(words)+1):
            if i == len(words):  # delete button
                text = "Delete"
                btn = DeleteScenarioButton(self, text=text)
                btn.grid(row=0, column=i, padx=(20, 0), sticky=E+W)  # padx=(20, 0) - odstęp tylko z lewej, sticky=E+W - rozciągnięcie na szerokość
            else:
                text = words[i]
                # btn = Button(frame_splited_scenario, text=words[i], command=lambda w=words[i]: word_clicked(w))
                btn = StepWordButton(self, text=text)
                btn.grid(row=0, column=i)


class StepWordButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command=self.click_function)
        self.config(background='white')

    def click_function(self):
        global selected_verbs
        if self['bg'] == 'white':
            self['bg'] = 'yellow'
            # selected_verbs.append(self['text'])
            self.master.master.selected_verbs.append(self['text']) # self.master - Step, self.master.master - scenario
            print("huhuhu",self.master.master.selected_verbs)
        elif self['bg'] == 'yellow':
            self['bg'] = 'white'
            self.master.master.selected_verbs.remove(self['text']) # self.master - Step, self.master.master - scenario
            # selected_verbs.remove(self['text'])
            # self.config(background=new_color, activebackground=new_color)


class DeleteScenarioButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command=self.click_function)
        self.config(background='#827675')

    def click_function(self):
        for item in self.master.winfo_children():
            if item['bg'] == 'yellow':
                selected_verbs.remove(item['text'])
        self.master.destroy()
        print("selected_verbs after delete: ", selected_verbs)


class AddStepButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command=self.click_function)

    def click_function(self):
        for item in self.master.winfo_children():
            print(item)
        print(type(self.master.master))
        l = Label(self.master, text="abhfeefw")
        if len(self.master.winfo_children()) > 4:
            l = Label(self.master, text="lolo")
        l.pack(anchor=W)


if __name__ == '__main__':

    root = Tk()     # root window
    root.title("IDE XD")
    # root.geometry("900x700")

    frame1_UC = LabelFrame(root, text="Use Case Diagram")  #  width=500, height=500, width=root.winfo_width()-20
    root.columnconfigure(0, weight=1, minsize=400)  # szerokość kolumny 0
    root.columnconfigure(1, weight=3)           # szerokosc kolumny 2 ma być  3 razy większa niż 1 i 3, w obrębie wolnego pola
    root.columnconfigure(2, weight=1)  #
    root.rowconfigure(0, weight=1, minsize=200)  # wysokość wiersza
    # root.grid_propagate(False)
    # frame1_UC.grid_propagate(False)

    frame2_scenario = LabelFrame(root, text="Scenarios")
    frame3_flowchart = LabelFrame(root, text="Flowchart")

    frame1_UC.grid(row=0, column=0, sticky="news")  # fill=None, sticky=W+E, sticky=N //news news fills whole
    frame2_scenario.grid(row=0, column=1, sticky=N+S)
    frame3_flowchart.grid(row=0, column=2, sticky=N+S)


    #################### FRAME1 - UC Diagram ####################

    def set_uc_img(filename):
        # global lbl_filename
        lbl_filename.configure(text=filename)

        i = Image.open(filename)

        print(i.size)  # 0 - width, 1 - height
        if i.size[0] > MAX_WIDTH:
            width_perc = (MAX_WIDTH / float(i.size[0]))
            height_size = int((float(i.size[1]) * float(width_perc)))
            i = i.resize((MAX_WIDTH, height_size), Image.ANTIALIAS)
        if i.size[1] > MAX_HEIGHT:
            height_percent = (MAX_HEIGHT / float(i.size[1]))
            width_size = int((float(i.size[0]) * float(height_percent)))
            i = i.resize((width_size, MAX_HEIGHT), Image.ANTIALIAS)

        img2 = ImageTk.PhotoImage(i)
        global panel
        panel.configure(image=img2)
        panel.image = img2



    def open_file():
        # TODO remove prev img or add possibility to have many, pack dodaje, grid by zastępował
        filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("png files", "*.png"),
                                                                                              ("jpg files", "*.jpg"),
                                                                                              ("jpeg files", "*.jpeg"),
                                                                                              ("all files", "*.*")))
        if not filename or filename in images:
            return

        set_uc_img(filename)
        images.append(filename)

        btn_next.configure(state=DISABLED)

        if len(images) > 1:
            btn_prev.configure(state=NORMAL)
            btn_prev.configure(command=lambda: prev_uc_clicked(len(images)-2)) # przedostatni

        print("images", images)

    def next_uc_clicked(image_number):
        print("image_number", image_number)
        # global btn_prev
        btn_prev.configure(command=lambda: prev_uc_clicked(image_number-1))
        btn_next.configure(command=lambda: next_uc_clicked(image_number+1))
        if image_number == len(images)-1:
            btn_next.configure(state=DISABLED)
        btn_prev.configure(state=NORMAL)

        set_uc_img(images[image_number])

    def prev_uc_clicked(image_number):
        print("image_number", image_number)
        # global btn_prev
        btn_prev.configure(command=lambda: prev_uc_clicked(image_number-1))
        btn_next.configure(command=lambda: next_uc_clicked(image_number+1))
        if image_number == 0:
            btn_prev.configure(state=DISABLED)
        btn_next.configure(state=NORMAL)

        set_uc_img(images[image_number])


    images = []

    frame_import_UC = Frame(frame1_UC)
    frame_import_UC.pack()

    btn_import_image = Button(frame_import_UC, text="Import", command=open_file)
    btn_import_image.pack(side=LEFT)

    btn_prev = Button(frame_import_UC, text="<", state=DISABLED, command=lambda: prev_uc_clicked(0))  # NORMAL
    btn_prev.pack(side=LEFT)

    lbl_filename = Label(frame_import_UC, text="")
    lbl_filename.pack(side=LEFT)  # grid(row=0, column=0)

    btn_next = Button(frame_import_UC, text=">", state=DISABLED, command=lambda: next_uc_clicked(1))  # NORMAL, zaczynamy od 0
    btn_next.pack(side=LEFT)

    img = ImageTk.PhotoImage(Image.open("uc_place_holder.png"))  # TODO wrzucić to shape
    panel = Label(frame1_UC, image=img)
    panel.pack(side="top")  # ,fill="both", expand="yes"






    #################### FRAME2 - SCENARIOS ####################

    frame_input_scenario = LabelFrame(frame2_scenario)
    frame_input_scenario.pack()

    input_scenario_id = Entry(frame_input_scenario, width=3, borderwidth=3)
    input_scenario_id.grid(row=0, column=0)
    input_scenario_id.insert(0, "UC")

    input_scenario_name = Entry(frame_input_scenario, width=50, borderwidth=3)
    input_scenario_name.grid(row=0, column=1)
    input_scenario_name.insert(0, "Enter scenario...")

    selected_verbs = []

    def word_clicked(word):
        global selected_verbs
        selected_verbs.append(word)
        print(word, selected_verbs)


    scenarios = []

    def add_scenario_clicked():
        print(f'selected_verbs {selected_verbs}')
        scenario = input_scenario_name.get().strip()
        id = input_scenario_id.get().strip()

        if not scenario:  # if empty
            return

        input_scenario_name.delete(0, END)
        input_scenario_id.delete(0, END)

        # global frame_scenario
        frame_scenario = Scenario(frame2_scenario, scenario)
        frame_scenario.pack(fill=X, pady=(10, 0))
        scenarios.append(frame_scenario)


        # btns.append(btn)
        # TODO możliwość zmiany kolejnoości - ruszanie framem



    btn_add_scenario = Button(frame_input_scenario, text="Add", command=add_scenario_clicked)
    btn_add_scenario.grid(row=0, column=2)



    root.mainloop()
