class Node:
    
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:

    def __init__(self):
        self.first = None
        self.last = None

    def enqueue(self, value):
        if self.isEmpty():
            self.first = Node(value)
            self.last = self.first
        else:
            self.last.next = Node(value)
            self.last = self.last.next

    def dequeue(self):
        if self.isEmpty():
            raise Exception("Queue is empty")
        else:
            temp = self.first.value
            self.first = self.first.next
            return temp

    def isEmpty(self):
        if self.first is None:
            return True
        else:
            return False
