from private.menu import Menu
from private.tree import Tree
import os
import math


class Controller:
    def __init__(self):
        self.menu = Menu()
        self.tree = Tree()

########################################################################################################################################################
# 1.)
    def assign(self):
        var_dict = {}

        while True:
            user_input = input("Enter variable assignment or 'exit' to quit: ")
            
            if user_input.lower() == 'exit':
                break

            # Assuming the format is 'variable = expression'
            if '=' in user_input:
                var_name, expression = user_input.split('=', 1)
                var_name = var_name.strip()
                
                try:
                    tree = build_parse_tree(expression.strip())
                    var_dict[var_name] = evaluate(tree, var_dict)
                    print(f"{var_name} = {var_dict[var_name]}")
                except Exception as e:
                    print(f"Error evaluating expression: {e}")
            else:
                print("Invalid input format. Please use 'variable = expression' format.")

########################################################################################################################################################
# 2.)
    def display(self):
        pass


########################################################################################################################################################
# 3.)
    def evaluate(self):
        pass


########################################################################################################################################################
# 4.)
    def read_file(self):
        pass


########################################################################################################################################################
# 5.)
    def sort_file(self):
        pass


########################################################################################################################################################
# 6.)
    def option1(self):
        pass


########################################################################################################################################################
# 7.)
    def option2(self):
        pass

########################################################################################################################################################
# 7.)



    