import re
import os


class DictionaryHandler:
    def add_to_dict(self, assignment_input, assignments):
        key, value = assignment_input.replace(" ", "").split("=")

        assignments[key] = value
        return assignments


class InputHandler:
    def __init__(self):
        self.assignment_pattern = re.compile(r"^[a-zA-Z0-9+\-*/**()= ]+$")

    def is_valid_assignment(self, assignment_string):
        if not assignment_string:
            print("Input Error: Assignment cannot be empty")
            return False
        elif not self.assignment_pattern.match(assignment_string):
            print("Input Error: Use of Invalid characters")
            return False
        elif "=" not in assignment_string:
            print("Input Error: Assignment must contain '='")
            return False
        else:
            balance = 0
            for char in assignment_string:
                if char == "(":
                    balance += 1
                elif char == ")":
                    balance -= 1
                if balance < 0:  # Closing parenthesis before an opening one
                    print("Error: Unbalanced parentheses")
                    return False

            if balance != 0:
                print("Error: Unbalanced parentheses")
                return False

            # Check for valid characters and syntax
            valid_chars = set(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/()= "
            )
            for char in assignment_string:
                if char not in valid_chars:
                    print("Error: Invalid character found")
                    return False

            # Basic syntax check for consecutive operators or invalid operand/operator placement
            prev_char = ""
            for char in assignment_string.replace(
                " ", ""
            ):  # Removing spaces to simplify checks
                if self._isoperator(char) and self._isoperator(prev_char):
                    print("Error: Consecutive operators")
                    return False
                if char in "+*/" and (prev_char == "" or prev_char in "+-*/("):
                    print("Error: Operator at invalid position")
                    return False
                prev_char = char

            # All checks passed
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
