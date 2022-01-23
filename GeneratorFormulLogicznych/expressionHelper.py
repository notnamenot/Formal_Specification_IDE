# import patternPropertySet as patternPropertySet
import GeneratorFormulLogicznych.patternPropertySet as patternPropertySet
import re
# from GeneratorFormulLogicznych.expressionHelper import patternPropertySet

patternPropertySet = patternPropertySet.PatternPropertySet()


def LabelExpression(expression):
    labelNumber = 0
    result = []
    for c in expression:
        if (c == '('):
            labelNumber += 1
            result.append("(" + str(labelNumber) + "]")
        elif (c == ')'):
            result.append("[" + str(labelNumber) + ")")
            labelNumber -= 1
        else:
            result.append(c)
    return ''.join(result)


def GetExpressionParam(expression, paramNumber):
    args = expression[expression.index("("): expression.index(")")].split(",")
    if (paramNumber < len(args)):
        return args[paramNumber]
    else:
        return None


def GetMaxedLabelPattern(labeledExpression):
    labeledExpression = re.sub("[^0-9]+", " ", labeledExpression)
    labels = labeledExpression.strip().split(" ")
    maxLabel = -1
    for label in labels:
        castedLabel = int(label)
        maxLabel = max(castedLabel, maxLabel)

    return maxLabel


def GetPat(labeledExpression, l, c, logic_type):
    occurenceIndex = 0
    while True:
        if (occurenceIndex == 0):
            occurenceIndex = labeledExpression.find(str(l) + "]")
        else:
            oldOccurenceIndex = occurenceIndex
            subst = labeledExpression[oldOccurenceIndex + 1:]
            occurenceIndex = subst.find(str(l) + "]") + oldOccurenceIndex + 1
            if (oldOccurenceIndex == occurenceIndex):
                return None
        c -= 1
        if c <= 0:
            break
    args = labeledExpression[occurenceIndex + len(str(l) + "]"): labeledExpression.find("[" + str(l), occurenceIndex)]
    beginExpressionIndex = 0
    i = occurenceIndex
    while i >= 0:
        if (labeledExpression[i] == ']' or labeledExpression[i] == ','):
            beginExpressionIndex = i
            break
        i -= 1

    expressionName = ""
    if (beginExpressionIndex != 0):
        expressionName = labeledExpression[beginExpressionIndex + 1: occurenceIndex - 1]
    else:
        expressionName = labeledExpression[0: occurenceIndex - 1]

    result = patternPropertySet.FindByIdentifier(expressionName.strip(), logic_type)
    if (result != None):
        arguments = ExtractArgumentsFromFunction(args)
        result.PassArguments(arguments)
    return result


def ExtractArgumentsFromFunction(args):
    arguments = []
    i = 0
    while i < len(args):
        if (args[i].islower()):
            arguments.append(args[i])
        else:
            if args[i] == ',':
                i += 1
                continue
            else:
                shouldStop = True
                counter = 99
                stCounter = 0
                j = i
                while (shouldStop):
                    stCounter += 1
                    if (args[j] == '('):
                        if (counter == 99):
                            counter = 1
                        else:
                            counter += 1
                    elif (args[j] == ')'):
                        counter -= 1
                        if (counter == 0):
                            arguments.append(args[i: i + stCounter])
                            i += stCounter
                            shouldStop = False
                            break
                    j += 1
        i += 1
    return arguments


def IsAtomic(argument):
    return not ("=>" in argument or "|" in argument or "^" in argument or "]" in argument)


def ExtractFromLabeled(labeled):
    x = labeled.find("]")
    argsLabeled = ExtractArgumentsFromFunction(labeled[x + 1: len(labeled) - 3])
    return argsLabeled


def GetPredefinedSetEntryByExpression(expression, logic_type):
    identifier = expression[:expression.find("(")]
    result = patternPropertySet.FindByIdentifier(identifier, logic_type)
    if (result != None):
        args = ExtractFromLabeled(expression)
        result.PassArguments(args)
    return result
