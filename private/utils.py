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
            pattern2 = r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*(?:[a-zA-Z_][a-zA-Z0-9_]*\s*(?:\+|-)\s*)*[a-zA-Z_][a-zA-Z0-9_]*\s*$'
            if bool(re.match(pattern, equation.strip())) == True:
                return True
            try:
                for key, item in temp_assignments.items():
                    if item is not None:
                        temp = self.bte.evaluate(
                            self.ptb.build_tree(key), temp_assignments
                        )
                    if temp is None:
                        print("Input Error: Expression is not valid. Please try Again")
            except Exception as e:
                print("Input Error: Expression is not valid. Please try Again")
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
