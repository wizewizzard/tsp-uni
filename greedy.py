from sys import maxsize 
from itertools import permutations
import graph
from typing import DefaultDict

INT_MAX = 2147483647
 
class Greedy:
    def tsp(self, graph):
        return greedy(graph.as_adjacency_matrix())

# Function to find the minimum
# cost path for all the paths
def greedy(tsp):
    sum = 0
    counter = 0
    j = 0
    i = 0
    min = INT_MAX
    visitedRouteList = DefaultDict(int)
 
    # Starting from the 0th indexed
    # city i.e., the first city
    visitedRouteList[0] = 1
    route = [0] * len(tsp)
 
    # Traverse the adjacency
    # matrix tsp[][]
    while i < len(tsp) and j < len(tsp[i]):
 
        # Corner of the Matrix
        if counter >= len(tsp[i]) - 1:
            break
 
        # If this path is unvisited then
        # and if the cost is less then
        # update the cost
        if j != i and (visitedRouteList[j] == 0):
            if tsp[i][j] < min:
                min = tsp[i][j]
                route[counter] = j + 1
 
        j += 1
 
        # Check all paths from the
        # ith indexed city
        if j == len(tsp[i]):
            sum += min
            min = INT_MAX
            visitedRouteList[route[counter] - 1] = 1
            j = 0
            i = route[counter] - 1
            counter += 1
 
    i = route[counter - 1] - 1
 
    for j in range(len(tsp)):
 
        if (i != j) and tsp[i][j] < min:
            min = tsp[i][j]
            route[counter] = j + 1
 
    sum += min

    return [0, ] + route + [0, ], sum

greedy_algorithm = Greedy()
gb = graph.GraphBuilder(vertex_count=3)
gb.add_edge(0, 1, 2.5).add_edge(1, 2, 4).add_edge(2, 0, 0.3)
route, dist = greedy_algorithm.tsp(gb.build())
assert dist == 6.8, "Should be 6.8"

gb = graph.GraphBuilder(vertex_count=4)
gb.add_edge(0, 1, 2).add_edge(1, 2, 4).add_edge(2, 3, 3).add_edge(3, 0, 2).add_edge(0, 2, 1).add_edge(1, 3, 2)
route, dist = greedy_algorithm.tsp(gb.build())
assert dist == 8, "Should be 8"

gb = graph.GraphBuilder(vertex_count=4)
gb.add_edge(0, 1, 1).add_edge(1, 2, 1).add_edge(2, 3, 1).add_edge(3, 0, 1).add_edge(0, 2, 1).add_edge(1, 3, 1)

route, dist = greedy_algorithm.tsp(gb.build())
print(route)
assert dist == 4, "Should be 4"
