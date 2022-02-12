from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import string
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from Helpers.State import NAME, INCLUDE, EXTEND

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
        self.frame_import_UC.columnconfigure(4, weight=1)  # button delete

        self.btn_import = Button(self.frame_import_UC, text="Import files", command=self.import_clicked)
        self.btn_import.grid(row=0, column=0, rowspan=2, sticky=W, padx=(5,5))

        # self.btn_import_xml = Button(self.frame_import_UC, text="Import xml", command=self.open_xml)

        self.btn_prev = Button(self.frame_import_UC, text="<", state=DISABLED, command=self.prev_uc_diagram_clicked)
        self.btn_prev.grid(row=0, column=1, rowspan=2, sticky=NS, padx=(5, 5))

        self.lbl_img_name = Label(self.frame_import_UC, text="<img_file_name>")
        self.lbl_img_name.grid(row=0, column=2)

        self.lbl_xml_name = Label(self.frame_import_UC, text="<xml_file_name>")
        self.lbl_xml_name.grid(row=1, column=2)

        self.btn_next = Button(self.frame_import_UC, text=">", state=DISABLED, command=self.next_uc_diagram_clicked)
        self.btn_next.grid(row=0, column=3, rowspan=2, sticky=NS, padx=(5, 5))

        self.btn_delete = Button(self.frame_import_UC, text="Delete", state=DISABLED, command=self.delete_uc_diagram_clicked)
        self.btn_delete.grid(row=0, column=4, rowspan=2, sticky=NS, padx=(5, 5))

        # img = ImageTk.PhotoImage(Image.open("uc_place_holder.png"))
        # self.panel = Label(self, image=img)
        self.panel = Label(self)
        self.panel.pack()

    def import_clicked(self):
        img_path = filedialog.askopenfilename(initialdir=".", title="Select image", filetypes=(("image files", "*.png"),
                                                                                               ("image files", "*.jpg"),
                                                                                               ("image files", "*.jpeg"),
                                                                                               ("all files", "*.*")))
        if not img_path:  # dialog canceled
            return

        contains_img, contains_xml = self.state.contains_img_xml(img_path)

        if contains_img and not contains_xml:
            self.state.change_curr_uc_diagram(img_path)
            self.open_xml()
        elif contains_img:
            self.state.change_curr_uc_diagram(img_path)
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
        # print(root.tag, root.attrib, root.nsmap)
        namespaces = root.nsmap

        uc_matches, ext_matches, inc_matches = self.gather_rules(namespaces)


        ####### USE CASES ########
        uc_xml_elems = []
        for match in uc_matches:
            uc_xml_elems.extend(root.findall(match, namespaces=namespaces))

        # for elem in root:
        #     print(elem.tag, elem.attrib)

        use_cases = {}
        for elem in uc_xml_elems:
            # print(elem.tag, elem.attrib, elem.text)
            id = ''
            for ns_abbr, ns_url in namespaces.items():
                attr_id = f'{{{ns_url}}}id'
                if attr_id in elem.attrib:
                    id = elem.attrib[attr_id]
                    break
            if not id:
                if 'Id' in elem.attrib:
                    id = elem.attrib['Id']
                else:
                    parent = elem.getparent()
                    if 'xmi.id' in parent.attrib:       # EnterpriseArchitect XMI 1.0 UML 1.3
                        id = parent.attrib['xmi.id']

            # if '{http://schema.omg.org/spec/XMI/2.1}id' in elem.attrib:
            #     id = elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id']
            # elif 'Id' in elem.attrib:
            #     id = elem.attrib['Id']
            # elif '{http://www.omg.org/spec/XMI/20131001}id' in elem.attrib:
            #     id = elem.attrib['{http://www.omg.org/spec/XMI/20131001}id']
            # elif '{http://www.omg.org/spec/XMI/20110701}id' in elem.attrib:
            #     id = elem.attrib['{http://www.omg.org/spec/XMI/20110701}id']

            if 'Name' in elem.attrib:
                use_cases[id] = elem.attrib['Name']
            elif 'name' in elem.attrib:
                use_cases[id] = elem.attrib['name']
            elif elem.tag == 'Foundation.Core.ModelElement.name':
                use_cases[id] = elem.text

        use_cases_list = list(set(use_cases.values()))  # remove duplicates


        ####### EXTEND ########
        ext_xml_elems = []
        for match in ext_matches:
            ext_xml_elems.extend(root.findall(match, namespaces=namespaces))

        print("EXT", ext_xml_elems)
        extend = {}
        cnt = 1
        for elem in ext_xml_elems:
            # print(elem.tag, elem.attrib, elem.text)
            extend["Ext" + str(cnt)] = {}
            if 'extension' in elem.attrib:
                extend["Ext" + str(cnt)]["From"] = use_cases[elem.attrib['extension']]
                extend["Ext" + str(cnt)]["To"] = use_cases[elem.attrib['extendedCase']]
            elif 'extendedCase' in elem.attrib:
                parent = use_cases[elem.find('...').attrib['{http://www.omg.org/spec/XMI/20131001}id']]
                extend["Ext" + str(cnt)]["From"] = parent
                extend["Ext" + str(cnt)]["To"] = use_cases[elem.attrib['extendedCase']]
            elif 'From' in elem.attrib:
                extend["Ext" + str(cnt)]["From"] = use_cases[elem.attrib['To']]
                extend["Ext" + str(cnt)]["To"] = use_cases[elem.attrib['From']]

            cnt += 1


        ####### INCLUDE ########
        inc_xml_elems = []
        for match in inc_matches:
            inc_xml_elems.extend(root.findall(match, namespaces=namespaces))

        include = {}
        cnt = 1
        for elem in inc_xml_elems:
            # print(elem.tag, elem.attrib, elem.text)
            include["Inc" + str(cnt)] = {}
            if 'includingCase' in elem.attrib:
                include["Inc" + str(cnt)]["From"] = use_cases[elem.attrib['includingCase']]
                include["Inc" + str(cnt)]["To"] = use_cases[elem.attrib['addition']]
            elif 'addition' in elem.attrib:
                parent = use_cases[elem.find('...').attrib['{http://www.omg.org/spec/XMI/20131001}id']]
                include["Inc" + str(cnt)]["From"] = parent
                include["Inc" + str(cnt)]["To"] = use_cases[elem.attrib['addition']]
            elif 'From' in elem.attrib:
                include["Inc" + str(cnt)]["From"] = use_cases[elem.attrib['From']]
                include["Inc" + str(cnt)]["To"] = use_cases[elem.attrib['To']]

            cnt += 1

        print(extend)
        print(include)

        use_cases = self.match_include_extend(use_cases_list, include, extend)

        return use_cases

    def gather_rules(self, namespaces):
        uc_matches = []
        ext_matches = []
        inc_matches = []
        uc_matches.append(".//UseCase[@Abstract='false']")     # visual paradigm 'Xml_structure': 'simple'
        uc_matches.append(".//Model[@modelType='UseCase']")    # visual paradigm 'Xml_structure': 'traditional'
        uc_matches.append(".//UMLUseCase")                     # Sinvas
        uc_matches.append(".//Behavioral_Elements.Use_Cases.UseCase/Foundation.Core.ModelElement.name")     # EnterpriseArchitect XMI 1.0 UML 1.3

        ext_matches.append(".//Extend[@BacklogActivityId='0']")
        inc_matches.append(".//Include[@BacklogActivityId='0']")

        if "xmi" in namespaces:
            uc_matches.append(".//packagedElement[@xmi:type='uml:UseCase']")   # Papyrus {'xmi': 'http://www.omg.org/spec/XMI/20131001'}
                                                                            # EnterpriseArchitect xmi 2.1 >= 2.5.1, uml 2.1 >= 2.5.1 {'xmi': 'http://schema.omg.org/spec/XMI/2.1'}
            ext_matches.append(".//extend[@xmi:type='uml:Extend']")
            inc_matches.append(".//include[@xmi:type='uml:Include']")

        if "xsi" in namespaces:
            uc_matches.append(".//packagedElement[@xsi:type='uml:UseCase']")   # GenMyModel {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
            ext_matches.append(".//extend")
            inc_matches.append(".//include")

        if "UML" in namespaces:
            uc_matches.append(".//UML:UseCase")                # EnterpriseArchitect XMI 1.1 UML 1.3 {'UML': 'omg.org/UML1.3'},
                                                            # EnterpriseArchitect XMI 1.2 UML 1.4 {'UML': 'org.omg.xmi.namespace.UML'}
        return uc_matches, ext_matches, inc_matches

    def match_include_extend(self, use_cases_list, include, extend):

        def get_uc_id_by_name(name):
            for id_, uc_dict in use_cases.items():
                if uc_dict[NAME] == name:
                    return id_

        def get_uc_name_snaka_case(name):
            for _, uc_dict in use_cases.items():
                if uc_dict[NAME] == name:
                    return name.replace(" ", "_").lower()

        # for ids
        # alphabet_list = list(string.ascii_lowercase)
        use_cases = {}
        # i = 0

        use_cases_list.sort()
        for uc_name in use_cases_list:
            # id_ = alphabet_list[i]
            id_ = uc_name.replace(" ", "_").lower()
            use_cases[id_] = {NAME: uc_name, INCLUDE: [], EXTEND: []}
            # i += 1

        for id_, uc_dict in use_cases.items():
            for _, from_to_dict in include.items():
                if from_to_dict['From'] == uc_dict[NAME]:
                    uc_dict[INCLUDE].append(get_uc_id_by_name(from_to_dict['To']))
                    # uc_dict[INCLUDE].append(get_uc_name_snaka_case(from_to_dict['To']))
            for _, from_to_dict in extend.items():
                if from_to_dict['From'] == uc_dict[NAME]:
                    uc_dict[EXTEND].append(get_uc_id_by_name(from_to_dict['To']))
                    # uc_dict[EXTEND].append(get_uc_name_snaka_case(from_to_dict['To']))

        return use_cases

    def prev_uc_diagram_clicked(self):
        self.state.set_curr_uc_diagram(self.state.get_curr_uc_diagram_seq() - 1)
        self.reload()

    def next_uc_diagram_clicked(self):
        self.state.set_curr_uc_diagram(self.state.get_curr_uc_diagram_seq() + 1)
        self.reload()

    def delete_uc_diagram_clicked(self):
        self.state.delete_curr_uc_diagram()
        self.reload()

    def reload(self):
        self.set_buttons_state()

        if not self.state.all_uc_diagrams:
            self.lbl_img_name.config(text="<img_file_name>")
            self.lbl_xml_name.config(text="<xml_file_name>")
            self.panel.configure(image="")
        else:
            img_path = self.state.get_curr_img_path()
            _, img_name = os.path.split(img_path)
            self.lbl_img_name.config(text=img_name)

            xml_path = self.state.get_curr_xml_path()
            _, xml_name = os.path.split(xml_path)
            self.lbl_xml_name.config(text=xml_name)

            self.set_uc_diagram_img(img_path)

        self.master.on_uc_diagram_changed()
        print("uc added:\n", self.state.all_uc_diagrams)

    def set_buttons_state(self):
        curr_uc_diagram_seq = self.state.get_curr_uc_diagram_seq()
        all_uc_diagrams_cnt = self.state.get_all_uc_diagrams_cnt()

        if curr_uc_diagram_seq <= 0:
            self.btn_prev.configure(state=DISABLED)
        else:
            self.btn_prev.configure(state=NORMAL)
        if curr_uc_diagram_seq == all_uc_diagrams_cnt-1:
            self.btn_next.configure(state=DISABLED)
        else:
            self.btn_next.configure(state=NORMAL)
        if all_uc_diagrams_cnt > 0:
            self.btn_delete.configure(state=NORMAL)
        else:
            self.btn_delete.configure(state=DISABLED)

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



