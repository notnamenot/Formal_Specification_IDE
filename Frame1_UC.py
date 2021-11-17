from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import xml.etree.ElementTree as ET

MAX_WIDTH = 600
MAX_HEIGHT = 800


class FrameUC(LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, text="Use Case Diagram", *args, **kwargs)

        self.images = []
        self.ucs = {}

        self.frame_import_UC = Frame(self)
        self.frame_import_UC.pack()

        self.btn_import_image = Button(self.frame_import_UC, text="Import files", command=self.open_file)
        self.btn_import_image.pack(side=LEFT)

        # self.btn_import_xml = Button(self.frame_import_UC, text="Import xml", command=self.open_xml)
        # self.btn_import_xml.pack(side=LEFT)

        self.btn_prev = Button(self.frame_import_UC, text="<", state=DISABLED, command=lambda: self.prev_uc_clicked(0))
        self.btn_prev.pack(side=LEFT)

        self.lbl_filename = Label(self.frame_import_UC, text="")
        self.lbl_filename.pack(side=LEFT)

        self.btn_next = Button(self.frame_import_UC, text=">", state=DISABLED, command=lambda: self.next_uc_clicked(1))
        self.btn_next.pack(side=LEFT)

        self.img = ImageTk.PhotoImage(Image.open("uc_place_holder.png"))  # TODO wrzucić to shape
        self.panel = Label(self, image=self.img)
        self.panel.pack()

    def open_file(self):
        file_path = filedialog.askopenfilename(initialdir=".", title="Select image", filetypes=(("image files", "*.png"),
                                                                                                ("image files", "*.jpg"),
                                                                                                ("image files", "*.jpeg"),
                                                                                                ("all files", "*.*")))
        if not file_path or file_path in self.images:
            return

        _, file_name = os.path.split(file_path)

        self.lbl_filename.configure(text=file_name)
        self.set_uc_img(file_path)

        self.images.append(file_path)
        # self.curr_img_file_path = file_path
        self.ucs[file_path] = {}

        self.btn_next.configure(state=DISABLED)

        if len(self.images) > 1:
            self.btn_prev.configure(state=NORMAL)
            self.btn_prev.configure(command=lambda: self.prev_uc_clicked(len(self.images) - 2))  # przedostatni

        print("images", self.images)
        self.open_xml(file_path)

    def set_uc_img(self, filename):
        i = Image.open(filename)

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

    def next_uc_clicked(self, image_number):
        print("image_number", image_number)

        self.btn_prev.configure(command=lambda: self.prev_uc_clicked(image_number - 1))
        self.btn_next.configure(command=lambda: self.next_uc_clicked(image_number + 1))
        if image_number == len(self.images) - 1:
            self.btn_next.configure(state=DISABLED)
        self.btn_prev.configure(state=NORMAL)

        self.set_uc_img(self.images[image_number])

    def prev_uc_clicked(self, image_number):
        print("image_number", image_number)

        # self.grid_forget()

        self.btn_prev.configure(command=lambda: self.prev_uc_clicked(image_number - 1))
        self.btn_next.configure(command=lambda: self.next_uc_clicked(image_number + 1))
        if image_number == 0:
            self.btn_prev.configure(state=DISABLED)
        self.btn_next.configure(state=NORMAL)

        self.set_uc_img(self.images[image_number])

    def open_xml(self, img_path):
        img_dir, _ = os.path.split(img_path)

        xml_file_path = filedialog.askopenfilename(initialdir=img_dir, title="Select XML", filetypes=(("xml files", "*.xml"),
                                                                                                      ("all files", "*.*")))
        if not xml_file_path:
            return

        self.ucs[img_path][xml_file_path] = {}

        # _, file_name = os.path.split(xml_file_path)

        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        print(root.tag)
        print(root.attrib)

        uc_xml_elems = []
        # uc_xml_elems = root.findall(".//MasterView/UseCase")  # visual paradigm 'Xml_structure': 'simple'
        uc_xml_elems.extend(root.findall(".//UseCase"))  # visual paradigm 'Xml_structure': 'simple'
        uc_xml_elems.extend(root.findall(".//Model[@modelType='UseCase']"))  # visual paradigm 'Xml_structure': 'traditional' (old)

        print("uc_xml_elems", uc_xml_elems)
        use_cases = []
        for elem in uc_xml_elems:
            if 'Name' in elem.attrib:
                print('Name', elem.tag, elem.attrib['Name'])
                use_cases.append(elem.attrib['Name'])
            if 'name' in elem.attrib:
                print('name', elem.tag, elem.attrib['name'])
                use_cases.append(elem.attrib['name'])

        use_cases = list(set(use_cases))  # remove duplicates

        for use_case in use_cases:
            self.ucs[img_path][xml_file_path][use_case] = []
        # self.ucs[img_path][xml_file_path] = use_cases

        print("ucs", self.ucs)
