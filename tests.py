import unittest
import DirectedGraph
import codecs


class ShortestRouteTests(unittest.TestCase):
    def setUp(self):
        self.graph = DirectedGraph.DirectedGraph()
        self.graph.insert('Санкт-Петербург', 'Москва', 10)
        self.graph.insert('Москва', 'Санкт-Петербург', 20)
        self.graph.insert('Москва', 'Хабаровск', 40)
        self.graph.insert('Хабаровск', 'Москва', 35)
        self.graph.insert('Хабаровск', 'Владивосток', 8)
        self.graph.insert('Владивосток', 'Хабаровск', 13)
        self.graph.insert('Санкт-Петербург', 'Казань', 25)
        self.graph.insert('Казань', 'Санкт-Петербург', 40)
        self.graph.insert('Санкт-Петербург', 'Владивосток', 30)
        self.graph.insert('Санкт-Петербург', 'Хабаровск', 14)
        self.graph.insert('Хабаровск', 'Казань', 6)

    def test_max(self):
        self.assertEqual(self.graph.max(), 5)

    def test_insert_vertex1_exists(self):
        self.graph.insert('Москва', 'Казань', 12)
        cur_list = self.graph.adjacency_lists.head
        while cur_list != None:
            if cur_list.value == 'Москва':
                break
            cur_list = cur_list.next_list
        cur = cur_list.next
        while cur != None:
            if cur.value == 'Казань':
                break
            cur = cur.next
        self.assertEqual(cur.value, 'Казань')

    def test_insert_vertex1_doesnt_exist(self):
        self.graph.insert('Сочи', 'Санкт-Петербург', 15)
        cur_list = self.graph.adjacency_lists.head
        while cur_list != None:
            if cur_list.value == 'Казань':
                break
            cur_list = cur_list.next_list
        cur = cur_list.next
        while cur != None:
            if cur.value == 'Санкт-Петербург':
                break
            cur = cur.next
        self.assertEqual(cur.value, 'Санкт-Петербург')

    def test_insert_exception(self):
        try:
            self.graph.insert('Казань', 'Санкт-Петербург', 40)
        except Exception as e:
            self.assertEqual(str(e), "Edge already exists")

    def test_remove(self):
        self.graph.remove('Хабаровск', 'Казань')
        iterator = self.graph.dftIterator(self.graph, 'Санкт-Петербург')
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, ['Санкт-Петербург', 'Хабаровск', 'Владивосток', 'Москва', 'Казань'])

    def test_remove_exception_vertex1_doesnt_exist(self):
        try:
            self.graph.remove('Сочи', 'Москва')
        except Exception as e:
            self.assertEqual(str(e), "Edge does not exist")

    def test_remove_exception_vertex2_doesnt_exist(self):
        try:
            self.graph.remove('Москва', 'Сочи')
        except Exception as e:
            self.assertEqual(str(e), "Edge does not exist")

    def test_dft_iterator_default_start(self):
        iterator = self.graph.dftIterator(self.graph)
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, ['Санкт-Петербург', 'Хабаровск', 'Казань', 'Владивосток', 'Москва'])

    def test_dft_iterator_set_start(self):
        iterator = self.graph.dftIterator(self.graph, 'Хабаровск')
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, ['Хабаровск', 'Казань', 'Санкт-Петербург', 'Владивосток', 'Москва'])

    def test_dft_iterator_in_graph_with_several_strongly_connected_components(self):
        self.graph.insert('Сочи', 'Екатеринбург', 25)
        iterator = self.graph.dftIterator(self.graph, 'Сочи')
        dft_result = []
        for _ in range(iterator.graph_size):
            dft_result.append(next(iterator))
        self.assertListEqual(dft_result, ['Сочи', 'Екатеринбург', 'Санкт-Петербург', 'Хабаровск', 'Казань', 'Владивосток', 'Москва'])

    def test_bft_iterator_default_start(self):
        iterator = self.graph.bftIterator(self.graph)
        bft_result = []
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, ['Санкт-Петербург', 'Москва', 'Казань', 'Владивосток', 'Хабаровск'])

    def test_bft_iterator_set_start(self):
        iterator = self.graph.bftIterator(self.graph, 'Владивосток')
        bft_result = []
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, ['Владивосток', 'Хабаровск', 'Москва', 'Казань', 'Санкт-Петербург'])

    def test_bft_iterator_in_graph_with_some_strongly_connected_components(self):
        self.graph.insert('Сочи', 'Екатеринбург', 25)
        iterator = self.graph.bftIterator(self.graph, 'Санкт-Петербург')
        bft_result = []
        for _ in range(iterator.graph_size):
            bft_result.append(next(iterator))
        self.assertListEqual(bft_result, ['Санкт-Петербург', 'Москва', 'Казань', 'Владивосток', 'Хабаровск', 'Сочи', 'Екатеринбург'])

    def test_shortest_path(self):
        graph = DirectedGraph.DirectedGraph()
        with codecs.open('Flights.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip('\n')
                line = line.strip('\r')
                line = line.split(';')
                if line[2] != 'N/A':
                    graph.insert(line[0], line[1], int(line[2]))
                if line[3] != 'N/A':
                    graph.insert(line[1], line[0], int(line[3]))
        self.assertListEqual(graph.dijkstra('Санкт-Петербург', 'Казань'), ['Санкт-Петербург', 'Хабаровск', 'Казань', '20'])
            

    def test_shortest_path_exception(self):
        self.graph.insert('Сочи', 'Ростов', 20)
        try:
            self.graph.dijkstra('Санкт-Петербург', 'Сочи')
        except Exception as e:
            self.assertEqual(str(e), 'Path does not exist')