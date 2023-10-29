import os
import re
from enum import Enum
from symbol_table import SymbolTable


class ScannerConfigs(Enum):
    # Programs filepaths
    P1_FILE = "lab3/programs/p1.txt"
    P2_FILE = "lab3/programs/p2.txt"
    P3_FILE = "lab3/programs/p3.txt"
    PERR_FILE = "lab3/programs/perr.txt"
    # Symbol table and PIF filepaths
    ST_FILE_OUT = "lab3/out/ST.out"
    PIF_FILE_OUT = "lab3/out/PIF.out"


class ScannerUtilities(Enum):
    IDENTIFIER_CODE = "ID"
    CONSTANT_CODE = "CONST"
    DEFAULT_INDEX = [-1, -1]

    RESERVED_WORDS = ["declarNumar", "saZicemCa", "dacaNu", "catTimp", "introdu", "afiseaza", "declarCuvant"]
    SEPARATORS = ["\n", "\t", ":", " ", "(", ")", ",", "{", "}"]
    OPERATORS = ["+", "-", "*", "/", "%", "=", "?=", "!=", "<", "<=", ">", ">=", "?", "&&", "||", "++", "--"]
    
    NUMERIC_REGEX = "^0|[+|-]*[1-9]([0-9])*$"
    STRING_REGEX = "^\"[a-zA-Z0-9_?!#*./%+=<>;)(}{ ]*\""
    BOOLEAN_REGEX = "^(adevarat)|(fals)$"
    IDENTIFIER_REGEX = "^[a-zA-Z][a-zA-Z0-9]{0,30}"


class Scanner:
    def __init__(self):
        self.__symbol_table = SymbolTable()
        self.__is_lexically_correct_program = True
        self.__pif = []        

    @staticmethod
    def is_constant(token):
        return bool(re.match(ScannerUtilities.NUMERIC_REGEX.value, token)) or \
               bool(re.match(ScannerUtilities.STRING_REGEX.value, token)) or \
               bool(re.match(ScannerUtilities.BOOLEAN_REGEX.value, token)) 

    @staticmethod
    def is_reserved_word(token):
        return token in ScannerUtilities.RESERVED_WORDS.value

    @staticmethod
    def is_operator(token):
        return token in ScannerUtilities.OPERATORS.value

    @staticmethod
    def is_separator(token):
        return token in ScannerUtilities.SEPARATORS.value

    @staticmethod
    def is_identifier(token):
        return bool(re.match(ScannerUtilities.IDENTIFIER_REGEX.value, token))

    @staticmethod
    def __print_lexical_error(line_number, token):
        if token[-1] == '\n':
            token = token[0:-1]
        print("Lexical error -> line: " + str(line_number) + ", token: " + token)

    def __get_operator(self, line, index):
        operator = line[index] + line[index + 1]
        if self.is_operator(operator):
            return operator
        return line[index]

    def __get_string_constant(self, line, index):
        string_constant = line[index]
        index = index + 1
        done = False
        while not done and index < len(line):
            string_constant = string_constant + line[index]
            if line[index] == "\"":
                done = True
            else:
                index = index + 1

        return string_constant

    def __get_token(self, line, index):
        token = ""
        while index < len(line) and not self.is_separator(line[index]) \
            and not (line[index] == "!" or self.is_operator(line[index])) \
            and line[index] != ' ':
            token = token + line[index]
            index = index + 1
        return token

    def __tokenize(self, line):
        # Splits the given line into tokens
        tokens = []
        i = 0
        while i < len(line):
            if self.is_separator(line[i]) and line[i] != ' ':
                tokens.append(line[i])
            elif line[i] == "\"":
                string_constant = self.__get_string_constant(line, i)
                tokens.append(string_constant)
                i = i + len(string_constant) - 1
            elif line[i] == "!" or self.is_operator(line[i]):
                operator = self.__get_operator(line, i)
                tokens.append(operator)
                i = i + len(operator) - 1
            elif line[i] != ' ':
                token = self.__get_token(line, i)
                tokens.append(token)
                i = i + len(token) - 1
            i = i + 1
        return tokens

    def __check_tokens_by_line(self, token, line_number):
        if self.is_reserved_word(token) or self.is_operator(token) or self.is_separator(token):
            # verify if the token is: reserved word, operator or separator.
            # if valid the value inserted in PIF will be of format [token, DEFAULT_INDEX]
            self.__pif.append([token, ScannerUtilities.DEFAULT_INDEX.value])
        elif self.is_identifier(token) and not self.is_constant(token):
            # check if the current token is an identifier.
            # if not in the Symbol table already, add it and insert into PIF the pair [ID, position]
            sym_table_position = self.__symbol_table.get_position(token)
            if (sym_table_position == ScannerUtilities.DEFAULT_INDEX.value):
                self.__symbol_table.add_item(token, None)
                sym_table_position = self.__symbol_table.get_position(token)
            self.__pif.append([ScannerUtilities.IDENTIFIER_CODE.value, sym_table_position])
        elif self.is_constant(token):
            # check if the current token is a constant.
            # if not in the Symbol table already, add it and insert into PIF the pair [CONSTANT, position]
            sym_table_position = self.__symbol_table.get_position(token)
            if (sym_table_position == ScannerUtilities.DEFAULT_INDEX.value):
                self.__symbol_table.add_item(token, None)
                sym_table_position = self.__symbol_table.get_position(token)
            self.__pif.append([ScannerUtilities.CONSTANT_CODE.value, sym_table_position])
        else:
            # the token cannot be classified
            self.__is_lexically_correct_program = False
            self.__print_lexical_error(line_number, token)

    def scan(self, program_file_path):
        file = open(program_file_path, 'r')
        current_line_number = 1

        for line in file:
            tokens = self.__tokenize(line)
            for token in tokens:
                self.__check_tokens_by_line(token, current_line_number)                
            current_line_number = current_line_number + 1

        if self.__is_lexically_correct_program:
            print("Lexically correct.")
        else:
            print("Lexically incorrect.")

    def __get_pit_text_format(self):
        pit_text_format = ""
        for pair in self.__pif:
            code, index = pair
            if code == '\n':
                code = "new_line"
            index_str = "(" + str(index[0]) + ", " + str(index[1]) + ")"
            pit_text_format += code + index_str.rjust(30 - len(code)) + "\n"
        return pit_text_format

    def print_tables(self):
        # write the ST in the ST.out file
        st_text_format = self.__symbol_table.get_string_form()
        f = open(ScannerConfigs.ST_FILE_OUT.value, "w")
        f.write(st_text_format)

        # write the PIF in the PIF.out file
        pit_text_format = self.__get_pit_text_format()
        f = open(ScannerConfigs.PIF_FILE_OUT.value, "w")
        f.write(str(pit_text_format))

scanner = Scanner()
scanner.scan(ScannerConfigs.P2_FILE.value)
scanner.print_tables()
