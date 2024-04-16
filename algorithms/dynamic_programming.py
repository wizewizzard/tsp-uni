import itertools
import sys


import sys

def tsp(dist):
    N = len(dist)
    dp = [[sys.maxsize] * N for _ in range(1 << N)]
    dp[1][0] = 0
    prev = [[-1] * N for _ in range(1 << N)]

    for mask in range(1, 1 << N):
        for j in range(1, N):
            if mask & (1 << j):
                for k in range(0, N):
                    if mask & (1 << k) and k != j:
                        if dp[mask - (1 << j)][k] + dist[k][j] < dp[mask][j]:
                            dp[mask][j] = dp[mask - (1 << j)][k] + dist[k][j]
                            prev[mask][j] = k

    min_cost = sys.maxsize
    last_city = -1
    for j in range(1, N):
        if dp[-1][j] + dist[j][0] < min_cost:
            min_cost = dp[-1][j] + dist[j][0]
            last_city = j

    path = []
    mask = (1 << N) - 1
    while last_city != -1:
        path.append(last_city)
        prev_city = prev[mask][last_city]
        mask -= (1 << last_city)
        last_city = prev_city

    path.reverse()
    path = path + [path[0], ]
    return path, min_cost

# def DP_TSP(distances_array):
#     n = len(distances_array)
#     all_points_set = set(range(n))
#
#     memo = {(tuple([i]), i): tuple([0, None]) for i in range(n)}
#     queue = [(tuple([i]), i) for i in range(n)]
#
#     while queue:
#         prev_visited, prev_last_point = queue.pop(0)
#         prev_dist, _ = memo[(prev_visited, prev_last_point)]
#
#         to_visit = all_points_set.difference(set(prev_visited))
#         for new_last_point in to_visit:
#             new_visited = tuple(sorted(list(prev_visited) + [new_last_point]))
#             new_dist = prev_dist + distances_array[prev_last_point][new_last_point]
#
#             if (new_visited, new_last_point) not in memo:
#                 memo[(new_visited, new_last_point)] = (new_dist, prev_last_point)
#                 queue += [(new_visited, new_last_point)]
#             else:
#                 if new_dist < memo[(new_visited, new_last_point)][0]:
#                     memo[(new_visited, new_last_point)] = (new_dist, prev_last_point)
#
#     optimal_path, optimal_cost = retrace_optimal_path(memo, n)
#     path = optimal_path + [optimal_path[0], ]
#     length = 0
#     for i in range(len(path) - 1):
#         length += distances_array[path[i]][path[i + 1]]
#     return path, length
#
#
# def retrace_optimal_path(memo: dict, n: int) -> [[int], float]:
#     points_to_retrace = tuple(range(n))
#
#     full_path_memo = dict((k, v) for k, v in memo.items() if k[0] == points_to_retrace)
#     path_key = min(full_path_memo.keys(), key=lambda x: full_path_memo[x][0])
#
#     last_point = path_key[1]
#     optimal_cost, next_to_last_point = memo[path_key]
#
#     optimal_path = [last_point]
#     points_to_retrace = tuple(sorted(set(points_to_retrace).difference({last_point})))
#
#     while next_to_last_point is not None:
#         last_point = next_to_last_point
#         path_key = (points_to_retrace, last_point)
#         _, next_to_last_point = memo[path_key]
#
#         optimal_path = [last_point] + optimal_path
#         points_to_retrace = tuple(sorted(set(points_to_retrace).difference({last_point})))
#
#     return optimal_path, optimal_cost


# Driver program to test above logic

class DynamicProgramming:
    def __init__(self):
        pass

    def tsp(self, matrix):
        path, length = tsp(matrix)
        # print("The cost of most efficient tour = " + str(ans))
        return path, length

#
# dp_algorithm = DynamicProgramming()
# matrix = [
#     [0, 2.5, 0.3],
#     [2.5, 0, 4],
#     [0.3, 4, 0]
# ]
# route, dist = dp_algorithm.tsp(matrix)
# print(dist)
# print(route)
#
# assert dist == 6.8, "Should be 6.8"
#
# matrix = [
#     [0, 2, 1, 2],
#     [2, 0, 4, 2],
#     [1, 4, 0, 3],
#     [2, 2, 3, 0]
# ]
# route, dist = dp_algorithm.tsp(matrix)
# print(route)
# assert dist == 8, "Should be 8"
#
# matrix = [
#     [0, 1, 1, 1],
#     [1, 0, 1, 1],
#     [1, 1, 0, 1],
#     [1, 1, 1, 0]
# ]
# route, dist = dp_algorithm.tsp(matrix)
# print(route)
# assert dist == 4, "Should be 4"
#
# distance_matrix = [
#     [0, 328, 259, 180, 314, 294, 269, 391],
#     [328, 0, 83, 279, 107, 131, 208, 136],
#     [259, 83, 0, 257, 70, 86, 172, 152],
#     [180, 279, 257, 0, 190, 169, 157, 273],
#     [314, 107, 70, 190, 0, 25, 108, 182],
#     [294, 131, 86, 169, 25, 0, 84, 158],
#     [269, 208, 172, 157, 108, 84, 0, 140],
#     [391, 136, 152, 273, 182, 158, 140, 0],
# ]
#
# print(dp_algorithm.tsp(distance_matrix))
# assert dp_algorithm.tsp(distance_matrix)[1] == 1072
