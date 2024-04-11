from sys import maxsize 
from itertools import permutations
import numpy as np

def tsp(matrix, start):
    n = len(matrix)
    min_path = []
    min_length = float('inf')

    for path in permutations([x for x in range(n) if x != start]):
        current_length = 0
        prev = 0
        path = path + (0, )
        for node in path:
            current_length += matrix[prev][node]
            prev = node
        current_length += matrix[prev][0]
        if current_length < min_length:
            min_length = current_length
            min_path = [0, ] + list(path)

    return min_path, min_length

class BruteForce:
    def tsp(self, matrix, start = 0):
        return tsp(matrix, start)


brute_force = BruteForce()

matrix = [
    [0, 2.5, 0.3], 
    [2.5, 0, 4], 
    [0.3, 4, 0]
]
route, dist = brute_force.tsp(matrix)
assert dist == 6.8, "Should be 6.8"

matrix = [
    [0, 2, 1, 2], 
    [2, 0, 4, 2], 
    [1, 4, 0, 3],
    [2, 2, 3, 0]
]
route, dist = brute_force.tsp(matrix)
assert dist == 8, "Should be 8"

matrix = [
    [0, 1, 1, 1], 
    [1, 0, 1, 1], 
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]
route, dist = brute_force.tsp(matrix)
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

assert brute_force.tsp(distance_matrix)[1] == 1072