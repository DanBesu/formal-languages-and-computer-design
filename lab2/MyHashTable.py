class Node: 
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next_node = None

class MyHashtable:
    def __init__(self):
        self.__size = 0
        self.__capacity = 100
        self.__items = [None] * 100

    def __hash_func(self, key):
        hash_sum = 0
        for i, c in enumerate(key):
            hash_sum = hash_sum + (i + len(key)) ** ord(c)
            hash_sum = hash_sum % self.__capacity
    
    def add_item(self, key, value):
        if self.find_item(key) is not None:
            return
        
        self.__size = self.__size + 1
        _hash = self.__hash_func(key)
        _node = self.__items[_hash]

        if _node is None:
          self.__items[_hash] = Node(key, value)
        else:
            previous_node = _node
            while _node is not None:
              previous_node = _node
              _node = _node.next_node
            previous_node.next_node = Node(key, value)

    def find_item(self, key):
        _hash = self.__hash_func(key)
        _node = self.__items[_hash]

        while _node is not None and _node.key != key:
            _node = _node.next_node
        
        if _node is None:
            return None
        else: 
            return _node.value
