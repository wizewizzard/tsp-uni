from PyQt5.QtWidgets import QWidget,QTextEdit,QVBoxLayout,QPushButton,QLineEdit,QHBoxLayout,QLabel
from PyQt5.QtGui import *
from random import randint, random
import time
from ui.generate_graph_popup import RandomizeGraphPopUp
from ui.build_graph_by_adjacency_matrix import BuildGraphByAjacencyMatrixPopUp

class CommandMenu(QWidget):
    def __init__(self,parent=None,
                set_graph_cb=None,
                output_info_cb=None):
        super().__init__(parent)

        self.parent = parent
        lbl = QLabel(self)
        lbl.setText('Command pallete')
        self.set_graph_cb = set_graph_cb
        self.output_info_cb = output_info_cb
        self.randomize_graph_btn = QPushButton("Generate")
        self.build_graph_graph_btn = QPushButton("Build by adj. matrix")
        self.help_btn = QPushButton("Help")
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        layout.addWidget(self.randomize_graph_btn)
        layout.addWidget(self.build_graph_graph_btn)
        layout.addWidget(self.help_btn)
        self.setLayout(layout)

        self.randomize_graph_btn.clicked.connect(self.randomize_graph_btn_clicked)
        self.build_graph_graph_btn.clicked.connect(self.build_graph_graph_btn_clicked)
        self.help_btn.clicked.connect(self.randomize_graph_btn_clicked)

    def build_graph_graph_btn_clicked(self):
        w = BuildGraphByAjacencyMatrixPopUp()
        matrix = w.getResults()

    def randomize_graph_btn_clicked(self):
        w = RandomizeGraphPopUp()
        vertex_count = w.getResults()
        if vertex_count and vertex_count > 1:
                start = time.time()
                graph = randomize_graph(vertex_count, vertex_count - 1)
                end = time.time()
                self.parent.set_graph(graph)
                self.parent.output_to_info(f"Graph was generated in {end - start}s")
    
    def help_btn_clicked(self):
        pass

def randomize_graph(vertices_count, degree = 1, max_weight = 100):
    if vertices_count <= 0:
        raise ValueError(f"edges count must be greater or equal vertices_count-1")
    if degree < 1:
        raise ValueError(f"edges count must be lesser or equal to (vertices_count ** 2 - vertices_count) / 2")
    from networkx.generators.random_graphs import random_regular_graph
    gr = random_regular_graph(degree, vertices_count)
    gr = gr.to_undirected()
    weights = {}
    for (u,v,w) in gr.edges(data=True):
        gr.edges[u,v]['weight'] = random_weight()
    return gr

def random_weight(lower=1, upper=100):
    return randint(lower, upper)