from LinkedList import LinkedList, LinkedListNode
import Stack, Queue, MinHeap, Map
import sys


class DirectedGraph:

    def __init__(self):
        self.adjacency_lists = LinkedList()
        self.nextVal = 1
        self.city_indexes = Map.Map()

    # Find vertex with max value
    def max(self):
        if self.adjacency_lists.head != None:
            max_value = 0
            cur_list = self.adjacency_lists.head
            while cur_list != None:
                cur = cur_list
                while cur != None:
                    if cur.node_num > max_value:
                        max_value = cur.node_num
                    cur = cur.next
                cur_list = cur_list.next_list
            return max_value
        else:
            raise Exception("Graph is empty")

    # Insert edge [vertex1, vertex2] into the graph
    def insert(self, vertex1, vertex2, distance):
        # If graph is empty
        if self.adjacency_lists.head == None:
            self.city_indexes.insert(vertex1, self.nextVal)
            self.nextVal += 1
            self.city_indexes.insert(vertex2, self.nextVal)
            self.nextVal += 1
            self.adjacency_lists.head = LinkedListNode(vertex1, self.city_indexes[vertex1])
            self.adjacency_lists.head.next = LinkedListNode(vertex2, self.city_indexes[vertex2], distance)
        else:
            cur_list = self.adjacency_lists.head
            # Check if vertex1 has adjacent vertices
            while cur_list.next_list != None and cur_list.value != vertex1:
                cur_list = cur_list.next_list
            # If vertex1 has adjacent vertices
            if cur_list.value == vertex1:
                if cur_list.next == None:
                    if self.city_indexes[vertex2] is None:
                        self.city_indexes.insert(vertex2, self.nextVal)
                        self.nextVal += 1
                    cur_list.next = LinkedListNode(vertex2, self.city_indexes[vertex2], distance)
                    return
                cur = cur_list.next
                while cur.next != None:
                    if cur.value == vertex2:
                        raise Exception("Edge already exists")
                    cur = cur.next
                if self.city_indexes[vertex2] is None:
                    self.city_indexes.insert(vertex2, self.nextVal)
                    self.nextVal += 1
                cur.next = LinkedListNode(vertex2, self.city_indexes[vertex2], distance)
                return
            # If vertex1 does not have adjacent vertices
            else:
                if self.city_indexes[vertex1] is None:
                    self.city_indexes.insert(vertex1, self.nextVal)
                    self.nextVal += 1
                cur_list.next_list = LinkedListNode(vertex1, self.city_indexes[vertex1])
                cur_list = cur_list.next_list
                if self.city_indexes[vertex2] is None:
                    self.city_indexes.insert(vertex2, self.nextVal)
                    self.nextVal += 1
                cur_list.next = LinkedListNode(vertex2, self.city_indexes[vertex2], distance)
                

    # Remove edge [vertex1, vertex2] from the graph
    def remove(self, vertex1, vertex2):
        cur_list = self.adjacency_lists.head
        while cur_list != None and cur_list.value != vertex1:
            cur_list = cur_list.next_list
        # If vertex1 has adjacent vertices
        if cur_list != None:
            cur = cur_list
            # Delete vertex2 from adjacency lists
            while cur.next != None and cur.next.value != vertex2:
                cur = cur.next
            if cur.next == None and cur.value != vertex2: # If vertex2 not in list of adjacent vertices of vertex1
                raise Exception("Edge does not exist")
            else:
                temp = cur.next.next
                cur.next = None
                cur.next = temp
        else: # If edge does not exist
            raise Exception("Edge does not exist")

    # Recover the path from start vertex to end vertex
    def recover_path(self, distances, start, end):
        path = []
        city_names = Map.Map()
        it = Map.DFT_Iterator(self.city_indexes)
        while it.has_next():
            temp = next(it)
            city_names.insert(temp.value, temp.key)
        path.insert(0, city_names[end])
        while end != start:
            cur_list = self.adjacency_lists.head
            while cur_list is not None:
                cur = cur_list.next
                while cur is not None and cur.node_num != end:
                    cur = cur.next
                if cur is not None and distances[end] - cur.edge_value == distances[cur_list.node_num]:
                    path.insert(0, city_names[cur_list.node_num])
                    end = cur_list.node_num
                    break
                cur_list = cur_list.next_list
        return path

    # Dijkstra shortest path algorithm
    def dijkstra(self, start_city, end_city):
        cur_list = graph.adjacency_lists.head
        start_found = False
        end_found = False
        start, end = None, None
        # Check if start and end vertices are in the graph
        while cur_list != None and (start_found == False or end_found == False):
            if cur_list.value == start_city:
                start_found = True
                start = cur_list.node_num
            if cur_list.value == end_city:
                end_found = True
                end = cur_list.node_num
            cur_list = cur_list.next_list
        if start_found == True and end_found == True:
            max_value = graph.max() # Max value in the graph
            distances = [sys.maxsize] * (max_value + 1) # Distances from start to vertex[i]
            minHeap = MinHeap.Minheap() # Min heap for vertixes that are not processed yet
            minHeap.size = max_value + 1 # Min heap.nextVal
            # Add all vertices to the min heap
            for i in range(max_value + 1):
                minHeap.heap.append(minHeap.new_node(i, distances[i]))
                minHeap.pos.append(i)
            minHeap.pos[start] = start
            distances[start] = 0 # Distance from start vertex to itself is 0
            minHeap.decrease_key(start, distances[start]) # Change vertex position in heap according to it's new distance
            while minHeap.min_el() != end: # While distance from start to end is not found
                cur_min = minHeap.extract_min() # Get minimal vertex with minimal distance from set of processed vertices
                cur_list = graph.adjacency_lists.head
                while cur_list != None and cur_list.node_num != cur_min.vertex:
                    cur_list = cur_list.next_list
                # Loop through adjacent vertices of current minimal vertex and update their distances if it's needed
                if cur_list != None:
                    cur = cur_list.next
                    while cur != None:
                        if minHeap.isInMinHeap(cur.node_num) and distances[cur_min.vertex] != sys.maxsize and cur.edge_value + distances[cur_min.vertex] < distances[cur.node_num]:
                            distances[cur.node_num] = cur.edge_value + distances[cur_min.vertex] # Change distance
                            minHeap.decrease_key(cur.node_num, distances[cur.node_num]) # Change position in min heap
                        cur = cur.next
            return self.recover_path(distances, start, end)
        else:
            raise Exception("Path does not exist")

    # Depth first traversal iterator
    class dftIterator:

        def __init__(self, graph, start=None):
            self.stack = Stack.Stack()
            self.graph = graph
            self.graph.sizel = self.graph.max() # Number of vertices in graph
            print(self.graph.size)
            self.visited = [False] * (self.graph.size + 1)
            if start is None:
                self.stack.push(self.graph.adjacency_lists.head.value) # Push first vertex of adjacency list into the stack
            else:
                self.stack.push(start) # Push start vertex into the stack
            self.traversal_done = False

        def __next__(self):
            if self.has_next():
                temp = self.stack.pop()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in stack
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                cur_list = self.graph.adjacency_lists.head
                while cur_list != None and cur_list.value != temp:
                    cur_list = cur_list.next_list
                if cur_list != None:
                    # Add not visited adjacent vertices into the stack
                    cur = cur_list.next
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.stack.push(cur.value)
                        cur = cur.next
                return temp # Return current vertex
            else:
                # Checking for other unhandled strongly connected components
                self.traversal_done = True
                cur_list = self.graph.adjacency_lists.head
                # Check if there is not visited vertex in the graph
                while cur_list != None:
                    if self.visited[cur_list.value] == False:
                        self.stack.push(cur_list.value)
                        self.traversal_done = False
                        break
                    cur_list = cur_list.next_list
                if self.traversal_done == False: # If we found that vertex
                    temp = self.stack.pop()
                    self.visited[temp] = True # Mark vertex as visited
                    cur = cur_list.next
                    # Add not visited adjacent vertices into the stack
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.stack.push(cur.value)
                        cur = cur.next
                    return temp # Return current vertex
                else: 
                    raise StopIteration # Traversal is done

        def has_next(self):
            if self.stack.isEmpty():
                return False
            else:
                return True


    # Breadth first traversal iterator
    class bftIterator:

        def __init__(self, graph, start=None):
            self.queue = Queue.Queue()
            self.graph = graph
            self.graph.size = self.graph.max() # Number of vertices in graph
            self.visited = [False] * (self.graph.size + 1)
            if start is None:
                self.queue.enqueue(self.graph.adjacency_lists.head.value) # Insert first vertex of adjacency list into the queue
            else:
                self.queue.enqueue(start) # Insert start vertex into the queue
            self.traversal_done = False 

        def __next__(self):
            if self.has_next():
                temp = self.queue.dequeue()
                if self.visited[temp] == True: # If vertex is already visited go to the next vertex in queue
                    return self.__next__()
                self.visited[temp] = True # Mark vertex as visited
                cur_list = self.graph.adjacency_lists.head
                while cur_list != None and cur_list.value != temp:
                    cur_list = cur_list.next_list
                # Add not visited adjacent vertices of current vertex if they exist
                if cur_list != None:
                    cur = cur_list.next
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.queue.enqueue(cur.value)
                        cur = cur.next
                return temp # Return current vertex
            else:
                # Checking for other unhandled strongly connected components
                self.traversal_done = True
                cur_list = self.graph.adjacency_lists.head
                # Check if there is not visited vertex in the graph
                while cur_list != None:
                    if self.visited[cur_list.value] == False:
                        self.queue.enqueue(cur_list.value)
                        self.traversal_done = False
                        break
                    cur_list = cur_list.next_list
                if self.traversal_done == False: # If we found that vertex
                    temp = self.queue.dequeue()
                    self.visited[temp] = True # Mark vertex as visited
                    cur = cur_list.next
                    # Add not visited adjacent vertices into the queue
                    while cur != None:
                        if self.visited[cur.value] == False:
                            self.queue.enqueue(cur.value)
                        cur = cur.next
                    return temp
                else: # Traversal is done
                    raise StopIteration

        def has_next(self):
            if self.queue.isEmpty():
                return False
            else:
                return True


graph = DirectedGraph()
graph.insert('Санкт-Петербург', 'Москва', 10)
graph.insert('Москва', 'Санкт-Петербург', 20)
graph.insert('Москва', 'Хабаровск', 40)
graph.insert('Хабаровск', 'Москва', 35)
graph.insert('Хабаровск', 'Владивосток', 8)
graph.insert('Владивосток', 'Хабаровск', 13)
graph.insert('Санкт-Петербург', 'Хабаровск', 14)
graph.insert('Санкт-Петербург', 'Владивосток', 30)


print(graph.dijkstra('Санкт-Петербург', 'Владивосток'))