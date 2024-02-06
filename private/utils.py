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
        def validity_equation(equation):
            _, equation_right = equation.split('=')
            modified_equation = re.sub(r'[a-zA-Z]+', '1', equation_right)
            try:
                eval(modified_equation)
                return True
            except:
                return False 
        def too_many_op(equation):
            # Improved pattern to correctly handle the '**-' exception
            pattern = r'(?:[+\-*/]{3,}(?<!\*\*\-))'

            if re.search(pattern, equation):
                return False
            return True
        def check_double_op(equation):
            exceptions = {"**", "*-", "**-", "--", "+-", "/-"}
            operators = {"+", "-", "*", "/", "**"}
            
            # Iterate through the string to check for side by side operators
            for i in range(len(equation) - 1):
                if equation[i] in operators:
                    # Check for two-character exceptions
                    if equation[i:i+2] in exceptions or equation[i:i+3] in exceptions:
                        continue
                    # Check for a non-exception side by side operators
                    if equation[i+1] in operators:
                        return False
            return True
        def check_solo(equation):
            _, equation_right = equation.split('=')
            for i, char in enumerate(equation_right):
                if char in "+*/":
                    if i == 0 or (not equation_right[i-1].isdigit() and (i < 2 or not equation_right[i-2].isdigit())):
                        return False, char
            return True, None

        if not assignment_string:
            return False, "Input Error: Assignment cannot be empty"
        elif "=" not in assignment_string:
            return False, "Input Error: Assignment must contain '='"
        elif assignment_string.count("(") != assignment_string.count(")"):
            return False, "Input Error: Unequal number of opening and closing parentheses"
        elif validity_equation(assignment_string) is False:
            return False, "Input Error: Invalid equation"
        elif too_many_op(assignment_string) is False:
            return False, "Input Error: Operator Error"
        elif check_double_op(assignment_string) is False:
            return False, "Input Error: Operator Error"
        elif check_solo(assignment_string) is False:
            return False, "Input Error: Free Roaming Operator"
        else:
            return True, None

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

class Plotter:
    def plot_function(self,formula, xmin, xmax, width=80, height=20, x_range=10):
        def math_function(x):
            return eval(formula, {"x": x, "__builtins__": {}})


        def derivative(f, x, h=0.0001):
            return (f(x + h) - f(x - h)) / (2 * h)
        
        def find_turning_points(f, xmin, xmax, steps=1000):
            x_values = [xmin + i * (xmax - xmin) / steps for i in range(steps + 1)]
            turning_points = []

            for i in range(1, len(x_values)):
                x0, x1 = x_values[i - 1], x_values[i]
                dy_dx0, dy_dx1 = derivative(f, x0), derivative(f, x1)

                if dy_dx0 * dy_dx1 < 0 or dy_dx0 == 0:
                    turning_points.append((x0 + x1) / 2)

            return turning_points

        turning_points_x = find_turning_points(math_function, xmin, xmax)
        if turning_points_x:
            center_x = sum(turning_points_x) / len(turning_points_x)
        else:
            center_x = (xmin + xmax) / 2

        xmin = center_x - x_range / 2
        xmax = center_x + x_range / 2

        ymin, ymax = min([math_function(x) for x in turning_points_x] + [math_function(xmin), math_function(xmax)]), max([math_function(x) for x in turning_points_x] + [math_function(xmin), math_function(xmax)])
        ypad = (ymax - ymin) * 0.1
        ymin, ymax = ymin - ypad, ymax + ypad

        plot = [[' ' for _ in range(width)] for _ in range(height)]

        for i in range(width):
            x = xmin + (xmax - xmin) * i / width
            y = math_function(x)
            if ymin <= y <= ymax:
                plot_y = int((y - ymin) / (ymax - ymin) * (height - 1))
                plot[height - plot_y - 1][i] = '*'

        for tp_x in turning_points_x:
            x_pos = int((tp_x - xmin) / (xmax - xmin) * width)
            y = math_function(tp_x)
            if ymin <= y <= ymax:
                plot_y = int((y - ymin) / (ymax - ymin) * (height - 1))
                plot[height - plot_y - 1][x_pos] = 'X'

        for row in plot:
            print(''.join(row))
        
        print(f"\n\ny = {formula}")
        if turning_points_x:
            print("Turning Points Centered Plot:")
        for tp_x in turning_points_x:
            print(f"x ≈ {tp_x:.2f}, y ≈ {math_function(tp_x):.2f}")
        print()

class Simplify:
    def simplify_equation(self, equation):
        equation = equation.replace('x*x', 'x**2').replace('-', '+-').replace(' ', '')
        parts = equation.split('+')
        
        coefficients = {}
        
        for part in parts:
            part = part.strip()
            if not part: 
                continue
            
            if 'x**' in part:
                power = int(part.split('x**')[1])
                coef_part = part.split('x**')[0]
            elif 'x' in part:
                power = 1
                coef_part = part.split('x')[0]
            else:
                power = 0
                coef_part = part
            
            coef_part = coef_part.replace('*', '') 
            if coef_part in ('', '+'):
                coefficient = 1
            elif coef_part == '-':
                coefficient = -1
            else:
                try:
                    coefficient = int(coef_part)
                except ValueError:
                    continue
            
            coefficients[power] = coefficients.get(power, 0) + coefficient
        
        simplified_parts = []
        for power in sorted(coefficients, reverse=True):
            coefficient = coefficients[power]
            if coefficient == 0:
                continue
            if power == 0:
                simplified_parts.append(str(coefficient))
            elif power == 1:
                if coefficient == 1:
                    simplified_parts.append("x")
                elif coefficient == -1:
                    simplified_parts.append("-x")
                else:
                    simplified_parts.append(f"{coefficient}*x")
            else:
                if coefficient == 1:
                    simplified_parts.append(f"x**{power}")
                elif coefficient == -1:
                    simplified_parts.append(f"-x**{power}")
                else:
                    simplified_parts.append(f"{coefficient}*x**{power}")
        
        simplified_equation = '+'.join(simplified_parts).replace('+-', '-')
        first_char, rest_expression = simplified_equation[0], simplified_equation[1:]
        spaced_expression = first_char + re.sub(r'([+\-])', r' \1 ', rest_expression)

        return spaced_expression