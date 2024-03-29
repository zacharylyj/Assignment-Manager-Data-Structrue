class BinaryTree:
    def __init__(self, key, leftTree=None, rightTree=None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def getLeftTree(self):
        return self.leftTree

    def getRightTree(self):
        return self.rightTree

    def insertLeft(self, key):
        if self.leftTree is None:
            self.leftTree = BinaryTree(key)
        else:
            new_node = BinaryTree(key, leftTree=self.leftTree)
            self.leftTree = new_node

    def insertRight(self, key):
        if self.rightTree is None:
            self.rightTree = BinaryTree(key)
        else:
            new_node = BinaryTree(key, rightTree=self.rightTree)
            self.rightTree = new_node

    def printPreorder(self, level=0):
        print(str(level * '.') + str(self.key))
        if self.leftTree is not None:
            self.leftTree.printPreorder(level + 1)
        if self.rightTree is not None:
            self.rightTree.printPreorder(level + 1)
            
    def printInorder(self, level=0):
        if self.leftTree is not None:
            self.leftTree.printInorder(level + 1)
        print(str(level * '.') + str(self.key))
        if self.rightTree is not None:
            self.rightTree.printInorder(level + 1)

    def printPostorder(self, level=0):
        if self.leftTree is not None:
            self.leftTree.printPostorder(level + 1)
        if self.rightTree is not None:
            self.rightTree.printPostorder(level + 1)
        print(str(level * '.') + str(self.key))


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.isEmpty():
            return self.items.pop()
        else:
            raise IndexError("Pop from an empty stack")

    def peek(self):
        if not self.isEmpty():
            return self.items[-1]
        else:
            raise IndexError("Peek from an empty stack")

    def size(self):
        return len(self.items)

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, key, item):
        new_node = Node(key, item)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def find(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current.item
            current = current.next
        return None

    def sort(self):
        if self.head is None or self.head.next is None:
            return

        size = 1
        current = self.head
        while current.next:
            size += 1
            current = current.next

        step = 1
        while step < size:
            self.head = self.merge_pass(self.head, step)
            step *= 2

    def merge_pass(self, head, step):
        current = head
        prev_tail = None
        new_head = None

        while current:
            left = current
            right = self.split(left, step)
            current = self.split(right, step)

            merged = self.sorted_merge(left, right)

            if prev_tail:
                prev_tail.next = merged
            else:
                new_head = merged

            while prev_tail and prev_tail.next:
                prev_tail = prev_tail.next

        return new_head

    def split(self, head, step):
        if head is None:
            return None
        for _ in range(step - 1):
            if head.next is None:
                break
            head = head.next
        next_head = head.next
        head.next = None
        return next_head

    def sorted_merge(self, a, b):
        if a is None:
            return b
        if b is None:
            return a

        if a.key <= b.key:
            result = a
            result.next = self.sorted_merge(a.next, b)
        else:
            result = b
            result.next = self.sorted_merge(a, b.next)
        return result

class Node:
    def __init__(self, key, item):
        self.key = key
        self.item = item
        self.next = None

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, src, dest):
        if src not in self.graph:
            self.graph[src] = []
        self.graph[src].append(dest)

    def detect_circular_dependency(self):
        visited = set()
        rec_stack = set()
        circular_dependency = set()
        path = []

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            if node in self.graph:
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        if dfs(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        circular_dependency.update(path[path.index(neighbor):])
                        return True

            rec_stack.remove(node)
            path.pop()
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return circular_dependency

        return set()

    def reset_edges(self):
        self.graph = {}

class VariableSearch:
    def __init__(self, variables):
        self.value_to_variables = {}
        for variable, expression, value in variables:
            if value not in self.value_to_variables:
                self.value_to_variables[value] = []
            self.value_to_variables[value].append((variable, expression))
    
    def _dfs(self, value, visited, found_variables):
        if value in visited:
            return
        visited.add(value)
        if value in self.value_to_variables:
            found_variables.extend(self.value_to_variables[value])
            for neighbor in self.value_to_variables[value]:
                self._dfs(neighbor, visited, found_variables)
    
    def find_variables_by_value(self, target_value):
        visited = set()
        found_variables = []
        self._dfs(target_value, visited, found_variables)
        return found_variables