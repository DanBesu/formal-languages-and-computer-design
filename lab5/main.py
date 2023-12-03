from grammar import Grammar

if __name__ == '__main__':
    if __name__ == '__main__':
        grammar = Grammar()
        grammar.readFromFile("lab5/g2.txt")
        print('Non-terminals:')
        grammar.printNonTerminals()
        print('Alphabet:')
        grammar.printAlphabet()
        print('Starting symbol: ')
        grammar.printStartingSymbol()
        print('Productions:')
        grammar.printProductions()
