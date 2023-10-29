DEFAULT_INDEX = [-1, -1]
CAPACITY = 10


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class MyHashTable:
    def __init__(self):
        self.__capacity = CAPACITY
        self.__size = 0
        self.__elements = [None] * self.__capacity
    
    def __hash_function(self, key):
        hashsum = 0
        for index, char in enumerate(key):
            hashsum = hashsum + (index + len(key)) ** ord(char)
            hashsum = hashsum % self.__capacity
        return hashsum

    def add_item(self, key, value):
        self.__size = self.__size + 1
        index = self.__hash_function(key)
        current_node = self.__elements[index]

        if current_node is None:
            self.__elements[index] = Node(key, value)
        else:
            # Collision
            # We have to iterate to the end of the linked list and add the new node
            prev_node = current_node
            while current_node is not None:
                prev_node = current_node
                current_node = current_node.next
            prev_node.next = Node(key, value)

    def find_item(self, key):
        index = self.__hash_function(key)
        current_node = self.__elements[index]
        
        while current_node is not None and current_node.key != key:
            current_node = current_node.next

        if current_node is None:
            return None
        else:
            return current_node.value

    def get_position(self, key):
        index_in_table = self.__hash_function(key)
        index_in_list = 0

        current_node = self.__elements[index_in_table]
        while current_node is not None and current_node.key != key:
            index_in_list = index_in_list + 1
            current_node = current_node.next
        
        if current_node is None:
            return DEFAULT_INDEX

        return [index_in_table, index_in_list]

    def get_string_form(self):
        string_representation = ""
        index = 0
        while index < len(self.__elements):
            string_representation = string_representation + str(index) + ": ["
            current_node = self.__elements[index]
            while current_node is not None:
                string_representation = string_representation + current_node.key + ", "
                current_node = current_node.next
            string_representation = string_representation + "]\n"
            index = index + 1
        return string_representation
