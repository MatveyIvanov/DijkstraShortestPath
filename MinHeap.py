class minHeapNode:

    def __init__(self, vertex, distance):
        self.vertex = vertex
        self.distance = distance

class Minheap:

    def __init__(self):
        self.heap = []
        self.pos = []
        self.size = 0

    def new_node(self, v, d):
        return minHeapNode(v, d)

    def min_el(self):
        return self.heap[0].vertex

    def swap(self, first, second):
        self.heap[int(first)], self.heap[int(second)] = self.heap[int(second)], self.heap[int(first)]

    def heapify(self, pos): 
        smallest = pos
        left = pos * 2 + 1
        right = pos * 2 + 2
        if left < self.size and self.heap[left].distance < self.heap[smallest].distance:
            smallest = left
        if right < self.size and self.heap[right].distance < self.heap[smallest].distance:
            smallest = right
        if smallest != pos:
            self.pos[self.heap[smallest].vertex] = pos
            self.pos[self.heap[pos].vertex] = smallest
            self.swap(smallest, pos)
            self.heapify(smallest)

    def isEmpty(self):
        if self.size == 0:
            return True
        else:
            return False

    def extract_min(self):
        if self.isEmpty():
            return
        root = self.heap[0]
        last = self.heap[self.size - 1]
        self.heap[0] = last
        self.pos[last.vertex] = 0
        self.pos[root.vertex] = self.size - 1
        self.size -= 1
        self.heapify(0)
        return root

    def decrease_key(self, vertex, distance):
        cur = self.pos[vertex]
        self.heap[int(cur)].distance = distance
        while cur > 0 and self.heap[int(cur)].distance < self.heap[int((cur - 1) / 2)].distance:
            self.pos[self.heap[int(cur)].vertex] = (cur - 1) / 2
            self.pos[self.heap[int((cur - 1) / 2)].vertex] = cur
            self.swap(cur, (cur - 1) / 2)
            cur  = (cur - 1) / 2

    def isInMinHeap(self, vertex):
        if self.pos[vertex] < self.size:
            return True
        else:
            return False
