class Graph:
    def __init__(self, vertices_count, edges) -> None:
        self.vertices_count = vertices_count
        self.adjacency_matrix = [[0] * vertices_count for x in range(vertices_count)]
        for edge in edges:
            i = edge[0]
            j = edge[1]
            weight = edge[2]
            self.adjacency_matrix[i][j] = weight
            self.adjacency_matrix[j][i] = weight

    def as_adjacency_matrix(self):
        return self.adjacency_matrix


# builds graph
class GraphBuilder:
    def __init__(self, graph=None, vertex_count=0) -> None:
        self.vertex_count = vertex_count
        self.edges = []

    def add_vertex(self):
        print(f"adding vertex...")
        self.vertex_count += 1
        return self

    def remove_vertex(self, index):
        print(f"removing vertex...")
        self.vertex_count -= 1
        self.edges = [
            [
                edge[0] - 1 if i > index else edge[0],
                edge[1] - 1 if i > index else edge[1],
                edge[2],
            ]
            for edge, i in self.edges
            if edge.from_vertex != index and edge.to_vertex != index
        ]
        return self

    def add_edge(self, vertex_from, vertex_to, weight):
        if vertex_from == vertex_to:
            raise ValueError("vertex source and dest must be different")
        self.edges.append([vertex_from, vertex_to, weight])
        return self

    def remove_edge(self, vertex_from, vertex_to):
        self.edges = [
            edge
            for edge in self.edges
            if (edge[0] != vertex_from and edge[1] != vertex_to)
            or (edge[1] != vertex_from and edge[0] != vertex_to)
        ]
        return self

    def modify_edge_weight(self, vertex_from, vertex_to, weight):
        edges = [
            edge
            for edge in self.edges
            if (edge[0] == vertex_from and edge[1] == vertex_to)
            or (edge[1] == vertex_from and edge[0] == vertex_to)
        ]
        if len(edges) == 0:
            raise ValueError(f"edge {vertex_from}->{vertex_to} was not found")
        for edge in edges:
            edge[2] = weight

    def build(self):
        return Graph(self.vertex_count, self.edges)
