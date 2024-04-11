from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QWidget,QVBoxLayout

class AdjacencyMatrixQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.table = QTableWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        self.table.itemChanged.connect(self.calc)

    def set_matrix(self, matrix):
        self.table.setColumnCount(len(matrix))  
        self.table.setRowCount(len(matrix))   
        self.table.setHorizontalHeaderLabels([str(i) for i in range(len(matrix))])
        self.table.setVerticalHeaderLabels([str(i) for i in range(len(matrix))])
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                self.table.setItem(i, j, QTableWidgetItem(str(matrix[i][j])))
        self.table.resizeColumnsToContents()

    def calc(self, item):
        pass
        # self.parent.
        # self.matrix[item.row()][item.column()] = 1.
        # print(f"{item.row()} - {item.column()}")
