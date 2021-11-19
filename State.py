IMG_PATH = "img_path"
XML_PATH = "xml_path"
USE_CASES = "use_cases"

class State:
    def __init__(self):
        self.all_uc_diagrams = []
        self.curr_uc_diagram = {}
        # self.curr_num = -1

    def add_uc_diagram(self, img_path):
        self.curr_uc_diagram = {IMG_PATH: img_path, XML_PATH: "", USE_CASES: []}
        self.all_uc_diagrams.append(self.curr_uc_diagram)

    def set_xml_path(self, xml_path):
        self.curr_uc_diagram[XML_PATH] = xml_path

    def get_all_uc_diagrams_number(self):
        return len(self.all_uc_diagrams)

    def change_curr_uc_diagram(self, idx):
        self.curr_uc_diagram = self.all_uc_diagrams[idx]

    def set_curr_uc_diagram(self, img_path):
        for diagram in self.all_uc_diagrams:
            if diagram[IMG_PATH] == img_path:
                self.curr_uc_diagram = diagram
                break

    def get_curr_uc_diagram_seq(self):  # ew trzymać w jsonie numerek
        for i, diagram in enumerate(self.all_uc_diagrams):
            if diagram[IMG_PATH] == self.curr_uc_diagram[IMG_PATH]:
                return i

    def get_curr_img_path(self):
        return self.curr_uc_diagram[IMG_PATH]

    def get_curr_xml_path(self):
        return self.curr_uc_diagram[XML_PATH]

    def add_use_cases(self, use_cases):
        for use_case_name in use_cases:
            self.curr_uc_diagram[USE_CASES].append({"name": use_case_name, "steps": []})

        print("self.curr_uc_diagram[USE_CASES]", self.curr_uc_diagram[USE_CASES])
        print(self.all_uc_diagrams)

    def contains_img(self, img_path):
        for diagram in self.all_uc_diagrams:
            if diagram[IMG_PATH] == img_path:
                print("file already exists")
                return True
        return False

    def contains_img_xml(self, img_path):
        contains_img = False
        contains_xml = False
        for diagram in self.all_uc_diagrams:
            if diagram[IMG_PATH] == img_path:
                print("file already exists")
                contains_img = True
                if diagram[XML_PATH]:
                    contains_xml = True
                break
        return contains_img, contains_xml

#
# [
# 	{
# 		"img_path":  "path_to_img1",
# 		"xml_path":  "path_to_xml1",
# 		"use_cases":
# 					[
# 						{
# 							"name":  "name_of_uc1_1",
# 							"steps": [ "step1_text", "step2_text", "step3_text" ]
# 						},
# 						{
# 							"name":  "name_of_uc2_1",
# 							"steps": [ "step1_text", "step2_text", "step3_text", "step4_text" ]
# 						}
# 					]
# 	},
# 	{
# 		"img_path":  "path_to_img2",
# 		"xml_path":  "path_to_xml2",
# 		"use_cases":
# 					[
# 						{
# 							"name":  "name_of_uc1_2",
# 							"steps": [ "step1_text", "step2_text", "step3_text" ]
# 						},
# 						{
# 							"name":  "name_of_uc2_2",
# 							"steps": [ "step1_text", "step2_text" ]
# 						}
# 					]
# 	}
# ]