from PyQt5.QtWidgets import QDialog,QLineEdit,QVBoxLayout,QPushButton


class RandomizeGraphPopUp(QDialog):
    def __init__(self, parent = None):
        super(RandomizeGraphPopUp, self).__init__()
        self.vertex_count_input = QLineEdit(self)
        self.vertex_count_input.setFixedWidth(40)
        layout = QVBoxLayout()
        self.ok_btn = QPushButton("Ok", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.vertex_count_input)
        layout.addWidget(self.ok_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            val1 = int(self.vertex_count_input.text())
            return val1
        else:
            return None