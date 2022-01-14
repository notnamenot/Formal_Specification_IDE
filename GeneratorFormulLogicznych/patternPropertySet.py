# import predefinedSetEntry as setEntry
import GeneratorFormulLogicznych.predefinedSetEntry as setEntry

class PatternPropertySet:
    def __init__(self):
        self.setEntries = [
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

    def FindByIdentifier(self, identifier):
        identifier = identifier.strip()
        searchedEntry = None
        for entry in self.setEntries:
            if entry.identifier.lower() == identifier.lower():
                searchedEntry = entry
                break
        return searchedEntry
