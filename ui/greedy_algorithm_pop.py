from PyQt5.QtWidgets import QDialog,QLineEdit,QVBoxLayout,QPushButton


class GreedyAlgorithmPopUp(QDialog):
    def __init__(self, vertex_count, parent = None,):
        super(GreedyAlgorithmPopUp, self).__init__()
        self.vertex_count = vertex_count
        self.start_vertex = QLineEdit(self)
        self.start_vertex.setFixedWidth(40)
        layout = QVBoxLayout()
        self.ok_btn = QPushButton("Ok", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.start_vertex)
        layout.addWidget(self.ok_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            val1 = int(self.start_vertex.text())
            if val1 >= self.vertex_count:
                raise ValueError()
            return val1
        else:
            return None