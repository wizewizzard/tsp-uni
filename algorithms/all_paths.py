import graph
from itertools import permutations
import numpy as np

def printAllPaths(graph):
    paths_and_lengths = []
    adjacency_matrix = graph.as_adjacency_matrix()
    for path in permutations(range(1, len(adjacency_matrix))):
        this_len = 0
        path = [0, ] + list(path) + [0, ]
        prev = path[0]
        for n in path:
            this_len += adjacency_matrix[prev][n]
            prev = n
        paths_and_lengths.append((path, this_len))
    
    return paths_and_lengths
              

gb = graph.GraphBuilder(3)
gb.add_edge(0, 1, 2.5).add_edge(1, 2, 4).add_edge(2, 0, 0.3)
print(printAllPaths(gb.build()))