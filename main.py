import sys
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5 import Qt, QtCore
import matplotlib
from random import randint, random
from config import get_config
from ui.graph import MplCanvas
from ui.adjacency_matrix import AdjacencyMatrixQWidget
from ui.greedy_algorithm_pop import GreedyAlgorithmPopUp
from ui.info import InfoOutput
from ui.command_menu import CommandMenu
from ui.generate_graph_popup import RandomizeGraphPopUp
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
        self.graph = None

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

        self.init_calc_buttons(button_layout, cfg)
        button_layout.addWidget(CommandMenu(parent=self, cfg=cfg))

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

    def init_calc_buttons(self, layout, cfg):
        # buttons section
        all_paths = Qt.QPushButton(cfg['text']['all_paths_btn_text'])
        all_paths.clicked.connect(self.calc_all_paths)
        layout.addWidget(all_paths)
        brute_force_button = Qt.QPushButton(cfg['text']['bruteforce_btn_text'])
        brute_force_button.clicked.connect(self.calc_with_brute_force)
        layout.addWidget(brute_force_button)
        greedy_button = Qt.QPushButton(cfg['text']['greedy_btn_text'])
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
            # self.print_graph_adjacency_matrix()
            pass

    #подсчет всех путей
    def calc_all_paths(self):
        if not hasattr(self.canvas, 'graph') and not self.canvas:
            self.output_error(f"Создайте граф.")
            return
        self.output_to_info(f"Вычисление набора всех путей...")
        ap = AllPaths()
        try:
            self.canvas.remove_path_highlight()
            paths = ap.all_paths(self.canvas.get_adjacency_matrix())
            for p in paths:
                self.output_to_info(path_with_arrows(p))
        except Exception as err:
            self.output_error(f"Вычисление набора всех путей завершилось с ошибкой.")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")

        
    # полный перебор
    def calc_with_brute_force(self):
        if not hasattr(self.canvas, 'graph') and not self.canvas:
            self.output_error(f"Создайте граф.")
            return
        self.output_to_info(f"Вычисление кратчайшего пути полным перебором...")
        try:
            self.canvas.remove_path_highlight()
            path, len = BruteForce().tsp(matrix=self.canvas.get_adjacency_matrix())
            self.canvas.highlight_path(path)
            self.output_to_info(path_with_arrows((path, len)))
            self.output_to_info(f"Вычисление кратчайшего пути полным перебором завершено.")
        except Exception as err:
            self.output_error(f"Вычисление кратчайшего пути полным перебором завершилось с ошибкой.")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")


    # жадный перебор
    def calc_with_greedy_search(self):
        if not hasattr(self.canvas, 'graph') and not self.canvas:
            self.output_error(f"Создайте граф.")
            return
        self.output_to_info(f"calculating with greedy search...")
        try:
            self.canvas.remove_path_highlight()
            w = GreedyAlgorithmPopUp(vertex_count=len(self.canvas.graph.nodes))
            start_vertex = w.getResults()
            path, path_len = Greedy().tsp(matrix=self.canvas.get_adjacency_matrix(), start=start_vertex)
            self.canvas.highlight_path(path)
            self.output_to_info(path_with_arrows((path, path_len)))
            self.output_to_info(f"Вычисление кратчайшего пути жадным алгоритмом завершено.")
        except Exception as err:
            self.output_error(f"Вычисление кратчайшего пути жадным алгоритмом завершилось с ошибкой.")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")

    # динамическое программирование
    def calc_with_dynamic_programming(self):
        self.output_to_info(f"calculating with dynamic programming...")

    def set_graph(self, graph):
        self.canvas.set_graph(graph)
            
    def print_graph_adjacency_matrix(self):
        if not hasattr(self.canvas, 'graph') and not self.canvas:
            return
        matrix = self.canvas.get_adjacency_matrix()
        self.table.set_matrix(matrix)  

    def output_error(self, error):
        self.output_to_info(f"<span style=\" font-weight:600; color:#ff0000;\" >{error}</span>")
    
    def output_to_info(self, text):
        self.info_box.append(text)    

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