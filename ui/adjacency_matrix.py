from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QWidget,QVBoxLayout,QPushButton
from PyQt5 import QtCore

class AdjacencyMatrixQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.table = QTableWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.apply_btn = QPushButton("Применить", self)
        layout.addWidget(self.table)
        layout.addWidget(self.apply_btn)
        self.setLayout(layout)
        self.table.installEventFilter(self)
    
        self.apply_btn.clicked.connect(self.update_graph)


    def set_matrix(self, matrix):
        self.vertex_count = len(matrix)
        self.table.setColumnCount(len(matrix))  
        self.table.setRowCount(len(matrix))   
        self.table.setHorizontalHeaderLabels([str(i) for i in range(len(matrix))])
        self.table.setVerticalHeaderLabels([str(i) for i in range(len(matrix))])
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                self.table.setItem(i, j, QTableWidgetItem(str(matrix[i][j])))
        self.table.resizeColumnsToContents()

    def update_graph(self):
        matrix = [[0] * self.vertex_count for _ in range(self.vertex_count)]
        for i in range(self.vertex_count):
            for j in range(self.vertex_count):
                print(self.table.item(i, j).text())
                matrix = round(float(self.table.item(i, j).text()), 1)
        self.parent.update_graph(matrix)
 
