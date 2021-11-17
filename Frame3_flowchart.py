from tkinter import *


class FrameFlowchart(LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, text="Workflow Diagram", *args, **kwargs)

        # self.padding

        # self.canvas = Canvas(self)
        # self.canvas.pack()
        #
        # self.rectangle = self.canvas.create_rectangle(
        #     5, 5, 50, 50, fill="#d6c085")
        # print(type(self.rectangle))
        ## self.t = self.rectangle.createText(8,8,text="ddd")

        self.lbl_start = Label(self, text="Start", bg="#eddeb4", padx=8, pady=8, width=8)
        self.lbl_start.pack(side=LEFT, anchor=NW)

        self.lbl_seq = Label(self, text="Sequence", bg="#8aaceb", padx=8, pady=8, width=8)
        self.lbl_seq.pack(side=LEFT, anchor=NW)

        self.lbl_branch = Label(self, text="Branch", bg="#6df776", padx=8, pady=8, width=8)
        self.lbl_branch.pack(side=LEFT, anchor=NW)

        self.lbl_branch_re = Label(self, text="BranchRe", bg="#5acc61", padx=8, pady=8, width=8)
        self.lbl_branch_re.pack(side=LEFT, anchor=NW)

        self.lbl_concur = Label(self, text="Concur", bg="#eb9f73", padx=8, pady=8, width=8)
        self.lbl_concur.pack(side=LEFT, anchor=NW)

        self.lbl_concur_re = Label(self, text="ConcurRe", bg="#cc845a", padx=8, pady=8, width=8)
        self.lbl_concur_re.pack(side=LEFT, anchor=NW)

        self.lbl_end = Label(self, text="End", bg="#eddeb4", padx=8, pady=8, width=8)
        self.lbl_end.pack(side=LEFT, anchor=NW)

# class Block: