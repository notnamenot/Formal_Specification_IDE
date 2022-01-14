class PredefinedSetEntry:
    def __init__(self, identifier, argNumber, possibleOutcomes):
        self.identifier = identifier
        self.argNumber = argNumber
        self.possibleOutcomes = possibleOutcomes
        self.arguments = ["arg" + str(i) for i in range(self.argNumber)]

    def PassArguments(self, args):
        if (len(args) > self.argNumber):
            raise Exception("Wrong arg number")
        else:
            self.arguments = args

    def GetPossibleOutcomes(self):
        outcomes = self.possibleOutcomes[:]
        for i in range(len(self.possibleOutcomes)):
            for j in range(self.argNumber):
                outcomes[i] = outcomes[i].replace("arg" + str(j), self.arguments[j])
        return outcomes

    def GetExpression(self):
        return self.identifier + "(" + ','.join([str(elem) for elem in self.arguments]) + ")"
