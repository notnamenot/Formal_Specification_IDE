import GeneratorFormulLogicznych.expressionHelper as expressionHelper
import GeneratorFormulLogicznych.patternPropertySet as patternPropertySet


def GenerateLogicalSpecification(pattern, logic_type):
    pattern = pattern.strip()
    predefinedSet = patternPropertySet.PatternPropertySet()
    L = []
    print("Wejściowe wyrażenie to: " + pattern)
    labeledExpresssion = expressionHelper.LabelExpression(pattern)
    print("Po labelowaniu: " + labeledExpresssion)
    maxedLabelValue = expressionHelper.GetMaxedLabelPattern(labeledExpresssion)
    l = maxedLabelValue
    while (l >= 1):
        c = 1
        pat = expressionHelper.GetPat(labeledExpresssion, l, c, logic_type)
        while True:
            L2 = pat.GetPossibleOutcomes()
            L2 = L2[2:]
            for arg in pat.arguments:
                if (not (expressionHelper.IsAtomic(arg))):
                    cons = GenerateConsolidatedExpression(arg, 0,
                                                          predefinedSet, logic_type) + " | " + GenerateConsolidatedExpression(
                        arg, 1, predefinedSet, logic_type)
                    L2_cons = []
                    for outcome in L2:
                        L2_cons.append(outcome.replace(arg, cons))
                    L2 = L2_cons
            c += 1
            L.append(L2)
            pat = expressionHelper.GetPat(labeledExpresssion, l, c, logic_type)
            if (pat == None):
                break
        l -= 1
    allExpAsString = ''
    print("\nWynik: ")
    for gen in L:
        for genLogicExp in gen:
            print(genLogicExp)
            allExpAsString += genLogicExp + '\n'

    return allExpAsString


def GenerateConsolidatedExpression(pattern, type, propertySet, logic_type):
    ex = ""
    pSet = expressionHelper.GetPredefinedSetEntryByExpression(pattern, logic_type)
    possibleOutcomes = pSet.GetPossibleOutcomes()
    ini = possibleOutcomes[0]
    fin = possibleOutcomes[1]
    possibleOutcomes = possibleOutcomes[2:]
    if (type == 0):
        ex = ini

    if (type == 1):
        ex = fin

    argsToCheck = expressionHelper.ExtractFromLabeled(pattern)

    for a in argsToCheck:
        if (not (a in argsToCheck)):
            continue
        if not (expressionHelper.IsAtomic(a)):
            cons2 = GenerateConsolidatedExpression(a, type, propertySet, logic_type)
            ex = ex.replace(a, cons2)

    return ex


# GenerateLogicalSpecification("Seq(a,Branch(c,d,e))")
# input("Press Enter to end...")
