import GeneratorFormulLogicznych.predefinedSetEntry as setEntry
import json
import os

from GeneratorFormulLogicznych.LogicType import LogicType


class PatternPropertySet:
    def __init__(self):
        self.patterns_FOL = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '\pattern_rules_FOL.json'))    # First Order Logic
        #print(self.patterns_FOL)
        #print(self.patterns_FOL['Seq']['number of args'])
        #print(self.patterns_FOL['Seq']['rules'])
        self.setEntries_FOL = [setEntry.PredefinedSetEntry(pattern,
                                                           self.patterns_FOL[pattern]['number of args'],
                                                           self.patterns_FOL[pattern]['rules'])
                               for pattern in self.patterns_FOL]

        self.patterns_LTL = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '\pattern_rules_LTL.json'))    # First Order Logic
        self.setEntries_LTL = [setEntry.PredefinedSetEntry(pattern,
                                                           self.patterns_FOL[pattern]['number of args'],
                                                           self.patterns_FOL[pattern]['rules'])
                               for pattern in self.patterns_LTL]

    """                
            setEntry.PredefinedSetEntry("Seq", 2, ["arg0", "arg1", "Exist(arg0)", "ForAll(arg0 => Exist(arg1))",
                                                   "ForAll(~(arg0 ^ arg1))"]),
            setEntry.PredefinedSetEntry("Branch", 3, ["arg0", "arg1 | arg2", "Exist(arg0)",
                                                      "ForAll(arg0 => (Exist(arg1) ^ ~Exist(arg2) | (~Exist(arg1) ^ Exist(arg2)))",
                                                      "ForAll(arg0 => Exist(arg1))", "ForAll(arg0 => Exist(arg2))",
                                                      "ForAll(~(arg0 ^ arg1))", "ForAll(~(arg0 ^ arg2))"]),
            setEntry.PredefinedSetEntry("BranchRE", 3, [
                "arg0 | arg1", "arg2", "(Exist(arg0) ^ ~Exist(arg1)) | (~Exist(arg0) ^ Exist(arg1))",
                "ForAll(arg0 | arg1 => Exist(arg2))", "ForAll(~(arg0 ^ arg2))", "ForAll(~(arg1 ^ arg2))"
            ]),
            setEntry.PredefinedSetEntry("Concur", 3, [
                "arg0", "arg1 | arg2", "Exist(arg0)", "ForAll(arg0 => Exist(arg1) ^ Exist(arg2))",
                "ForAll(~(arg0 ^ arg1))", "ForAll(~(arg0 ^ arg2))"
            ]),
            setEntry.PredefinedSetEntry("ConcurRE", 3, [
                "arg0 | arg1", "arg2", "Exist(arg0)", "Exist(arg1)", "ForAll(arg0 => Exist(arg2))",
                "ForAll(arg1 => Exist(arg2))", "ForAll(~(arg0 ^ arg2))", "ForAll(~(arg1 ^ arg2))"
            ])
        ]
    """

    def FindByIdentifier(self, identifier, logic_type):
        identifier = identifier.strip()
        searchedEntry = None
        if logic_type == LogicType.FOL:
            for entry in self.setEntries_FOL:
                if entry.identifier.lower() == identifier.lower():
                    searchedEntry = entry
                    break
        elif logic_type == LogicType.LTL:
            for entry in self.setEntries_LTL:
                if entry.identifier.lower() == identifier.lower():
                    searchedEntry = entry
                    break
        return searchedEntry
