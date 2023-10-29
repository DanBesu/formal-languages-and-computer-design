from hash_table.hash_table import MyHashTable

class SymbolTable:
    def __init__(self):
        self.__elements = MyHashTable()

    def find_item(self, key):
        return self.__elements.find_item(key=key)

    def add_item(self, key, value):
        return self.__elements.add_item(key=key, value=value)

    def get_position(self, key):
        return self.__elements.get_position(key=key)
    
    def get_string_form(self):
        return self.__elements.get_string_form()
