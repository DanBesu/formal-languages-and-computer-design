class Node:
    def __init__(self, value):
        self.father = -1
        self.sibling = -1
        self.production = -1
        self.value = value

    def __str__(self):
        return str(self.value) + "  " + str(self.father) + "  " + str(self.sibling)
