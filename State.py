
# state =

class State:
    def __init__(self):
        self.all = []
        # self.curr_img_path = ""
        self.curr_uc = {}
        # self.curr_num = -1

    def add_img_path(self, img_path):
        # self.curr_img_path = img_path
        self.curr_uc = {"img_path": img_path, "xml_path": "", "use_cases": []}
        self.all.append(self.curr_uc)

    def add_xml_path(self, xml_path):
        self.curr_uc["xml_path"] = xml_path
        print("self.curr_uc", self.curr_uc)
        print("self.all",self.all)

    def get_number_of_objects(self):
        return len(self.all)

    def change_curr_uc(self, idx):
        self.curr_uc = self.all[idx]

    def set_curr_uc(self, img_path):
        for o in self.all:
            if o["img_path"] == img_path:
                self.curr_uc = o
                break

    def get_curr_uc_num(self):
        for i, obj in enumerate(self.all):
            if obj["img_path"] == self.curr_uc["img_path"]:
                return i


    def get_curr_img_path(self):
        return self.curr_uc["img_path"]

    def get_curr_xml_path(self):
        return self.curr_uc["xml_path"]

    def add_use_cases(self, use_cases):
        for use_case_name in use_cases:
            self.curr_uc["use_cases"].append({"name": use_case_name, "steps": []})

        print("self.curr_uc[\"use_cases\"]", self.curr_uc["use_cases"])
        print(self.all)

    def contains_img(self, img_path):
        for o in self.all:
            if o["img_path"] == img_path:
                print("file already exists")
                return True
        return False

    def contains_img_xml(self, img_path):
        contains_img = False
        contains_xml = False
        for o in self.all:
            if o["img_path"] == img_path:
                print("file already exists")
                contains_img = True
                if o["xml_path"]:
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