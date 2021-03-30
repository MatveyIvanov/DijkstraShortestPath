class Node:
    
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.top_node = None

    def push(self, value):
        if self.top_node is None:
            self.top_node = Node(value)
        else:
            temp = self.top_node
            self.top_node = Node(value)
            self.top_node.next = temp

    def top(self):
        return self.top_node.value
    
    def pop(self):
        if self.isEmpty():
            raise Exception("Stack is empty")
        else:
            temp = self.top_node.value
            self.top_node = self.top_node.next
            return temp

    def isEmpty(self):
        if self.top_node is None:
            return True
        else:
            return False