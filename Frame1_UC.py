from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import xml.etree.ElementTree as ET

from State import State

MAX_WIDTH = 600
MAX_HEIGHT = 800


class FrameUC(LabelFrame):
    def __init__(self, master, state, *args, **kwargs):
        super().__init__(master, text="Use Case Diagram", width=100, height=700, *args, **kwargs)

        self.state = state

        self.frame_import_UC = Frame(self)
        self.frame_import_UC.pack()  # fill=BOTH

        self.frame_import_UC.rowconfigure(0, weight=1)  # img name
        self.frame_import_UC.rowconfigure(1, weight=1)  # xml name
        self.frame_import_UC.columnconfigure(0, weight=1)  # button import
        self.frame_import_UC.columnconfigure(1, weight=1)  # <
        self.frame_import_UC.columnconfigure(2, weight=2)  # nazwy
        self.frame_import_UC.columnconfigure(3, weight=1)  # >

        self.btn_import_image = Button(self.frame_import_UC, text="Import files", command=self.open_img)
        # self.btn_import_image.pack(side=LEFT)
        self.btn_import_image.grid(row=0, column=0, rowspan=2, sticky=W, padx=(0, 20))

        # self.btn_import_xml = Button(self.frame_import_UC, text="Import xml", command=self.open_xml)
        # self.btn_import_xml.pack(side=LEFT)

        self.btn_prev = Button(self.frame_import_UC, text="<", state=DISABLED, command=self.prev_uc_clicked)
        # self.btn_prev.pack(side=LEFT)
        self.btn_prev.grid(row=0, column=1, rowspan=2, sticky=NS, padx=(5, 5))

        self.lbl_img_name = Label(self.frame_import_UC, text="Image file name")
        # self.lbl_img_name.pack(side=LEFT)
        self.lbl_img_name.grid(row=0, column=2)

        self.lbl_xml_name = Label(self.frame_import_UC, text="XML file name")
        self.lbl_xml_name.grid(row=1, column=2)

        self.btn_next = Button(self.frame_import_UC, text=">", state=DISABLED, command=self.next_uc_clicked)
        # self.btn_next.pack(side=LEFT)
        self.btn_next.grid(row=0, column=3, rowspan=2, sticky=NS, padx=(5, 5))

        # img = ImageTk.PhotoImage(Image.open("uc_place_holder.png"))  # TODO wrzucić to shape
        # self.panel = Label(self, image=img)
        self.panel = Label(self)
        self.panel.pack()

    def open_img(self):
        img_path = filedialog.askopenfilename(initialdir=".", title="Select image", filetypes=(("image files", "*.png"),
                                                                                               ("image files", "*.jpg"),
                                                                                               ("image files", "*.jpeg"),
                                                                                               ("all files", "*.*")))
        if not img_path:  # dialog canceled
            return

        contains_img, contains_xml = self.state.contains_img_xml(img_path)

        if contains_img and not contains_xml:
            self.state.set_curr_uc_diagram(img_path)
            self.open_xml()
        elif contains_img:
            self.state.set_curr_uc_diagram(img_path)
        else:
            self.state.add_uc_diagram(img_path)  # also sets curr_uc_diagram
            self.open_xml()

        self.reload()

    def open_xml(self):
        img_path = self.state.get_curr_img_path()
        img_dir, _ = os.path.split(img_path)

        xml_path = filedialog.askopenfilename(initialdir=img_dir, title="Select XML", filetypes=(("xml files", "*.xml"),
                                                                                                 ("all files", "*.*")))
        if not xml_path:  # dialog canceled
            return

        self.state.set_xml_path(xml_path)

        use_cases = self.find_use_cases(xml_path)

        self.state.add_use_cases(use_cases)

    def find_use_cases(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        # print(root.tag, root.attrib)

        uc_xml_elems = []

        # uc_xml_elems = root.findall(".//MasterView/UseCase")  # visual paradigm 'Xml_structure': 'simple'
        uc_xml_elems.extend(root.findall(".//UseCase"))  # visual paradigm 'Xml_structure': 'simple'
        uc_xml_elems.extend(root.findall(".//Model[@modelType='UseCase']"))  # visual paradigm 'Xml_structure': 'traditional' (old)

        namespaces = {'xmi': 'http://www.omg.org/spec/XMI/20131001'}
        uc_xml_elems.extend(root.findall(".//packagedElement[@xmi:type='uml:UseCase']", namespaces))  # Papyrus

        uc_xml_elems.extend(root.findall(".//UMLUseCase"))  # Sinvas

        namespaces = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        uc_xml_elems.extend(root.findall(".//packagedElement[@xsi:type='uml:UseCase']", namespaces))  # GenMyModel

        # for elem in root:
        #     print(elem.tag, elem.attrib)

        use_cases = []
        for elem in uc_xml_elems:
            if 'Name' in elem.attrib:
                use_cases.append(elem.attrib['Name'])
            if 'name' in elem.attrib:
                use_cases.append(elem.attrib['name'])

        use_cases = list(set(use_cases))  # remove duplicates

        return use_cases

    def next_uc_clicked(self):
        self.state.change_curr_uc_diagram(self.state.get_curr_uc_diagram_seq() + 1)
        self.reload()

    def prev_uc_clicked(self):
        self.state.change_curr_uc_diagram(self.state.get_curr_uc_diagram_seq() - 1)
        self.reload()

    def reload(self):
        self.set_buttons_state()

        img_path = self.state.get_curr_img_path()
        _, img_name = os.path.split(img_path)
        self.lbl_img_name.config(text=img_name)

        xml_path = self.state.get_curr_xml_path()
        _, xml_name = os.path.split(xml_path)
        self.lbl_xml_name.config(text=xml_name)

        self.set_uc_diagram_img(img_path)

        self.master.refresh_frames()

    def set_buttons_state(self):
        curr_uc_diagram_seq = self.state.get_curr_uc_diagram_seq()
        all_uc_diagrams_number = self.state.get_all_uc_diagrams_number()

        if curr_uc_diagram_seq == 0:
            self.btn_prev.configure(state=DISABLED)
        else:
            self.btn_prev.configure(state=NORMAL)
        if curr_uc_diagram_seq == all_uc_diagrams_number-1:
            self.btn_next.configure(state=DISABLED)
        else:
            self.btn_next.configure(state=NORMAL)

    def set_uc_diagram_img(self, img_path):
        i = Image.open(img_path)

        # print(i.size)  # 0 - width, 1 - height
        if i.size[0] > MAX_WIDTH:
            width_perc = (MAX_WIDTH / float(i.size[0]))
            height_size = int((float(i.size[1]) * float(width_perc)))
            i = i.resize((MAX_WIDTH, height_size), Image.ANTIALIAS)
        if i.size[1] > MAX_HEIGHT:
            height_perc = (MAX_HEIGHT / float(i.size[1]))
            width_size = int((float(i.size[0]) * float(height_perc)))
            i = i.resize((width_size, MAX_HEIGHT), Image.ANTIALIAS)

        img2 = ImageTk.PhotoImage(i)

        self.panel.configure(image=img2)
        self.panel.image = img2



