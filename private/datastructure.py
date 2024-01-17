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
        print(str(level * '-') + str(self.key))
        if self.leftTree is not None:
            self.leftTree.printPreorder(level + 1)
        if self.rightTree is not None:
            self.rightTree.printPreorder(level + 1)
            
    def printInorder(self, level=0):
        if self.leftTree is not None:
            self.leftTree.printInorder(level + 1)
        print(str(level * '-') + str(self.key))
        if self.rightTree is not None:
            self.rightTree.printInorder(level + 1)

    def printPostorder(self, level=0):
        if self.leftTree is not None:
            self.leftTree.printPostorder(level + 1)
        if self.rightTree is not None:
            self.rightTree.printPostorder(level + 1)
        print(str(level * '-') + str(self.key))


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