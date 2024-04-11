from itertools import permutations
import numpy as np

class AllPaths:
    def __init__(self) -> None:
        pass

    def all_paths(self, adjacency_matrix):
        paths_and_lengths = []
        for path in permutations(range(1, len(adjacency_matrix))):
            this_len = 0
            path = [0, ] + list(path) + [0, ]
            prev = path[0]
            for n in path:
                this_len += adjacency_matrix[prev][n]
                prev = n
            paths_and_lengths.append((path, this_len))
        
        return paths_and_lengths    
              
ap = AllPaths()
matrix = [[0, 2.5, 0.3], [2.5, 0, 4], [0.3, 4, 0]]
print(ap.all_paths(matrix))