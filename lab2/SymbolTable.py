from MyHashTable import MyHashTable

class SymbolTable:
    def __init__(self):
        self.__items = MyHashTable()

    def add_item(self, key, value):
        return self.__items.add_item(key, value)

    def find_item(self, key):
        return self.__items.find_item(key)
