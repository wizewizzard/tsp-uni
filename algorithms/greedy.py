from sys import maxsize 

INT_MAX = 2147483647
 
class Greedy:
    def tsp(self, matrix, start = 0):
        return tsp(matrix, start)

def tsp(matrix, start):
    path = []
    visited = [0] * len(matrix)
    cost = 0
    g_start = start
    for i in range(len(matrix)):
        visited[start] = 1
        adj_vertex = -1
        min_val = maxsize
        path.append(start)
        for k in range(len(matrix)):
            if (matrix[start][k] != 0) and (visited[k] == 0):
                if matrix[start][k] < min_val:
                    min_val = matrix[start][k]
                    adj_vertex = k
        if adj_vertex == -1:
            adj_vertex = 0
            path.append(g_start)
            cost += matrix[start][g_start]
            return path, cost
        cost += matrix[start][adj_vertex]
        start = adj_vertex

greedy_algorithm = Greedy()
matrix = [
    [0, 2.5, 0.3], 
    [2.5, 0, 4], 
    [0.3, 4, 0]
]
route, dist = greedy_algorithm.tsp(matrix)
print(dist)
assert dist == 6.8, "Should be 6.8"

matrix = [
    [0, 2, 1, 2], 
    [2, 0, 4, 2], 
    [1, 4, 0, 3],
    [2, 2, 3, 0]
]
route, dist = greedy_algorithm.tsp(matrix)
assert dist == 8, "Should be 8"

matrix = [
    [0, 1, 1, 1], 
    [1, 0, 1, 1], 
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
route, dist = greedy_algorithm.tsp(matrix)
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

print(greedy_algorithm.tsp(distance_matrix))
assert greedy_algorithm.tsp(distance_matrix)[1] == 1126