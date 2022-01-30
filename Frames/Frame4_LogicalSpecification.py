import json
import os
from tkinter import *
from tkinter import ttk
from pathlib import Path

from GeneratorFormulLogicznych.GeneratorFormulLogicznychMain import GenerateLogicalSpecification
from GeneratorFormulLogicznych.LogicType import LogicType
from Helpers.State import SPECIFICATION_STRING, NAME


class FrameLogicalSpecification(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master=master, text="Logical Specification", *args, **kwargs)

        self.state = state

        self.sv_specification_string = StringVar()
        self.lbl_specification_string = Label(self, textvariable=self.sv_specification_string)
        self.lbl_specification_string.pack(side=TOP)

        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(side=TOP, fill=X)

        self.lbl_logical_formulas_FOL_title = Label(self, text="First Order Logic", font='Arial 11') # 'Arial 11 bold'
        self.lbl_logical_formulas_FOL_title.pack(side=TOP)

        self.sv_logical_formulas_FOL = StringVar()
        self.lbl_logical_formulas_FOL = Label(self, textvariable=self.sv_logical_formulas_FOL)
        self.lbl_logical_formulas_FOL.pack(side=TOP)

        separator2 = ttk.Separator(self, orient='horizontal')
        separator2.pack(side=TOP, fill=X)

        self.lbl_logical_formulas_LTL_title = Label(self, text="Linear Temporal Logic", font='Arial 11')
        self.lbl_logical_formulas_LTL_title.pack(side=TOP)

        self.sv_logical_formulas_LTL = StringVar()
        self.lbl_logical_formulas_LTL = Label(self, textvariable=self.sv_logical_formulas_LTL)
        self.lbl_logical_formulas_LTL.pack(side=TOP)

    def refresh(self):
        cur_specification_string = self.state.curr_uc[SPECIFICATION_STRING]
        self.sv_specification_string.set(cur_specification_string)

        fol_formulas = self.generate_logical_specification(cur_specification_string, LogicType.FOL)
        self.sv_logical_formulas_FOL.set(fol_formulas)

        ltl_formulas = self.generate_logical_specification(cur_specification_string, LogicType.LTL)
        self.sv_logical_formulas_LTL.set(ltl_formulas)

        self.save_to_file()

    def generate_logical_specification(self, specification_string, logic_type):
        formulas = ''
        if specification_string != '':
            try:
                formulas = GenerateLogicalSpecification(specification_string, logic_type)
            except:
                formulas = f"Logical formulas generation error!)"  # (Logic type: {logic_type.name}
        return formulas

    def save_to_file(self):
        fol_formulas = self.sv_logical_formulas_FOL.get()
        ltl_formulas = self.sv_logical_formulas_LTL.get()
        specification = {SPECIFICATION_STRING: self.state.curr_uc[SPECIFICATION_STRING],
                         LogicType.FOL.name: fol_formulas,
                         LogicType.LTL.name: ltl_formulas
                         }
        json_object = json.dumps(specification, indent=4)

        specification_file_path = self.make_specification_file_path()

        with open(specification_file_path, "w") as outfile:
            outfile.write(json_object)

    def make_specification_file_path(self):
        img_path = self.state.get_curr_img_path()
        _, img_name = os.path.split(img_path)
        dir_name = os.path.splitext(img_name)[0]
        dir_name = f"{dir_name}_output"
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        specification_file_path = f'{dir_name}{os.sep}{self.state.curr_uc[NAME]}_specification.json'
        return specification_file_path
