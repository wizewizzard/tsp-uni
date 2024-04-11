import numpy as np
import sys

def tsp_branch_and_bound(graph):
    n = len(graph)
    INF = sys.maxsize

    def reduce_matrix(graph, row, col):
        for i in range(n):
            if i != row and graph[i][col] != INF:
                min_val = INF
                for j in range(n):
                    if j != col and graph[i][j] < min_val:
                        min_val = graph[i][j]
                graph[i][col] -= min_val

        for j in range(n):
            if j != col and graph[row][j] != INF:
                min_val = INF
                for i in range(n):
                    if i != row and graph[i][j] < min_val:
                        min_val = graph[i][j]
                graph[row][j] -= min_val

    def branch_and_bound(graph, level, path, bound, cost):
        nonlocal min_cost, final_path

        if level == n:
            if graph[path[level - 1]][path[0]] != INF:
                curr_cost = cost + graph[path[level - 1]][path[0]]
                if curr_cost < min_cost:
                    min_cost = curr_cost
                    final_path = path.copy()
            return

        for i in range(n):
            if not visited[i] and graph[path[level-1]][i] != INF:
                temp = bound
                cost += graph[path[level-1]][i]
                bound -= ((min(graph[path[level-1]]) + min([row[i] for row in graph])) / 2)
                if cost + bound < min_cost:
                    path[level] = i
                    visited[i] = True
                    branch_and_bound(graph, level+1, path, bound, cost)
                cost -= graph[path[level-1]][i]
                bound = temp
                visited = [False] * n
                for j in range(level):
                    visited[path[j]] = True

    for i in range(n):
        reduce_matrix(graph, i, 0)

    path = [-1] * (n+1)
    visited = [False] * n
    visited[0] = True
    path[0] = 0
    min_cost = INF
    final_path = []

    branch_and_bound(graph, 1, path, 0, 0)

    return min_cost, final_path

# Пример использования
INF = sys.maxsize
graph = np.array([[INF, 10, 15, 20],
                   [10, INF, 35, 25],
                   [15, 35, INF, 30],
                   [20, 25, 30, INF]])

min_cost, final_path = tsp_branch_and_bound(graph)
print("Минимальная стоимость коммивояжера:", min_cost)
print("Оптимальный путь коммивояжера:", final_path)
