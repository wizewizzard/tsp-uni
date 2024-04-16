from random import uniform, randint


def path_with_arrows(p):
    path, path_len = p
    res = '[' + '->'.join([str(s) for s in path]) + ']'
    if path_len is not None:
        res += '=' + str(path_len)
    return res


def randomize_graph_fn(vertices_count, degree=1, max_weight=100):
    if vertices_count <= 0:
        raise ValueError(f"edges count must be greater or equal vertices_count-1")
    if degree < 1:
        raise ValueError(f"edges count must be lesser or equal to (vertices_count ** 2 - vertices_count) / 2")
    from networkx.generators.random_graphs import random_regular_graph
    gr = random_regular_graph(degree, vertices_count)
    gr = gr.to_undirected()
    matrix = [[0] * vertices_count for _ in range(vertices_count)]
    for (u, v) in gr.edges():
        matrix[u][v] = matrix[v][u] = random_weight()
    return matrix


def random_weight(lower=1, upper=100):
    return randint(lower, upper)
