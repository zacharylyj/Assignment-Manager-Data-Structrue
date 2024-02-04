from private.menu import Menu
from private.tree import ExpressionTokenizer, ParseTreeBuilder, BinaryTreeEvaluator
from private.utils import InputHandler, DictionaryHandler
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
            elif self.ih.is_valid_assignment(assignment_input):
                self.assignments = self.dh.add_to_dict(
                    assignment_input, self.assignments
                )
            print()
            assignment_input = input(
                "Enter another assignment statement or type 'q' to quit.\n| "
            )

    ########################################################################################################################################################
    # 2.)
    def display(self):
        print(f"CURRENT ASSIGNMENTS:\n{'*'*20}")
        print(self.assignments)
        for key, item in self.assignments.items():
            if item is not None:
                result = self.bte.evaluate(self.ptb.build_tree(key), self.assignments)
                print(f"{key} = {item} => {result}")
        print()
        self.menu.select_option()

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
