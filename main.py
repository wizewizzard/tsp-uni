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
from netgraph import InteractiveGraph, Graph
from netgraph import EditableGraph
from netgraph._artists import NodeArtist, EdgeArtist
from graph import GraphBuilder
from ui.graph import MplCanvas
from ui.adjacency_matrix import AdjacencyMatrixQWidget
from ui.info import InfoOutput
from ui.command_menu import CommandMenu
from ui.generate_graph_popup import RandomizeGraphPopUp

matplotlib.use("Qt5Agg")

class MainWindow(Qt.QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.edit_mode = False
        self.graph = None
        self.initUI()
        self.show()

    def initUI(self):
        self.resize(1480, 1080)
        self.move(250, 0)
        self.title = 'Оптимизация задачи коммивояжера'
        self.central_widget = Qt.QWidget()
        main_layout = Qt.QHBoxLayout()
        button_layout = Qt.QVBoxLayout()
        col1 = Qt.QVBoxLayout()
        col2 = Qt.QVBoxLayout()
        col3 = Qt.QGridLayout()
        col1_widget = Qt.QWidget()
        col2_widget = Qt.QWidget()
        col3_widget = Qt.QWidget()
        col1_widget.setFixedWidth(300)
        col3_widget.setFixedWidth(300)
        col1_widget.setLayout(col1)
        col2_widget.setLayout(col2)
        col3_widget.setLayout(col3)

        self.init_calc_buttons(button_layout)
        button_layout.addWidget(CommandMenu(parent=self))

        self.info_box = InfoOutput()
        self.table = AdjacencyMatrixQWidget()
        self.canvas = MplCanvas(parent=self, width=8, height=8, dpi=100)
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        self.canvas.mpl_connect('draw_event', self.on_canvas_redraw)
        col1.addLayout(button_layout)
        col2.addWidget(self.canvas)
        col3.addWidget(self.table, 1, 0, 3, 1)
        col3.addWidget(self.info_box, 4, 0, 8, 1)
        main_layout.addWidget(col1_widget)
        main_layout.addWidget(col2_widget)
        main_layout.addWidget(col3_widget)

        self.central_widget = Qt.QWidget()
        self.central_widget.setLayout(main_layout)
        
        self.setCentralWidget(self.central_widget)

    def init_calc_buttons(self, layout):
        # buttons section
        all_paths = Qt.QPushButton('Все пути')
        all_paths.clicked.connect(self.calc_all_paths)
        layout.addWidget(all_paths)
        brute_force_button = Qt.QPushButton('Полный перебор')
        brute_force_button.clicked.connect(self.calc_with_brute_force)
        layout.addWidget(brute_force_button)
        greedy_button = Qt.QPushButton('Жадный алгоритм')
        greedy_button.clicked.connect(self.calc_with_greedy_search)
        layout.addWidget(greedy_button)
        
    def on_canvas_redraw(self, event):
        if hasattr(self.canvas, 'graph') and self.canvas.graph:
            # for edge in self.canvas.graph.edges:
            #         if edge in self.canvas.graph.edge_label_artists and self.canvas.graph.edge_label_artists[edge].get_text():
            #             self.canvas.weights[edge] = float(self.canvas.graph.edge_label_artists[edge].get_text())
            #         else:
            #             self.canvas.weights[edge] = str(random_weight())
                        # self.canvas.graph.edge_label_artists[edge]._text = str(random_weight())
            self.print_graph_adjacency_matrix()
    
    def output_to_info(self, text):
        self.info_box.append(text)

    #подсчет всех путей
    def calc_all_paths(self):
        print(f"calculating all paths...")
        self.canvas.highlight_path([0, 5, 20, 10, 15, 0])

    # полный перебор
    def calc_with_brute_force(self):
        print(f"calculating all paths...")
        gb = GraphBuilder(adjacent_matrix=self.graph_to_adjacent_matrix())
        graph = gb.build()
        from brute_force import BruteForce
        paths, len = BruteForce().tsp(matrix=graph)
        self.output_to_info(
            f"length: {len}\n" + str(paths))
        self.output_to_info("bebebebeb")

    # жадный перебор
    def calc_with_greedy_search(self):
        print(f"calculating with greedy search...")

    # динамическое программирование
    def calc_with_dynamic_programming(self):
        print(f"calculating with dynamic programming...")

    def set_graph(self, graph):
        self.canvas.set_graph(graph)
            
    def print_graph_adjacency_matrix(self):
        if not hasattr(self.canvas, 'graph') and not self.canvas:
            return
        matrix = self.canvas.get_adjacency_matrix()
        self.table.set_matrix(matrix)  

    def print_error(self, error):
        self.output_to_info(f"Error: {error}")

    def graph_to_adjacent_matrix(self):
        matrix = [[None for i in range(len(self.canvas.graph.node_artists))] for j in range(len(self.canvas.graph.node_artists))]
        for edge in self.canvas.graph.edges:
            matrix[edge[0]][edge[1]] = matrix[edge[1]][edge[0]] = float(self.canvas.weights[edge])
        return matrix        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    with open("./qss/macos.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()