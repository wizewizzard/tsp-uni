from PyQt5.QtWidgets import QWidget,QTextEdit,QVBoxLayout,QPushButton,QLineEdit
from PyQt5.QtGui import *
from random import randint, random
import time

class CommandMenu(QWidget):
    def __init__(self,parent=None,
                set_graph_cb=None,
                output_info_cb=None):
        super().__init__(parent)
        self.parent = parent
        self.set_graph_cb = set_graph_cb
        self.output_info_cb = output_info_cb

        self.vertex_count_input = QLineEdit(self)
        self.vertex_count_input.setFixedWidth(40)
        self.vertex_count_input.setValidator(QIntValidator())
        self.generate_graph_btn = QPushButton("Generate")
        layout = QVBoxLayout()
        layout.addWidget(self.vertex_count_input)
        layout.addWidget(self.generate_graph_btn)
        self.setLayout(layout)

        self.generate_graph_btn.clicked.connect(self.generate_graph_btn_clicked)

    def generate_graph_btn_clicked(self):
        if int(self.vertex_count_input.text()) > 1:
                start = time.time()
                graph = randomize_graph(int(self.vertex_count_input.text()), int(self.vertex_count_input.text()) - 1)
                end = time.time()
                self.parent.set_graph(graph)
                self.parent.output_to_info(f"Graph was generated in {end - start}s")            


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