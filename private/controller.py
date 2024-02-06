from private.menu import Menu
from private.tree import ExpressionTokenizer, ParseTreeBuilder, BinaryTreeEvaluator
from private.utils import InputHandler, DictionaryHandler, MergeSort, Plotter
from private.datastructure import Graph
import os
import math


class Controller:
    def __init__(self):
        self.assignments = {}
        self.menu = Menu()
        self.tkn = ExpressionTokenizer()
        self.ptb = ParseTreeBuilder()
        self.bte = BinaryTreeEvaluator()
        self.ih = InputHandler()
        self.dh = DictionaryHandler()
        self.plotter = Plotter()

    ########################################################################################################################################################
    # 1.)
    def assign(self):
        assignment_input = input(
            "Enter the assignment stament you want to add/modify:\nFor example, a=(1+2)\n| "
        )
        while True:
            if assignment_input.lower() == "q" or assignment_input.lower() == "exit":
                break
            else:
                is_valid, error_message = self.ih.is_valid_assignment(assignment_input)
                if is_valid:
                    self.assignments = self.dh.add_to_dict(assignment_input, self.assignments)
                else:
                    print(f"Invalid Assignment: {error_message}")
            print()
            assignment_input = input(
                "Enter another assignment statement or type 'q' to quit.\n| "
            )
        print("\n")
        self.menu.select_option()

    ########################################################################################################################################################
    # 2.)
    def display(self):

        print(f"CURRENT ASSIGNMENTS:\n{'*'*20}")
        self.bte.reset_edges()

        for key, item in self.assignments.items():
            if item is not None:
                result = self.bte.evaluate(self.ptb.build_tree(key), self.assignments)
                print(f"{key} = {item} => {result}")
        circular_dependency = 0
        
        for key, item in self.assignments.items():
            if item is not None:
                circular_dependency = self.bte.check_cd(self.ptb.build_tree(key), self.assignments)

        if circular_dependency == 0:
            print()
        elif len(circular_dependency) != 0:
            print(f"\nCircular dependency detected involving {circular_dependency}\n")

        self.menu.select_option()

    ########################################################################################################################################################
    # 3.)
    def evaluate(self):
        variable_input = input("Enter the variable whose expression you want to see in in-order:\nFor example, if you have an assignment a=(1+2), just type 'a'\n| ")
        if variable_input in self.assignments:
            expression = self.assignments[variable_input]
            try:
                print()
                # parse the expression into a binary tree
                expression_tree = self.ptb.build_tree(expression)
                # perform an in-order traversal to display the three
                print("Expression Tree:")
                expression_tree.printInorder()
                result = self.bte.evaluate(expression_tree, self.assignments, parent_var=variable_input)
                print(f"\nValue for variable '{variable_input}' is: {result if result is not None else 'None'}\n")
                print()
            except Exception as e:
                print(f"Error in processing the expression for '{variable_input}': {str(e)}\n")
        else:
            print("Variable not found in the current assignments")
        self.menu.select_option()

            

    ########################################################################################################################################################
    # 4.)
    def read_file(self):
        file = input("Please enter input file: ")
        print("\n")
        try:
            with open(file, 'r') as file:
                for line in file:
                    line = line.strip()
                    is_valid, error_message = self.ih.is_valid_assignment(line)
                    if is_valid:
                        self.assignments = self.dh.add_to_dict(line, self.assignments)
                    else:
                        print(f"{error_message}\nline: {line}")
            print(f"CURRENT ASSIGNMENTS:\n{'*'*20}")
            self.bte.reset_edges()

            for key, item in self.assignments.items():
                if item is not None:
                    result = self.bte.evaluate(self.ptb.build_tree(key), self.assignments)
                    print(f"{key} = {item} => {result}")
            circular_dependency = 0
            
            for key, item in self.assignments.items():
                if item is not None:
                    circular_dependency = self.bte.check_cd(self.ptb.build_tree(key), self.assignments)

            if circular_dependency == 0:
                print()
            elif len(circular_dependency) != 0:
                print(f"\nCircular dependency detected involving {circular_dependency}\n")
        except FileNotFoundError:
            print(f"\nFile not found: {file}")
        print("\n")
        self.menu.select_option()

    ########################################################################################################################################################
    # 5.)
    def sort_file(self):
        result_list = []
        for key, item in self.assignments.items():
            if item is not None:
                result = self.bte.evaluate(self.ptb.build_tree(key), self.assignments)
                result_list.append((key, item, result))
        mergesort = MergeSort(result_list)
        sorted_list = mergesort.items
        if len(sorted_list) == 0:
            print("No item to sort.")
            self.menu.select_option()
        else:
            file = input("Please enter output file: ")
            with open(file, "w") as file:
                prev_result = None
                for result_tuple in sorted_list:
                    key, item, result = result_tuple
                    if result != prev_result:
                        if prev_result is not None:
                            file.write("\n")  # Separate entries with the same result
                        file.write(f"*** Statements with value => {result}\n")
                    file.write(f"{key} = {item}\n")
                    prev_result = result
            print("\n")
            self.menu.select_option()

    ########################################################################################################################################################
    # 6.)
    def option1(self):
        if len(self.assignments) == 0 and len(self.save) == 0:
            print("\nNothing to delete/load or save.\n")
        else:
            dl_input = input("Do you want to load the last save, save or delete (l/s/d): ")
            if dl_input.lower() != "d" and dl_input.lower() != "l" and dl_input.lower() != "s":
                print("\nInvalid input") 
            elif dl_input == 'd':
                save = input("\nDo you want to save the current assignments temporarily (y/n): ")
                while save.lower() != 'y' and save.lower() != 'n':
                    save = input("\nDo you want to save the current assignments temporarily (y/n): ")
                if save == 'y':
                    self.save = self.assignments
                    self.assignments = {}
                    print("\nAssignments cleared")
                else:
                    self.assignments = {}
                    print("\nAssignments cleared")
            elif dl_input == 'l':
                self.assignments = self.save
                print("\nLoaded last saved assignments\n")
            elif dl_input == 's':
                self.save = self.assignments
                print("\nSaved assignments\n")
        
        self.menu.select_option()

    ########################################################################################################################################################
    # 7.)
    def option2(self):
        pass

    def option3(self):
        while True:
            user_formula = input("Please enter a formula example(x**2 + 2*x + 1):\ny = ")
            if user_formula.lower() in ['q', 'exit']:
                break
            try:
                self.plotter.plot_function(user_formula, xmin=-10, xmax=10, width=100, height=30, x_range=10)
                self.menu.select_option()
            except:
                print(f"\nInput Error: Try Again or Quit('q')\n")
        self.menu.select_option()
    def option4(self):
        pass


########################################################################################################################################################
# 7.)
