from sys import maxsize 
from itertools import permutations
import graph
import numpy as np

def tsp(graph):
    n = len(graph)
    min_path = []
    min_length = float('inf')

    for path in permutations(range(1, n)):
        current_length = 0
        prev = 0
        for node in path:
            current_length += graph[prev][node]
            prev = node
        current_length += graph[prev][0]
        if current_length < min_length:
            min_length = current_length
            min_path = [0, ] + list(path) + [0, ]

    return min_path, min_length

class BruteForce:
    def tsp(self, graph):
        return tsp(graph.as_adjacency_matrix())


brute_force = BruteForce()

gb = graph.GraphBuilder(vertex_count=3)
gb.add_edge(0, 1, 2.5).add_edge(1, 2, 4).add_edge(2, 0, 0.3)
route, dist = brute_force.tsp(gb.build())
assert dist == 6.8, "Should be 6.8"

gb = graph.GraphBuilder(vertex_count=4)
gb.add_edge(0, 1, 2).add_edge(1, 2, 4).add_edge(2, 3, 3).add_edge(3, 0, 2).add_edge(0, 2, 1).add_edge(1, 3, 2)
route, dist = brute_force.tsp(gb.build())
assert dist == 8, "Should be 8"

gb = graph.GraphBuilder(vertex_count=4)
gb.add_edge(0, 1, 1).add_edge(1, 2, 1).add_edge(2, 3, 1).add_edge(3, 0, 1).add_edge(0, 2, 1).add_edge(1, 3, 1)

route, dist = brute_force.tsp(gb.build())
print(route)
assert dist == 4, "Should be 4"

distance_matrix = [
        [0, 328, 259, 180, 314, 294, 269, 391],
        [328, 0, 83, 279, 107, 131, 208, 136],
        [259, 83, 0, 257, 70, 86, 172, 152],
        [180, 279, 257, 0, 190, 169, 157, 273],
        [314, 107, 70, 190, 0, 25, 108, 182],
        [294, 131, 86, 169, 25, 0, 84, 158],
        [269, 208, 172, 157, 108, 84, 0, 140],
        [391, 136, 152, 273, 182, 158, 140, 0],
]

print(tsp(distance_matrix))
assert tsp(distance_matrix)[1] == 1072