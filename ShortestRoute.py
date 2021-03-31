import codecs
import DirectedGraph

graph = DirectedGraph.DirectedGraph()
filename = 'Flights.txt'


with codecs.open(filename, 'r', encoding='utf-8') as f: # Open file
    for line in f: # Loop through all lines
        line = line.strip('\n') # Delete \n symbol from line
        line = line.strip('\r') # Delete \r symbol from line
        line = line.split(';') # Slpit line by ;
        if line[2] != 'N/A': # If path from city1 to city2 exists
            graph.insert(line[0], line[1], int(line[2])) # Add edge to the graph
        if line[3] != 'N/A': # If path from city2 to city1 exists
            graph.insert(line[1], line[0], int(line[3])) # Add edge to the graph

print(graph.dijkstra('Санкт-Петербург', 'Владивосток'))
print(graph.dijkstra('Санкт-Петербург', 'Казань'))
print(graph.dijkstra('Москва', 'Хабаровск'))
print(graph.dijkstra('Москва', 'Казань'))