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

        # self.images = []  # TODO utrzymywanie images i ucs jest głupie
        # self.ucs = {}

        # self.state = State()
        self.state = state

        # self.curr_uc # TODO , może wyżej

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

        self.btn_prev = Button(self.frame_import_UC, text="<", state=DISABLED, command=lambda: self.prev_uc_clicked(0))
        # self.btn_prev.pack(side=LEFT)
        self.btn_prev.grid(row=0, column=1, rowspan=2, sticky=NS, padx=(5, 5))

        self.lbl_img_name = Label(self.frame_import_UC, text="Image file name")
        # self.lbl_img_name.pack(side=LEFT)
        self.lbl_img_name.grid(row=0, column=2)

        self.lbl_xml_name = Label(self.frame_import_UC, text="XML file name")
        self.lbl_xml_name.grid(row=1, column=2)

        self.btn_next = Button(self.frame_import_UC, text=">", state=DISABLED, command=lambda: self.next_uc_clicked(1))
        # self.btn_next.pack(side=LEFT)
        self.btn_next.grid(row=0, column=3, rowspan=2, sticky=NS, padx=(5, 5))

        self.img = ImageTk.PhotoImage(Image.open("uc_place_holder.png"))  # TODO wrzucić to shape
        self.panel = Label(self, image=self.img)
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
            self.state.set_curr_uc(img_path)
            self.open_xml()
            # self.reload()
        elif contains_img:
            self.state.set_curr_uc(img_path)
            # self.reload()
            # pass
        else:
            self.state.add_img_path(img_path)  # also sets curr_uc
            self.open_xml()

        # if (img_path in self.images) and (not self.ucs[img_path]):
        #     self.open_xml(img_path)
        #     return



        # _, file_name = os.path.split(img_path)
        #
        # self.lbl_img_name.configure(text=file_name)
        # self.set_uc_img(img_path)

        # self.images.append(img_path)
        # self.curr_img_file_path = img_path
        # self.ucs[img_path] = {}

        # self.btn_next.configure(state=DISABLED)
        #
        # # if len(self.images) > 1:
        # if self.state.get_number_of_objects() > 1:
        #     self.btn_prev.configure(state=NORMAL)
        #     self.btn_prev.configure(command=lambda: self.prev_uc_clicked(self.state.get_number_of_objects() - 2))  # przedostatni

        # print("images", self.images)
        # self.open_xml(img_path)

        # self.reload(len(self.images) - 1)
        self.set_buttons_state()
        self.reload()

    def set_uc_img(self, file_path):
        i = Image.open(file_path)

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

    def next_uc_clicked(self, image_number):  # TODO change also xml label
        # print("image_number", image_number)

        # self.btn_prev.configure(command=lambda: self.prev_uc_clicked(image_number - 1))
        # self.btn_next.configure(command=lambda: self.next_uc_clicked(image_number + 1))
        # if image_number == self.state.get_number_of_objects()-1:  # len(self.images) - 1:        # ostatni z listy
        #     self.btn_next.configure(state=DISABLED)
        # self.btn_prev.configure(state=NORMAL)


        # self.state.change_curr_uc(image_number)
        self.state.change_curr_uc(self.state.get_curr_uc_num()+1)
        self.set_buttons_state()
        # self.reload(image_number)
        self.reload()


    def prev_uc_clicked(self, image_number):
        # print("image_number", image_number)

        # self.grid_forget()

        # self.btn_prev.configure(command=lambda: self.prev_uc_clicked(image_number - 1))
        # self.btn_next.configure(command=lambda: self.next_uc_clicked(image_number + 1))
        # if image_number == 0:
        #     self.btn_prev.configure(state=DISABLED)
        # self.btn_next.configure(state=NORMAL)


        # self.state.change_curr_uc(image_number)
        self.state.change_curr_uc(self.state.get_curr_uc_num()-1)
        self.set_buttons_state()
        # self.reload(image_number)
        self.reload()

    def set_buttons_state(self):
        curr_obj_num = self.state.get_curr_uc_num()
        all_obj_num = self.state.get_number_of_objects()

        if curr_obj_num == 0:
            self.btn_prev.configure(state=DISABLED)
        else:
            self.btn_prev.configure(state=NORMAL)
        if curr_obj_num == all_obj_num-1:
            self.btn_next.configure(state=DISABLED)
        else:
            self.btn_next.configure(state=NORMAL)


    def reload(self):
    # def reload(self, image_number):

        # self.state.change_curr_uc(image_number)

        img_path = self.state.get_curr_img_path()  # self.images[image_number]
        self.set_uc_img(img_path)
        _, img_name = os.path.split(img_path)
        self.lbl_img_name.config(text=img_name)

        xml_path = self.state.get_curr_xml_path()
        _, xml_name = os.path.split(xml_path)
        self.lbl_xml_name.config(text=xml_name)

        # self.images.append(img_path)
        self.set_uc_img(img_path)

        # if self.ucs[img_path]: # if xml set
        #     _, img_name = os.path.split(list(self.ucs[img_path])[0])
        #     self.lbl_xml_name.config(text=img_name)

        # self.master.refresh_frames(self.ucs, current_image_path=self.images[image_number])

    # def open_xml(self, img_path):
    def open_xml(self):

        img_path = self.state.get_curr_img_path()
        img_dir, _ = os.path.split(img_path)

        xml_file_path = filedialog.askopenfilename(initialdir=img_dir, title="Select XML", filetypes=(("xml files", "*.xml"),
                                                                                                      ("all files", "*.*")))
        if not xml_file_path:
            return

        self.state.add_xml_path(xml_file_path)

        # self.ucs[img_path][xml_file_path] = {}

        _, xml_name = os.path.split(xml_file_path)
        self.lbl_xml_name.config(text=xml_name)

        use_cases = self.find_use_cases(xml_file_path)

        self.state.add_use_cases(use_cases)
        # for use_case in use_cases:
        #     self.state.add
        #     self.ucs[img_path][xml_file_path][use_case] = []
        # self.ucs[img_path][xml_file_path] = use_cases

        # print("ucs", self.ucs)

    def find_use_cases(self, xml_file_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        # print(root.tag, root.attrib)

        uc_xml_elems = []
        # uc_xml_elems = root.findall(".//MasterView/UseCase")  # visual paradigm 'Xml_structure': 'simple'
        uc_xml_elems.extend(root.findall(".//UseCase"))  # visual paradigm 'Xml_structure': 'simple'
        uc_xml_elems.extend(root.findall(".//Model[@modelType='UseCase']"))  # visual paradigm 'Xml_structure': 'traditional' (old)

        # print("uc_xml_elems", uc_xml_elems)
        use_cases = []
        for elem in uc_xml_elems:
            if 'Name' in elem.attrib:
                # print('Name', elem.tag, elem.attrib['Name'])
                use_cases.append(elem.attrib['Name'])
            if 'name' in elem.attrib:
                # print('name', elem.tag, elem.attrib['name'])
                use_cases.append(elem.attrib['name'])

        use_cases = list(set(use_cases))  # remove duplicates

        return use_cases


