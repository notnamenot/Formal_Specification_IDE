IMG_PATH = "img_path"
XML_PATH = "xml_path"
USE_CASES = "use_cases"
NAME = "name"
STEPS = "steps"
SEQ = "seq"
SELECTED_WORDS = "selected_words"
TEXT = "text"
CONNECTIONS = "connections"

SEQUENCE = "Sequence"
BRANCH = "Branch"
BRANCHRE = "BranchRe"
CONCUR = "Concur"
CONCURRE = "ConcurRe"

from collections import defaultdict


class State:
    def __init__(self):
        self.all_uc_diagrams = []
        self.curr_uc_diagram = {}
        self.curr_uc = {}   # kliknięty scenariusz

    def add_uc_diagram(self, img_path):  # and set_curr_uc_diagram
        self.curr_uc_diagram = {IMG_PATH: img_path, XML_PATH: "", USE_CASES: []}
        self.all_uc_diagrams.append(self.curr_uc_diagram)
        self.curr_uc = {}

    def set_xml_path(self, xml_path):
        self.curr_uc_diagram[XML_PATH] = xml_path

    def get_all_uc_diagrams_cnt(self):
        return len(self.all_uc_diagrams)

    def set_curr_uc_diagram(self, idx):
        self.curr_uc_diagram = self.all_uc_diagrams[idx]
        self.curr_uc = {}

    def delete_curr_uc_diagram(self):
        i = self.get_curr_uc_diagram_seq()
        self.all_uc_diagrams.pop(i)
        if self.get_all_uc_diagrams_cnt() > 0:
            self.curr_uc_diagram = self.all_uc_diagrams[0]
        else:
            self.curr_uc_diagram = {}
        self.curr_uc = {}

    def change_curr_uc_diagram(self, img_path):
        for i, diagram in enumerate(self.all_uc_diagrams):
            if diagram[IMG_PATH] == img_path:
                self.set_curr_uc_diagram(i)
                break
        # self.curr_uc = {}

    def get_curr_uc_diagram_seq(self):  # ew trzymać w jsonie numerek
        for i, diagram in enumerate(self.all_uc_diagrams):
            if diagram[IMG_PATH] == self.curr_uc_diagram[IMG_PATH]:
                return i
        return -1  # all diagrams deleted

    def get_curr_img_path(self):
        return self.curr_uc_diagram[IMG_PATH]

    def get_curr_xml_path(self):
        return self.curr_uc_diagram[XML_PATH]

    def set_curr_uc(self, uc_name):
        for use_case in self.curr_uc_diagram[USE_CASES]:
            if use_case[NAME] == uc_name:
                self.curr_uc = use_case
                break

    def add_use_cases(self, use_cases):
        for use_case_name in use_cases:
            self.curr_uc_diagram[USE_CASES].append({NAME: use_case_name,
                                                    STEPS: [],
                                                    CONNECTIONS: {SEQUENCE: defaultdict(set), # set a nie list żeby były unikalne wartości
                                                                  BRANCH: defaultdict(set),
                                                                  BRANCHRE: defaultdict(set),
                                                                  CONCUR: defaultdict(set),
                                                                  CONCURRE: defaultdict(set)}})

    def add_step(self, step_text):
        self.curr_uc[STEPS].append({SEQ: len(self.curr_uc[STEPS])+1, TEXT: step_text, SELECTED_WORDS: []})

    def delete_step(self, seq):
        self.curr_uc[STEPS].pop(seq-1)  # -1 bo seq numerujemy od 1, a lista leci od 0
        # renumerate
        for i, step in enumerate(self.curr_uc[STEPS]):
            step[SEQ] = i+1

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

    def add_selected_word(self, step_id, word):
        for step in self.curr_uc[STEPS]:
            if step[SEQ] == step_id:
                step[SELECTED_WORDS].append(word)

    def remove_selected_word(self, step_id, word):
        for step in self.curr_uc[STEPS]:
            if step[SEQ] == step_id:
                step[SELECTED_WORDS].remove(word)



# [
# 	{
# 		"img_path":  "path_to_img",
# 		"xml_path":  "path_to_xml",
# 		"use_cases":
# 					[
# 						{
# 							"name":  "Display account balance",
# 							"steps":
# 									[
# 										{
# 											"seq": 1,
# 											"text": "System displays welcome screen",
# 											"selected_words": ["displays"]
# 										},
# 										{
# 											"seq": 2,
# 											"text": "User inserts Card",
# 											"selected_words": ["inserts"]
# 										},
# 										...
# 									],
#                         "connections":
#                                     {
#                                         "Sequence":
#                                             {
#                                                 "selected_word2": ["selected_word3"],
#                                                 "selected_word5": ["selected_word6"]
#                                             },
#                                         "Branch":  # OR - potrzebne warunki
#                                             {
#                                                 "selected_word1": ["selected_word2", "selcted_word5"]  # from: [to1, to2]
#                                             },
#                                         "BranchRe":
#                                             {
#                                                 "selected_word7": ["selected_word3", "selcted_word6"]  # to: [from1, from2]
#                                             },
#                                         "Concur": {...},
#                                         "ConcurRe": {...}
#                                     }
# 						},
# 						...
# 					]
# 	},
# 	...
# ]
