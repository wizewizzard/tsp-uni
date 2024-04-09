from PyQt5.QtWidgets import QWidget,QTextEdit,QVBoxLayout,QPushButton

class AlgorithmMenu(QWidget):
    def __init__(self,parent=None):
            super().__init__(parent)

            self.textEdit = QTextEdit()
            self.btnPress1 = QPushButton("Clear")
            self.textEdit.setReadOnly(True)
            layout = QVBoxLayout()
            layout.addWidget(self.textEdit)
            layout.addWidget(self.btnPress1)
            self.setLayout(layout)

            self.btnPress1.clicked.connect(self.btnPress1_Clicked)

    def btnPress1_Clicked(self):
            self.clear()