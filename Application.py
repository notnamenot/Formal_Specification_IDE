from tkinter import *

from Frame1_UC import FrameUC
from Frame2_scenarios import FrameScenarios
from Frame3_flowchart import FrameFlowchart

from State import State

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Formal Specification Generator IDE")

        self.state = State()

        self.create_widgets()
        # self.geometry("800x600")

        # the same width
        # self.columnconfigure((0, 1, 2), weight=1, uniform='col')
        # self.columnconfigure(0, weight=1, uniform='col')
        # self.columnconfigure(1, weight=1, uniform='col')
        # self.columnconfigure(2, weight=1, uniform='col')

    def create_widgets(self):
        self.frame1_UC = FrameUC(self, self.state)
        self.frame1_UC.grid(row=0, column=0, sticky="news")

        self.frame2_scenarios = FrameScenarios(self, self.state)
        self.frame2_scenarios.grid(row=0, column=1, sticky=N+S)

        # self.frame3_flowchart = FrameFlowchart(self)
        # self.frame3_flowchart.grid(row=0, column=2, sticky=N+S)

    def add_frame3_flowchart(self):
        self.frame3_flowchart = FrameFlowchart(self, self.state)
        self.frame3_flowchart.grid(row=0, column=2, sticky=N+S)

    def refresh_frames(self):
        # print("from refresh_frames\nall\n", self.state.all_uc_diagrams, "\ncurr\n", self.state.curr_uc_diagram)
        self.frame2_scenarios.refresh()
        # TODO i refresh flowchart
