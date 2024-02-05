from private.menu import Menu
from private.tree import ExpressionTokenizer, ParseTreeBuilder, BinaryTreeEvaluator
from private.utils import InputHandler, DictionaryHandler, MergeSort
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

    ########################################################################################################################################################
    # 1.)
    def assign(self):
        assignment_input = input(
            "Enter the assignment stament you want to add/modify:\nFor example, a=(1+2)\n| "
        )
        while True:
            if assignment_input.lower() == "q" or assignment_input.lower() == "exit":
                print()
                self.menu.select_option()
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

    ########################################################################################################################################################
    # 2.)
    def display(self):
        print(f"CURRENT ASSIGNMENTS:\n{'*'*20}")
        for key, item in self.assignments.items():
            if item is not None:
                result = self.bte.evaluate(self.ptb.build_tree(key), self.assignments)
                print(f"{key} = {item} => {result}")
        print()
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
        self.assignments = {}
        print("Assignments cleared")
        self.menu.select_option()

    ########################################################################################################################################################
    # 7.)
    def option2(self):
        pass

    def option3(self):
        pass


########################################################################################################################################################
# 7.)
