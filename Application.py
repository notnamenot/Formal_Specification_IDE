from tkinter import *

from Frame1_UC import FrameUC
from Frame2_scenarios import FrameScenarios
from Frame3_flowchart import FrameFlowchart

from State import State

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Formal Specification Generator IDE")
        # self.ucs_summary = {}
        # self.curr_uc =
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

        self.frame2_scenario = FrameScenarios(self)
        self.frame2_scenario.grid(row=0, column=1, sticky=N+S)

        self.frame3_flowchart = FrameFlowchart(self)
        self.frame3_flowchart.grid(row=0, column=2, sticky=N+S)

    def refresh_frames(self, uc_summary, current_image_path):
        self.uc_summary = uc_summary
        self.frame2_scenario.load_conf(uc_summary[current_image_path])

        print("from refresh_frames", self.state.all, self.state.curr_uc)
    # def update_conf(self, conf):