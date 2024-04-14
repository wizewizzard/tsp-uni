from PyQt5.QtWidgets import QDialog,QLineEdit,QVBoxLayout,QPushButton,QTableWidget
from PyQt5 import Qt


class BuildGraphByAjacencyMatrixPopUp(QDialog):
    def __init__(self):
        super(BuildGraphByAjacencyMatrixPopUp, self).__init__()
        self.vertex_count_input = QLineEdit(self)
        self.vertex_count_input.setFixedWidth(40)
        layout = QVBoxLayout()

        self.matrix_input = AdjacencyMatrixQWidget()

        self.ok_btn = QPushButton("Ok", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.matrix_input)
        layout.addWidget(self.ok_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            return []
        else:
            return None
        
class AdjacencyMatrixQWidget(QTableWidget):
    def __init__(self, vertex_count=50, parent=None):
        super().__init__(parent)
        self.setColumnCount(vertex_count)  
        self.setRowCount(vertex_count)   
        self.resizeColumnsToContents()
        for i in range(vertex_count):
            item = Qt.QTableWidgetItem('0')
            item.setDisabled(True)
            self.setItem(i, i, item)
        