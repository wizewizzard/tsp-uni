from PyQt5.QtWidgets import QWidget,QTextEdit,QVBoxLayout,QPushButton,QLineEdit,QHBoxLayout,QLabel
from PyQt5.QtGui import *
from random import randint, random
import time
from components.generate_graph_popup import RandomizeGraphPopUp
from components.build_graph_by_adjacency_matrix import BuildGraphByAjacencyMatrixPopUp

class CommandMenu(QWidget):
    def __init__(self,
                cfg,
                parent=None,
                set_graph_cb=None,
                output_info_cb=None):
        super().__init__(parent)

        self.parent = parent
        self.set_graph_cb = set_graph_cb
        self.output_info_cb = output_info_cb
        self.randomize_graph_btn = QPushButton(cfg['text']['randomize_graph_btn_text'])
        self.build_graph_graph_btn = QPushButton(cfg['text']['build_graph_graph_btn_text'])
        layout = QVBoxLayout()
        layout.addWidget(self.randomize_graph_btn)
        self.setLayout(layout)

        self.randomize_graph_btn.clicked.connect(self.randomize_graph_btn_clicked)
        self.build_graph_graph_btn.clicked.connect(self.build_graph_graph_btn_clicked)


    def build_graph_graph_btn_clicked(self):
        w = BuildGraphByAjacencyMatrixPopUp()
        matrix = w.getResults()

    def randomize_graph_btn_clicked(self):
        w = RandomizeGraphPopUp()
        vertex_count = w.getResults()
        if vertex_count and vertex_count > 1:
            self.parent.randomize_graph(vertex_count, vertex_count - 1)
                
    def help_btn_clicked(self):
        pass

