from tkinter import *

from Frames.Frame1_UC import FrameUC
from Frames.Frame2_scenarios import FrameScenarios
from Frames.Frame3_flowchart import FrameFlowchart
from Frames.Frame4_LogicalSpecification import FrameLogicalSpecification

from Helpers.State import State

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

        self.frame3_flowchart = FrameFlowchart(self, self.state)
        # self.frame3_flowchart.grid(row=0, column=2, sticky=N+S)

        self.frame4_logical_specification = FrameLogicalSpecification(self, self.state)
        # self.frame4_logical_specification.grid(row=0, column=3, sticky=N+S)

    def add_frame3_flowchart(self):
        if self.is_frame3_flowchart_visible():
            # print("frame3 existed")
            return

        # self.frame3_flowchart = FrameFlowchart(self, self.state)
        self.frame3_flowchart.grid(row=0, column=2, sticky=N+S)
        self.frame3_flowchart_refresh()

    def remove_frame3_flowchart(self):
        if self.is_frame3_flowchart_visible():
            self.frame3_flowchart.grid_forget()
        self.remove_frame4_logical_specification()

    def add_frame4_logical_specification(self):
        if self.frame4_logical_specification.winfo_ismapped():
            return
        self.frame4_logical_specification.grid(row=0, column=3, sticky=N+S)
        self.frame4_logical_specification.refresh()

    def remove_frame4_logical_specification(self):
        if self.frame4_logical_specification.winfo_ismapped():
            self.frame4_logical_specification.grid_forget()

    def on_uc_diagram_changed(self):
        # print("from refresh_frames\nall\n", self.state.all_uc_diagrams, "\ncurr\n", self.state.curr_uc_diagram)
        self.frame2_scenarios.refresh()
        if self.state.curr_uc_diagram_connections_exist() and not self.frame2_scenarios.validate_state():  # istnieje już jakiś flowchart i wszędzie są selected_words
            self.add_frame3_flowchart()
            self.frame3_flowchart_refresh()
        else:
            self.remove_frame3_flowchart()

    def frame3_flowchart_refresh(self):
        self.frame3_flowchart.refresh()

    def on_refresh_frame3_flowchart(self):
        if self.is_frame3_flowchart_visible():
            self.frame3_flowchart_refresh()
        self.on_refresh_frame4_logical_specification()
        self.remove_frame4_logical_specification()

    def on_refresh_frame4_logical_specification(self):
        self.frame4_logical_specification.refresh()

    def is_frame3_flowchart_visible(self):
        if self.frame3_flowchart.winfo_ismapped():  # winfo_exists()
            return True
        return False

