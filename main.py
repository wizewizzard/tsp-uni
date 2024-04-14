import sys
import time
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5 import Qt, QtCore
import matplotlib
from random import uniform
from config import get_config
from components.algorithm_menu import AlgorithmMenu
from components.graph import MplCanvas
from components.adjacency_matrix import AdjacencyMatrixQWidget
from components.greedy_algorithm_pop import GreedyAlgorithmPopUp
from components.info import InfoOutput
from components.command_menu import CommandMenu
from algorithms.brute_force import BruteForce
from algorithms.greedy import Greedy
from algorithms.all_paths import AllPaths
from utils import path_with_arrows

matplotlib.use("Qt5Agg")

class MainWindow(Qt.QMainWindow):
    
    def __init__(self, cfg, parent=None):
        super(MainWindow, self).__init__(parent)
        self.edit_mode = False
        self.initUI(cfg)
        self.show()
        self.G = None

    def initUI(self, cfg):
        self.resize(cfg['size']['width'], cfg['size']['height'])
        self.move(cfg['pos']['x'], cfg['pos']['y'])
        self.title = cfg['text']['main_window_title']
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

        button_layout.addWidget(CommandMenu(parent=self, cfg=cfg))
        button_layout.addWidget(AlgorithmMenu(parent=self, cfg=cfg))

        self.info_box = InfoOutput(parent=self)
        self.table = AdjacencyMatrixQWidget(parent=self)
        self.canvas = MplCanvas(parent=self, width=8, height=8, dpi=100)
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
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

    #подсчет всех путей
    def calc_all_paths(self):
        if self.G == None:
            self.output_error(f"Создайте граф.")
            return
        self.output_to_info(f"Вычисление набора всех путей...")
        ap = AllPaths()
        try:
            self.canvas.remove_path_highlight()
            paths = ap.all_paths(self.G)
            for (p, l) in paths:
                self.output_to_info(path_with_arrows((p, round(l, 1))))
        except Exception as err:
            self.output_error(f"Вычисление набора всех путей завершилось с ошибкой.")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")

        
    # полный перебор
    def calc_with_brute_force(self):
        if self.G == None:
            self.output_error(f"Создайте граф.")
            return
        self.output_to_info(f"Вычисление кратчайшего пути полным перебором...")
        try:
            self.canvas.remove_path_highlight()
            path, len = BruteForce().tsp(matrix=self.G)
            self.canvas.highlight_path(path)
            self.output_to_info(path_with_arrows((path, round(len, 1))))
            self.output_to_info(f"Вычисление кратчайшего пути полным перебором завершено.")
        except Exception as err:
            self.output_error(f"Вычисление кратчайшего пути полным перебором завершилось с ошибкой.")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")


    # жадный перебор
    def calc_with_greedy_search(self):
        if self.G == None:
            self.output_error(f"Создайте граф.")
            return
        self.output_to_info(f"calculating with greedy search...")
        try:
            self.canvas.remove_path_highlight()
            w = GreedyAlgorithmPopUp(vertex_count=len(self.canvas.graph.nodes))
            start_vertex = w.getResults()
            path, path_len = Greedy().tsp(matrix=self.G, start=start_vertex)
            self.canvas.highlight_path(path)
            self.output_to_info(path_with_arrows((path, round(path_len, 1))))
            self.output_to_info(f"Вычисление кратчайшего пути жадным алгоритмом завершено.")
        except Exception as err:
            self.output_error(f"Вычисление кратчайшего пути жадным алгоритмом завершилось с ошибкой.")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")

    # динамическое программирование
    def calc_with_dynamic_programming(self):
        self.output_to_info(f"calculating with dynamic programming...")

    # graph update
    def update_graph(self, matrix):
        if self.G == None:
            self.output_error(f"Создайте граф.")
            return
        

        self.canvas.set_matrix(self.G)
        self.table.set_matrix(self.G)    

    # рандомный граф
    def randomize_graph(self, vertex_count, degree):
        start = time.time()
        self.G = randomize_graph_fn(vertex_count, degree)
        end = time.time()
        self.canvas.set_matrix(self.G)
        self.table.set_matrix(self.G)     
        self.output_to_info(f"Graph was generated in {end - start}s")

    def output_error(self, error):
        self.output_to_info(f"<span style=\" font-weight:600; color:#ff0000;\" >{error}</span>")
    
    def output_to_info(self, text):
        self.info_box.append(text)    


def randomize_graph_fn(vertices_count, degree = 1, max_weight = 100):
    if vertices_count <= 0:
        raise ValueError(f"edges count must be greater or equal vertices_count-1")
    if degree < 1:
        raise ValueError(f"edges count must be lesser or equal to (vertices_count ** 2 - vertices_count) / 2")
    from networkx.generators.random_graphs import random_regular_graph
    gr = random_regular_graph(degree, vertices_count)
    gr = gr.to_undirected()
    matrix = [[0] * vertices_count for _ in range(vertices_count)]
    for (u,v) in gr.edges():
        matrix[u][v] = matrix[v][u] = random_weight()
    return matrix

def random_weight(lower=1, upper=100):
    return round(uniform(lower,upper), 1)

def main():
    cfg = get_config()
    app = QApplication(sys.argv)
    window = MainWindow(cfg=cfg)
    with open("./qss/macos.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()