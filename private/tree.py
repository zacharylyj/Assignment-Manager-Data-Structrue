from private.datastructure import BinaryTree, Stack
import operator

class Tree:
    def __init__(self):
        self.BinaryTree = BinaryTree()
        self.Stack = Stack()

    def build_parse_tree(self, postfix_expr):
        token_list = postfix_expr.split()
        stack = Stack()
        
        for token in token_list:
            if token in "+-*/**":
                node = BinaryTree(token)
                node.rightTree = stack.pop()
                node.leftTree = stack.pop()
                stack.push(node)
            else:
                stack.push(BinaryTree(token))

        return stack.pop()
        
    def evaluate(self, parse_tree, var_dict={}):
        ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '**': operator.pow}

        leftree = parse_tree.getLeftTree()
        rightree = parse_tree.getRightTree()

        if leftree and rightree:
            fn = ops[parse_tree.getKey()]
            return fn(self.evaluate(leftree, var_dict), self.evaluate(rightree, var_dict))
        else:
            key = parse_tree.getKey()
            if key.isdigit():
                return int(key)
            else:
                return var_dict.get(key, None)