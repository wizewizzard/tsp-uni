from netgraph import EditableGraph
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=10, dpi=2):
        super(MplCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)
    
    def set_matrix(self, adjacency_matrix):
        edges = []
        for i in range(len(adjacency_matrix)):
            for j in range(i, len(adjacency_matrix)):
                if adjacency_matrix[i][j] > 0:
                    edges.append([i, j, adjacency_matrix[i][j]])
        self.figure.clf()
        self.ax = self.figure.add_subplot(111, position=[0, 0, 1.0, 1.0])
        self.graph = None
        self.path_memo = {}
        self.graph = EditableGraph(edges, 
                                   ax=self.ax, 
                                   node_labels=True,
                                   node_layout='spring',
                                   scale=[1.5, 1.5],
                                   edge_width=0.5,
                                   edge_label_fontdict=dict(size=0),
                                   )
        self.figure.canvas.draw_idle()
        
    def highlight_path(self, path):
        self.path_memo = {}
        for i in range(len(path) - 1):
            edge = (path[i], path[(i + 1)]) if (path[i], path[(i + 1)]) in self.graph.edge_artists else (path[(i + 1)], path[i])
            self.path_memo[edge] = {
                "width": self.graph.edge_artists[edge].width,
                "alpha": self.graph.edge_artists[edge].get_alpha(),
                "color": self.graph.edge_artists[edge].get_edgecolor()
            }
            self.graph.edge_artists[edge].update_width(1.5 * 1e-2)
            self.graph.edge_artists[edge].set_alpha(1.0)
            # self.graph.edge_artists[edge].set_linewidth(0.006)
            self.graph.edge_artists[edge].set_color('red')
        self.figure.canvas.draw_idle()

    def remove_path_highlight(self):
        if self.path_memo == None:
            return
        path = self.path_memo
        for edge, props in self.path_memo.items():
            self.graph.edge_artists[edge].update_width(props['width'])
            self.graph.edge_artists[edge].set_alpha(props['alpha'])
            self.graph.edge_artists[edge].set_color(props['color'])
        self.figure.canvas.draw_idle()
        self.path_memo = None
