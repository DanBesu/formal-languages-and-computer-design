class Grammar:
    def __init__(self):
        self._N = [] # non terminals
        self._E = [] # alphabet
        self._P = {} # productions
        self._S = [] # starting symbol

    def getTerminals(self):
        return self._E

    def getNonTerminals(self):
        return self._N

    def getStartingSymbol(self):
        return self._S

    def printNonTerminals(self):
        print(self._N)

    def printStartingSymbol(self):
        print(self._S)

    def printAlphabet(self):
        print(self._E)

    def printProductions(self):
        print(self._P)

    def readFromFile(self, filename):
        """
        Reads a grammar from a file
        :param filename: given filename
        """
        with open(filename, 'r') as file:
            # read the non-terminals
            self._N = Grammar.parseLine(file.readline())
            # read the alphabet
            self._E = Grammar.parseLine(file.readline())
            # read the starting symbol
            self._S = file.readline().split('=')[1].strip()
            # read the production rules
            file.readline()
            rules = []
            for line in file:
                rules.append(line.strip())
            self._P = Grammar.parseRules(rules)

        if not Grammar.checkCFG(rules, self._N):
            raise Exception('Grammar is not CFG')

    @staticmethod
    def parseLine(line):
        """
        parse a line from the file that with the given structure: symbol = symbol { , symbol }
        :param line: given line from file
        :return: the list of values after equal
        """
        result = []
        after_equal = line.strip().split('=', 1)[1]
        if after_equal.strip()[-1] == ',':
            result = [',']
        result += [value.strip() for value in after_equal.split(',')]
        return result

    @staticmethod
    def parseRules(rules):
        """
        parse the list of rules of the form A -> alpha { | beta }
        :return: a dictionary that contains the set of productions
        """
        result = {}
        # start indexing the productions by 1
        index = 1
        for rule in rules:
            # split by lhs and rhs
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [value.strip() for value in rhs.split('|')]

            # for each value in rhs:
            for value in rhs:
                if lhs in result.keys():
                    # if lsh is in the dictionary we append in the list of values
                    result[lhs].append((value, index))
                else:
                    # else we add a new entry in the dictionary
                    result[lhs] = [(value, index)]
                index += 1
        return result

    @staticmethod
    def checkCFG(rules, N):
        """
        check if a grammar is a context free grammar = every lhs has the form of: A [ -> alpha ]
        :param rules: set of rules
        :param N: set of non-terminals
        :return: true | false
        """
        for rule in rules:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            count = 0
            for element in lhs.split('|'):
                element = element.strip()
                if element in N:
                    count += 1
            if count > 1:
                return False
        return True