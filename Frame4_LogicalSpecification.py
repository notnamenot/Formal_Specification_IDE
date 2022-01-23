import json
import os
from tkinter import *
from tkinter import ttk
from pathlib import Path

from GeneratorFormulLogicznych.GeneratorFormulLogicznychMain import GenerateLogicalSpecification
from State import SPECIFICATION_STRING, LOGICAL_SPECIFICATION, NAME


class FrameLogicalSpecification(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master=master, text="Logical Specification", *args, **kwargs)

        self.state = state

        self.sv_specification_string = StringVar()
        self.lbl_specification_string = Label(self, textvariable=self.sv_specification_string)
        self.lbl_specification_string.pack(side=TOP)

        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(side=TOP, fill=X)

        self.sv_logical_formulas = StringVar()
        self.lbl_logical_formulas = Label(self, textvariable=self.sv_logical_formulas)
        self.lbl_logical_formulas.pack(side=TOP)

    def refresh(self):
        cur_specification_string = self.state.curr_uc[SPECIFICATION_STRING]
        self.sv_specification_string.set(cur_specification_string)
        self.sv_logical_formulas.set('')
        formulas = ''
        if cur_specification_string != '':
            try:
                formulas = GenerateLogicalSpecification(cur_specification_string)
                self.sv_logical_formulas.set(formulas)
            except:
                formulas = "Logical formulas generation error!"
                self.sv_logical_formulas.set(formulas)

        self.save_to_file(formulas)

    def save_to_file(self, formulas):
        specification = {SPECIFICATION_STRING: self.state.curr_uc[SPECIFICATION_STRING],
                         LOGICAL_SPECIFICATION: formulas}
        json_object = json.dumps(specification, indent=4)

        img_path = self.state.get_curr_img_path()
        _, img_name = os.path.split(img_path)
        dir_name = os.path.splitext(img_name)[0]
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        output_file_path = f'{dir_name}{os.sep}{self.state.curr_uc[NAME]}_specification.json'

        with open(output_file_path, "w") as outfile:
            outfile.write(json_object)

