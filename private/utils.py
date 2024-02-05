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
        self.dh = DictionaryHandler()
        self.ptb = ParseTreeBuilder()
        self.bte = BinaryTreeEvaluator()

    def is_valid_assignment(self, assignment_string):
        def is_numeric_equation(equation):
            numeric_pattern = r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*\(\s*(?:\d*\.?\d+|\d+\.\d*|[a-zA-Z_][a-zA-Z0-9_]*)(?:\s*[\+\-\*\/]\s*(?:\d*\.?\d+|\d+\.\d*|[a-zA-Z_][a-zA-Z0-9_]*))*\s*\)\s*$'
            return bool(re.match(numeric_pattern, equation))

        def is_complex_equation(equation):
            complex_pattern = r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*\((?:[a-zA-Z_0-9\.\+\-\*\/\s\(\)]+)\)\s*$'
            return bool(re.match(complex_pattern, equation))

        temp_assignments = {}
        temp_assignments = self.dh.add_to_dict(assignment_string, temp_assignments)
        if not assignment_string:
            return False, "Input Error: Assignment cannot be empty"
        elif "=" not in assignment_string:
            return False, "Input Error: Assignment must contain '='"
        elif assignment_string.count("(") != assignment_string.count(")"):
            return False, "Input Error: Unequal number of opening and closing parentheses"
        else:
            assignment_string_clean = assignment_string.replace(" ", "")
            if is_numeric_equation(assignment_string_clean):
                return True, None
            elif is_complex_equation(assignment_string_clean):
                return True, None
            else:
                return False, "Input Error: Invalid Format"

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