from private.datastructure import BinaryTree, Stack, Graph
from private.menu import Menu


class ExpressionTokenizer:
    def _isvariable(self, char):
        return char.isalpha()

    def _isoperator(self, char):
        return char in {"+", "-", "*", "/", "**"}

    def _tokenize_inner(self, exp):
        tokens = []
        i = 0
        while i < len(exp):
            if exp[i] == "*" and i + 1 < len(exp) and exp[i + 1] == "*":
                tokens.append("**")
                i += 2
            elif self._isvariable(exp[i]):
                variable_name = exp[i]
                i += 1
                while i < len(exp) and self._isvariable(exp[i]):
                    variable_name += exp[i]
                    i += 1
                tokens.append(variable_name)
            elif exp[i].isdigit():
                number = exp[i]
                i += 1
                while i < len(exp) and (exp[i].isdigit() or exp[i] == "."):
                    number += exp[i]
                    i += 1
                tokens.append(number)
            elif exp[i] == "-":
                # Check if it's a normal minus sign based on your provided condition
                if (
                    i != 0
                    and (exp[i - 1]).isdigit()
                    or self._isvariable(exp[i - 1])
                    or exp[i - 1] == ")"
                ) and (
                    (exp[i + 1]).isdigit()
                    or self._isvariable(exp[i + 1])
                    or exp[i + 1] == "("
                ):
                    tokens.append("-")  # Append '-' directly as an operator
                    i += 1
                else:
                    # Handle as negation
                    if exp[i + 1] == "(":
                        j = i + 2
                        bracket_count = 1
                        while j < len(exp) and bracket_count > 0:
                            if exp[j] == "(":
                                bracket_count += 1
                            elif exp[j] == ")":
                                bracket_count -= 1
                            j += 1
                        inside_tokens = self._tokenize_inner(exp[i + 2 : j - 1])
                        tokens.extend(["(", *inside_tokens, "*", "-1", ")"])
                        i = j
                    elif exp[i + 1].isdigit() or self._isvariable(exp[i + 1]):
                        # For negative numbers or variables next
                        i += 1  # Move past '-' to process the number/variable
                        if exp[i].isdigit():  # Negative number
                            number = exp[i]
                            i += 1
                            while i < len(exp) and (exp[i].isdigit() or exp[i] == "."):
                                number += exp[i]
                                i += 1
                            tokens.extend(["(", number, "*", "-1", ")"])
                        else:  # Negative variable
                            variable_name = exp[i]
                            i += 1
                            while i < len(exp) and self._isvariable(exp[i]):
                                variable_name += exp[i]
                                i += 1
                            tokens.extend(["(", variable_name, "*", "-1", ")"])
            else:
                tokens.append(exp[i])
                i += 1
        return tokens

    def tokenize(self, expression):
        exp = "".join(("(", expression.replace(" ", ""), ")"))
        return self._tokenize_inner(exp)


class ParseTreeBuilder:
    def __init__(self):
        self.stack = Stack()
        self.tkn = ExpressionTokenizer()

    def build_tree(self, expression):
        tokens = self.tkn.tokenize(expression)
        for token in tokens:
            if token == "(":
                self.stack.push(token)
            elif token in ["+", "-", "*", "/", "**"]:
                self.stack.push(token)
            elif token == ")":
                # pop until the '('
                temp_stack = Stack()
                while not self.stack.isEmpty() and self.stack.peek() != "(":
                    temp_stack.push(self.stack.pop())
                self.stack.pop()

                # process the temp_stack to form a sub-tree
                while temp_stack.size() > 1:
                    right = temp_stack.pop()
                    operator = temp_stack.pop()
                    if operator in ["+", "-", "*", "/", "**"]:
                        left = temp_stack.pop()
                        new_node = BinaryTree(operator, left, right)
                    else:  # for unary operator
                        new_node = BinaryTree(operator, None, right)
                    temp_stack.push(new_node)

                # push the sub-tree back onto the main stack
                self.stack.push(temp_stack.pop())
            else:
                # push operand as a new leaf node
                self.stack.push(BinaryTree(token))

        # last node on the stack is the root of the tree
        return self.stack.pop()


class BinaryTreeEvaluator:
    def __init__(self):
        self.menu = Menu()
        self.circular_detector = Graph()

    def evaluate(self, root, variables, parent_var=None):
        if root is None:
            return 0

        key = root.getKey()

        # Add edges to the graph for circular dependency detection
        if parent_var and key in variables:
            self.circular_detector.add_edge(parent_var, key)

        # detect circular dependency
        circular_dependency = self.circular_detector.detect_circular_dependency()
        if key in circular_dependency:
            return None

        # check if the key is a variable in the dictionary
        if key in variables:
            # get the value of the variable
            var_value = variables[key]

            # handle None value
            if var_value is None:
                return None

            # if the value is an expression, evaluate it
            if isinstance(var_value, str):
                builder = ParseTreeBuilder()
                var_tree = builder.build_tree(var_value)
                return self.evaluate(var_tree, variables, parent_var=key)

        # if it's a leaf node and not a variable, return its value as an integer
        if root.getLeftTree() is None and root.getRightTree() is None:
            try:
                return float(key)
            except ValueError:
                return None  # in case the leaf node is not an integer or a valid variable

        # recursively evaluate the left and right subtrees
        left_val = self.evaluate(root.getLeftTree(), variables, parent_var)
        right_val = self.evaluate(root.getRightTree(), variables, parent_var)

        # apply the operation at the current node (need to handle division by 0 later)
        if key == "+":
            return right_val + left_val if right_val is not None and left_val is not None else None
        elif key == "-":
            return right_val - left_val if right_val is not None and left_val is not None else None
        elif key == "*":
            return right_val * left_val if right_val is not None and left_val is not None else None
        elif key == "/":
            return right_val / left_val if right_val is not None and left_val is not None and left_val != 0 else None
        elif key == "**":
            return right_val ** left_val if right_val is not None and left_val is not None else None

        return 0  # in case of an unsupported operation (debug)
    
    def check_cd(self, root, variables, parent_var=None):
        if root is None:
            return 0

        key = root.getKey()

        # Add edges to the graph for circular dependency detection
        if parent_var and key in variables:
            self.circular_detector.add_edge(parent_var, key)

        # Detect circular dependency
        circular_dependency = self.circular_detector.detect_circular_dependency()
        if len(circular_dependency) != 0:
            return circular_dependency