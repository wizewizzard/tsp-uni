from netgraph import EditableGraph
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=10, dpi=2):
        super(MplCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)
    
    def set_graph(self, graph):
        self.figure.clf()
        self.ax = self.figure.add_subplot(111, position=[0, 0, 1.0, 1.0])
        self.graph = None
        self.graph = EditableGraph(graph, 
                                   ax=self.ax, 
                                   node_labels=True,
                                   node_layout='spring',
                                   scale=[1.5, 1.5],
                                   edge_width=0.5,
                                   edge_label_fontdict=dict(size=0),
                                   edge_labels={(u,v):str(w['weight']) for u,v,w in graph.edges(data=True)},
                                   )
        self.figure.canvas.draw_idle()
        
    def highlight_path(self, path):
        for i in range(len(path) - 1):
            edge = (path[i], path[(i + 1)]) if (path[i], path[(i + 1)]) in self.graph.edge_artists else (path[(i + 1)], path[i])
            
            self.graph.edge_artists[edge].update_width(0.5 * 1e-2)
            self.graph.edge_artists[edge].set_alpha(1.0)
            self.graph.edge_artists[edge].set_label('90000')
            self.graph.edge_artists[edge].set_color('red')
        self.figure.canvas.draw_idle()

    def get_adjacency_matrix(self):
        matrix = [[0] * len(self.graph.nodes) for _ in range(len(self.graph.nodes)) ]
        for u, v in self.graph.edges:
            matrix[u][v] = matrix[v][u] = float(self.graph.edge_label_artists[(u, v)].get_text())
        return matrix