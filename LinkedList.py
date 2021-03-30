class LinkedListNode:

    def __init__(self, value, node_num=0, edge_value = 0):
        self.value = value
        self.edge_value = edge_value
        self.node_num = node_num
        self.next = None
        self.next_list = None


class LinkedList:

    def __init__(self):
        self.head = None
        self.last = self.head

    def push_back(self, val, node_num, edge_value = 0):
        new_node = LinkedListNode(val, node_num, edge_value)
        if self.head == None:
            self.head = new_node
            self.last = self.head
        else:
            self.last.next = new_node
            self.last = self.last.next

    def pop_back(self):
        temp = self.head
        while(temp.next.next != None):
            temp = temp.next
        temp.next = None

    def remove(self, val):
        if self.head.value == val:
            self.head = None
            self.head = self.head.next
        else:
            cur = self.head
            while cur.next.value != val and cur != None:
                cur = cur.next
            temp = cur.next.next
            cur.next = None
            cur.next = temp
