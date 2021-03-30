import codecs
import DirectedGraph

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

print(graph.dijkstra('Санкт-Петербург', 'Владивосток'))