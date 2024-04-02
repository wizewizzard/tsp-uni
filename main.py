import sys
import graph
from PyQt5.QtWidgets import QApplication
from PyQt5 import Qt, QtCore
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
from random import randint, random
import time
from netgraph import InteractiveGraph
from netgraph import EditableGraph
from netgraph._artists import NodeArtist, EdgeArtist

matplotlib.use("Qt5Agg")

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=10, dpi=100):
        super(MplCanvas, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)

    def set_graph(self, graph, weights):
        self.figure.clf()
        self.ax = self.figure.add_subplot(111, position=[0, 0, 1.0, 1.0])
        self.weights = weights
        self.graph = EditableGraph(graph, ax=self.ax, edge_labels=self.weights)

    def get_edges(self):
        from pprint import pprint
        for key in self.graph.edge_artists:
                pprint(key)
                pprint(self.graph.edge_label_artists[key].get_text())
            
        self.graph.edge_label_artists

        return 

class MainWindow(Qt.QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.edit_mode = False
        self.graph = None
        self.initUI()
        self.show()

    def initUI(self):
        self.resize(1280, 1080)
        self.move(250, 0)
        self.title = 'Оптимизация задачи коммивояжера'
        self.central_widget = Qt.QWidget()
        main_layout = Qt.QHBoxLayout()
        button_layout = Qt.QVBoxLayout()
        left_column = Qt.QVBoxLayout()
        right_column = Qt.QVBoxLayout()

        self.init_cmd_buttons(button_layout)
        self.init_calc_buttons(button_layout)

        self.info_box = Qt.QPlainTextEdit()
        self.info_box.setReadOnly(True)
        right_column.addWidget(self.info_box)
        self.table = Qt.QTableWidget()
        right_column.addWidget(self.table)
        left_column.addLayout(button_layout)
        main_layout.addLayout(left_column)
        main_layout.addLayout(right_column)
        self.central_widget = Qt.QWidget()
        self.central_widget.setLayout(main_layout)
        self.canvas = MplCanvas(parent=self, width=8, height=8, dpi=100)
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        self.canvas.mpl_connect('draw_event', self.on_canvas_redraw)
        left_column.addWidget(self.canvas)
        self.setCentralWidget(self.central_widget)

    def init_cmd_buttons(self, layout):
        randomize_graph_btn = Qt.QPushButton('Рандомный граф')
        randomize_graph_btn.clicked.connect(self.randomize_graph)
        layout.addWidget(randomize_graph_btn)
        # adjacency_matrix_btn = Qt.QPushButton('Матрица смежности')
        # adjacency_matrix_btn.clicked.connect(self.print_graph_adjacency_matrix)
        # layout.addWidget(adjacency_matrix_btn)

    def init_calc_buttons(self, layout):
        # buttons section
        brute_force_button = Qt.QPushButton('Полный перебор')
        brute_force_button.clicked.connect(self.calc_with_brute_force)
        layout.addWidget(brute_force_button)
        greedy_button = Qt.QPushButton('Жадный алгоритм')
        greedy_button.clicked.connect(self.calc_with_greedy_search)
        layout.addWidget(greedy_button)
        
    def on_canvas_redraw(self, event):
        # from pprint import pprint
        # pprint((vars(self.canvas.graph)))
        if hasattr(self.canvas, 'graph'):
            for key in self.canvas.graph.edge_artists:
                    if self.canvas.graph.edge_label_artists[key].get_text():
                        self.canvas.weights[key] = float(self.canvas.graph.edge_label_artists[key].get_text())
            self.print_graph_adjacency_matrix()
        
    
    def output_to_info(self, text):
        self.info_box.setPlainText(text)

    def toggle_edit_mode(self):
        if False:
            print(f"editing mode is already toggled")
            return
        self.edit_mode = not self.edit_mode

    #подсчет всех путей
    def calc_all_paths(self):
        print(f"calculating all paths...")

    # полный перебор
    def calc_with_brute_force(self):
        print(f"calculating all paths...")
        self.canvas.get_edges()

        # from brute_force import bf
        # paths, len = bf.tsp(self.graph)
        # self.output_to_info(
        #     f"length: {len}\n" + paths.__str___())
        # self.output_to_info("bebebebeb")

    # жадный перебор
    def calc_with_greedy_search(self):
        print(f"calculating with greedy search...")

    # динамическое программирование
    def calc_with_dynamic_programming(self):
        print(f"calculating with dynamic programming...")

    def randomize_graph(self):
        vertices_count = 5
        start = time.time()
        graph, weights = randomize_graph(10, 40)
        end = time.time()
        self.output_to_info(f"Graph was generated in {end - start}s")
        self.canvas.set_graph(graph, weights)
            

    def print_graph_adjacency_matrix(self):
        if not hasattr(self.canvas, 'graph'):
            return
        matrix = [[0 for i in range(len(self.canvas.graph.node_artists))] for j in range(len(self.canvas.graph.node_artists))]
        self.table.setColumnCount(len(self.canvas.graph.node_artists))  
        self.table.setRowCount(len(self.canvas.graph.node_artists))   
        self.table.setHorizontalHeaderLabels([str(i) for i in range(len(self.canvas.graph.node_artists))])
        self.table.setVerticalHeaderLabels([str(i) for i in range(len(self.canvas.graph.node_artists))])
        for i in range(len(self.canvas.graph.node_artists)):
            for j in range(len(self.canvas.graph.node_artists)):
                self.table.setItem(i, j, Qt.QTableWidgetItem(str(matrix[i][j])))
        self.table.resizeColumnsToContents()

    def print_error(self, error):
        self.output_to_info(f"Error: {error}")

    def ui_monitoring(self):
        print(f"edit mode: {self.edit_mode}")


# def randomize_graph(vertices_count, edges_count, min_weight = 1, max_weight = 100):
#     gb = graph.GraphBuilder(vertex_count=vertices_count)
#     if edges_count < vertices_count - 1:
#         raise ValueError(f"edges count must be greater or equal vertices_count-1")
#     if edges_count > (vertices_count ** 2 - vertices_count) / 2:
#         raise ValueError(f"edges count must be lesser or equal to (vertices_count ** 2 - vertices_count) / 2")
#     from networkx.generators.random_graphs import erdos_renyi_graph
#     g = erdos_renyi_graph(vertices_count, edges_count * 2 / (vertices_count ** 2 - vertices_count) / 2)
#     for n in g.edges:
#         gb.add_edge(n[0], n[1], randint(min_weight, max_weight))
    
#     return gb.build()
        

def randomize_graph(vertices_count, edges_count, min_weight = 1, max_weight = 100):
    gb = graph.GraphBuilder(vertex_count=vertices_count)
    if edges_count < vertices_count - 1:
        raise ValueError(f"edges count must be greater or equal vertices_count-1")
    if edges_count > (vertices_count ** 2 - vertices_count) / 2:
        raise ValueError(f"edges count must be lesser or equal to (vertices_count ** 2 - vertices_count) / 2")
    from networkx.generators.random_graphs import erdos_renyi_graph
    gr = erdos_renyi_graph(vertices_count, edges_count * 2 / (vertices_count ** 2 - vertices_count) / 2)
    weights = {}
    for edge in gr.edges:
        weights[edge] = "228"
    return gr, weights

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()