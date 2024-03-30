from sys import maxsize 
from itertools import permutations
import graph

def tsp(graph):
    n = len(graph)
    min_paths = []
    min_length = float('inf')

    for path in permutations(range(1, n)):
        current_length = 0
        prev = 0
        for node in path:
            current_length += graph[prev][node]
            prev = node
        current_length += graph[prev][0]  # Добавляем расстояние от последнего узла к начальному

        if current_length < min_length:
            min_length = current_length
            min_paths = [(0,) + path + (0,)]
        elif min_length == current_length:
            min_paths.append((0,) + path + (0,))

    return min_paths, min_length

class BruteForce:
    def tsp(self, graph):
        return tsp(graph.as_adjacency_matrix())

brute_force = BruteForce()
route, dist = brute_force.tsp(graph.Graph(3, [
     [0, 1, 2.5],
     [1, 2, 4],
     [2, 0, 0.3]
]))
print(route)
assert dist == 6.8, "Should be 6.8"

route, dist = brute_force.tsp(graph.Graph(4, [
     [0, 1, 2],
     [1, 2, 4],
     [2, 3, 3],
     [3, 0, 2],
     [0, 2, 1],
     [1, 3, 2]
]))
print(route)
assert dist == 8, "Should be 8"

gb = graph.GraphBuilder(vertex_count=4)
gb.add_edge(0, 1, 1).add_edge(1, 2, 1).add_edge(2, 3, 1).add_edge(3, 0, 1).add_edge(0, 2, 1).add_edge(1, 3, 1)

route, dist = brute_force.tsp(gb.build())
print(route)
assert dist == 4, "Should be 4"

