from tkinter import *

from Frame1_UC import *
from Frame2_scenarios import *


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Formal Specification Generator IDE")
        self.create_widgets()

    def create_widgets(self):
        self.frame1_UC = FrameUC(self)
        self.frame1_UC.grid(row=0, column=0, sticky="news")

        self.frame2_scenario = FrameScenarios(self)
        self.frame2_scenario.grid(row=0, column=1, sticky=N+S)

        self.frame3_flowchart = LabelFrame(self, text="Flowchart")
        self.frame3_flowchart.grid(row=0, column=2, sticky=N+S)
