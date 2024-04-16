from random import random

import numpy as np
import sys

class BranchAndBound:
    def __init__(self):
        pass

    def tsp(self, matrix):
        return tsp_branch_and_bound1(matrix)

def tsp_branch_and_bound1(distances):
    def calculate_bound(path):
        bound = 0
        for i in range(len(path)):
            if i < len(path) - 1:
                bound += distances[path[i]][path[i+1]]
            else:
                bound += distances[path[i]][path[0]]
        for i in range(len(distances)):
            if i not in path:
                bound += min([distances[i][j] for j in range(len(distances)) if j != i])
        return bound

    def branch_and_bound_helper(path, bound, length):
        nonlocal best_path, best_length
        if len(path) == len(distances):
            if length + distances[path[-1]][path[0]] < best_length:
                best_path = path[:]
                best_length = length + distances[path[-1]][path[0]]
        else:
            for i in range(len(distances)):
                if i not in path:
                    new_path = path + [i]
                    new_bound = calculate_bound(new_path)
                    if new_bound < best_length:
                        branch_and_bound_helper(new_path, new_bound, length + distances[path[-1]][i])

    best_path = []
    best_length = np.inf

    branch_and_bound_helper([1], calculate_bound([1]), 0)
    path = best_path + [best_path[0], ]
    return path, best_length

def tsp_stochastic_branch_and_bound(dist_matrix):
    n = len(dist_matrix)
    best_tour = []
    best_cost = np.inf

    def bound(tour):
        remaining = [i for i in range(n) if i not in tour]
        bound = sum(min(dist_matrix[i][j] for j in remaining) for i in tour)
        for i in remaining:
            min_to_i = min(dist_matrix[i][j] for j in remaining if j != i)
            bound += min_to_i
        return bound

    def dfs(node, visited, cost):
        nonlocal best_cost, best_tour

        if len(visited) == n:
            cost += dist_matrix[node][0]
            if cost < best_cost:
                best_cost = cost
                best_tour = visited + [0]
            return

        possible_cities = [i for i in range(n) if i not in visited]
        for city in possible_cities:
            new_cost = cost + dist_matrix[node][city]
            if new_cost + bound(visited + [city]) < best_cost:
                dfs(city, visited + [city], new_cost)

    dfs(0, [0], 0)

    return best_tour, best_cost


# Пример использования
algo = BranchAndBound()

graph = np.array([[0, 10, 15, 20],
                   [10, 0, 35, 25],
                   [15, 35, 0, 30],
                   [20, 25, 30, 0]])

matrix = [
    [0, 2.5, 0.3],
    [2.5, 0, 4],
    [0.3, 4, 0]
]
min_cost, final_path = algo.tsp(matrix)

route, dist = algo.tsp(matrix)
print(dist)
assert dist == 6.8, "Should be 6.8"

matrix = [
    [0, 2, 1, 2],
    [2, 0, 4, 2],
    [1, 4, 0, 3],
    [2, 2, 3, 0]
]
route, dist = algo.tsp(matrix)
assert dist == 8, "Should be 8"

matrix = [
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
route, dist = algo.tsp(matrix)
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

print(algo.tsp(distance_matrix))
assert algo.tsp(distance_matrix)[1] == 1098
