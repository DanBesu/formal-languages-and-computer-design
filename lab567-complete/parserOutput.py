class ParserOutput:

    def __init__(self, parser):
        self.parser = parser

    def write_parsing_tree(self):
        if self.parser.state != "e":
            self.parser.write_in_output_file("\n The Parsing Tree: ")
            self.parser.write_in_output_file("Index Information Parent Left Sibling")
            for i in range(0, len(self.parser.working_stack)):
                message = str(i) + "  " + str(self.parser.tree[i])
                self.parser.write_in_output_file(message)
