import re
import os
from private.tree import ParseTreeBuilder, BinaryTreeEvaluator


class DictionaryHandler:
    def add_to_dict(self, assignment_input, assignments):
        key, value = assignment_input.replace(" ", "").split("=")

        assignments[key] = value
        return assignments


class InputHandler:
    def __init__(self):
        self.assignment_pattern = re.compile(
            r"^[a-zA-Z][a-zA-Z0-9]*\s*=\s*[a-zA-Z0-9+\-*/**()= ]+$"
        )
        self.dh = DictionaryHandler()
        self.ptb = ParseTreeBuilder()
        self.bte = BinaryTreeEvaluator()

    def is_valid_assignment(self, assignment_string):
        temp_assignments = {}
        temp_assignments = self.dh.add_to_dict(assignment_string, temp_assignments)
        if not assignment_string:
            print("Input Error: Assignment cannot be empty")
            return False
        elif not self.assignment_pattern.match(assignment_string):
            print("Input Error: Use of Invalid characters")
            return False
        elif "=" not in assignment_string:
            print("Input Error: Assignment must contain '='")
            return False
        elif assignment_string.count("(") != assignment_string.count(")"):
            print("Input Error: Unequal number of opening and closing parentheses")
            return False
        else:
            pattern2 = r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*(?:[a-zA-Z_][a-zA-Z0-9_]*|\d+(?:\.\d+)?)(\s*(?:\+|-|\*{1,2}|\/)\s*(?:[a-zA-Z_][a-zA-Z0-9_]*|\d+(?:\.\d+)?))*\s*$'
            if bool(re.match(pattern2, assignment_string.strip())) != True:
                print("Input Error: Invalid Expression")
                return False
            return True

    def is_valid_filename(self, filename):
        if not filename:
            print("Filename cannot be empty")
            return False

        if not os.path.basename(filename) == filename:
            print("File cannot be fun")
            return False

        if "." not in filename:
            filename += ".txt"

        return True


class EquationSorter:
    def __init__(self):
        self.eq_dict = {}
        self.dependency_graph = {}

    def _add_dependencies(self, var, sorted_eqs, seen, undefined_vars):
        if var in seen:
            raise ValueError(f"Circular dependency detected involving '{var}'")
        if var not in sorted_eqs:
            if var not in self.dependency_graph:
                undefined_vars.add(var)
                return
            seen.add(var)
            for dep in self.dependency_graph.get(var, []):
                self._add_dependencies(dep, sorted_eqs, seen, undefined_vars)
            sorted_eqs[var] = self.eq_dict[var]
            seen.remove(var)

    def sort_equations(self, equations):
        # parsing the equations to extract variables and their dependencies
        for eq in equations:
            var, expr = eq.split(" = ")
            deps = set([x for x in expr.split(" ") if x.isalpha() and x != var])
            self.eq_dict[var] = expr
            self.dependency_graph[var] = deps

        # sorting the equations based on dependencies
        sorted_eqs = {}
        seen = set()
        undefined_vars = set()
        for var in self.dependency_graph:
            self._add_dependencies(var, sorted_eqs, seen, undefined_vars)

        # adding undefined variables at the end
        for var in undefined_vars:
            sorted_eqs[var] = None

        return sorted_eqs
    
class MergeSort:
    def __init__(self, items, sort_index = 2):
        self.items = items
        self.sort_index = sort_index
        self._merge_sort()

    def _merge_sort(self):
        if len(self.items) > 1:
            mid = int(len(self.items) / 2)

            left_half = self.items[:mid]
            right_half = self.items[mid:]

            left_sorter = MergeSort(left_half, self.sort_index)
            right_sorter = MergeSort(right_half, self.sort_index)

            left_index, right_index, merge_index = 0, 0, 0

            while left_index < len(left_half) and right_index < len(right_half):
                left_value = left_half[left_index][self.sort_index]
                right_value = right_half[right_index][self.sort_index]

                left_value = float('-inf') if left_value is None else left_value
                right_value = float('-inf') if right_value is None else right_value

                # Reverse the comparison for descending order
                if left_value > right_value:
                    self.items[merge_index] = left_half[left_index]
                    left_index += 1
                else:
                    self.items[merge_index] = right_half[right_index]
                    right_index += 1
                merge_index += 1

            while left_index < len(left_half):
                self.items[merge_index] = left_half[left_index]
                left_index += 1
                merge_index += 1

            while right_index < len(right_half):
                self.items[merge_index] = right_half[right_index]
                right_index += 1
                merge_index += 1