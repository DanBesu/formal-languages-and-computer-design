from symbol_table import SymbolTable

symbol_table = SymbolTable()

symbol_table.add_item('a', 5)
value = symbol_table.find_item('a')
assert value == 5

found_value = symbol_table.find_item('b')
assert found_value == None

symbol_table.add_item('b', 8) 

found_b = symbol_table.find_item('b')
assert found_b == 8

print('All good!')