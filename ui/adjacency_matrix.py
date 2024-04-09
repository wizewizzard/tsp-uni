from PyQt5 import Qt

class AdjacencyMatrixQWidget(Qt.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_matrix(self, matrix):
        self.setColumnCount(len(matrix))  
        self.setRowCount(len(matrix))   
        self.setHorizontalHeaderLabels([str(i) for i in range(len(matrix))])
        self.setVerticalHeaderLabels([str(i) for i in range(len(matrix))])
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                self.setItem(i, j, Qt.QTableWidgetItem(str(matrix[i][j])))
        self.resizeColumnsToContents()