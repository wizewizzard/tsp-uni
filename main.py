import sys
import threading
import time
import traceback
from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget, QLabel
from PyQt5 import Qt, QtCore
from PyQt5.QtCore import QThreadPool, QRunnable
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from algorithms.bnb import BnB
from algorithms.dynamic_programming import DynamicProgramming
from components.conversion_window import ConversionWindow, ConversionPointEvent
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
from utils import randomize_graph_fn
import numpy as np

matplotlib.use("Qt5Agg")


class BnBEvent:
    def __init__(self, current_path, current_result, time_elapsed, completed):
        self.current_path = current_path
        self.current_result = current_result
        self.time_elapsed = time_elapsed
        self.completed = completed


class CommunicateBnB(QtCore.QObject):
    progress = QtCore.pyqtSignal(BnBEvent)
    stop_signal = QtCore.pyqtSignal(bool)
    point = QtCore.pyqtSignal(ConversionPointEvent)

class MainWindow(Qt.QMainWindow):

    def __init__(self, cfg, parent=None):
        super(MainWindow, self).__init__(parent)
        self.current_calculation = None
        self.cfg = cfg
        self.communicate = CommunicateBnB()
        self.communicate.progress.connect(self.accumulate_bnb_results)
        self.communicate.stop_signal.connect(self.stop_calculation)
        self.threadpool = QThreadPool()
        self.initUI(cfg)
        self.setWindowTitle('Методы оптимизации')
        self.show()
        self.G = None
        self.bnb_runner = None
        self.conversion_window = None


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
            start = time.time()
            paths = ap.all_paths(self.G)
            end = time.time()
            for (p, l) in paths:
                self.output_to_info(path_with_arrows((p, round(l, 1))))
            self.output_to_info(f"Вычисление набора всех путей завершено", end - start)
        except Exception as err:
            self.output_error(f"Вычисление набора всех путей завершилось с ошибкой")
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
            start = time.time()
            path, path_len = BruteForce().tsp(matrix=self.G)
            end = time.time()
            self.canvas.highlight_path(path)
            self.output_to_info(path_with_arrows((path, round(path_len, 1))))
            self.output_to_info(f"Вычисление кратчайшего пути полным перебором завершено", end - start)
        except Exception as err:
            self.output_error(f"Вычисление кратчайшего пути полным перебором завершилось с ошибкой")
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
            start = time.time()
            path, path_len = Greedy().tsp(matrix=self.G, start=start_vertex)
            end = time.time()
            self.canvas.highlight_path(path)
            self.output_to_info(path_with_arrows((path, round(path_len, 1))))
            self.output_to_info(f"Вычисление кратчайшего пути жадным алгоритмом завершено", end - start)
        except Exception as err:
            self.output_error(f"Вычисление кратчайшего пути жадным алгоритмом завершилось с ошибкой")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")

    # динамическое программирование
    def calc_with_dynamic_programming(self):
        if self.G == None:
            self.output_error(f"Создайте граф.")
            return
        self.output_to_info(f"Вычисление кратчайшего пути с помощью динамического программирования...")
        try:
            self.canvas.remove_path_highlight()
            start = time.time()
            path, path_len = DynamicProgramming().tsp(matrix=self.G)
            end = time.time()
            self.canvas.highlight_path(path)
            self.output_to_info(path_with_arrows((path, round(path_len, 1))))
            self.output_to_info(f"Вычисление кратчайшего пути с помощью динамического программирования завершено",
                                end - start)
        except Exception as err:
            self.output_error(
                f"Вычисление кратчайшего пути с помощью динамического программирования завершилось с ошибкой")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")

    def calc_with_branch_and_bound(self):
        if self.G == None:
            self.output_error(f"Создайте граф.")
            return
        self.output_to_info(f"Вычисление кратчайшего пути методом ветвей и границ...")
        # self.canvas.remove_path_highlight()
        try:
            self.conversion_window = ConversionWindow(communication=self.communicate, cfg=self.cfg)
            self.bnb_runner = BnBRunner(bnb=BnB(self.G), communicate=self.communicate)
            self.threadpool.start(self.bnb_runner)
        except Exception as err:
            self.output_error(
                f"Вычисление кратчайшего пути методом ветвей и границ завершилось с ошибкой.")
            traceback.print_exception(*sys.exc_info())
            print(f"Unexpected {err=}, {type(err)=}")

    def accumulate_bnb_results(self, progress):
        print(
            f"Current res: {progress.current_path} - {progress.current_result}. Completed: {progress.completed}. Time elapsed: {round(progress.time_elapsed, 3)}")
        self.communicate.point.emit(ConversionPointEvent(x=progress.time_elapsed, y=progress.current_result, terminate=progress.completed))
        if progress.time_elapsed > 3 and progress.completed is not True and self.conversion_window is not None:
            self.conversion_window.show()
        if progress.completed:
            self.canvas.highlight_path(progress.current_path)
            self.output_to_info(path_with_arrows((progress.current_path, progress.current_result)))
            self.output_to_info(f"Вычисление кратчайшего пути методом ветвей и границ завершено.",
                                progress.time_elapsed)

    def stop_calculation(self, event):
        if self.bnb_runner is not None:
            self.bnb_runner.stopped = True
        # self.conversion_window = None

    # graph update
    def update_graph(self, matrix):
        if self.G == None:
            self.output_error(f"Создайте граф.")
            return

        self.G = matrix
        self.canvas.set_matrix(self.G, recreate=False)
        self.table.set_matrix(self.G)

    # рандомный граф
    def randomize_graph(self, vertex_count, degree):
        start = time.time()
        self.G = randomize_graph_fn(vertex_count, degree)
        end = time.time()
        self.canvas.set_matrix(self.G)
        self.table.set_matrix(self.G)
        self.output_to_info("Граф был сгенерирован.", end - start)

    def output_error(self, error):
        self.output_to_info(f"<span style=\" font-weight:600; color:#ff0000;\" >{error}</span>")

    def output_to_info(self, text, elapsed_time=None):
        if elapsed_time is not None:
            self.info_box.append(f"{text}. Время выполнения: {round(elapsed_time, 3)}мс")
        else:
            self.info_box.append(text)


class BnBRunner(QRunnable):
    def __init__(self, bnb, communicate):
        super().__init__()
        self.bnb = bnb
        self.communicate = communicate
        self.stopped = True

    def run(self):
        print(f"BnbRunner: {threading.get_ident() }")
        self.stopped = False
        start = time.time()
        self.bnb.start()
        probe_times = np.logspace(start=4, stop=0, base=0.1, num=100, endpoint=True) * 3600
        i = 0
        while self.bnb.is_alive() and self.stopped is False and i < 100:
            print(f'tick {self.stopped}')
            self.communicate.progress.emit(
                BnBEvent(self.bnb.final_path, self.bnb.final_res, time.time() - start, False))
            self.bnb.join(probe_times[i])
            i+=1
        self.bnb.stopped = True
        self.bnb.join()
        end = time.time()
        self.communicate.progress.emit(BnBEvent(self.bnb.final_path, self.bnb.final_res, end - start, True))


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
