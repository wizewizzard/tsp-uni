from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QPushButton
from PyQt5 import QtCore, Qt


class AdjacencyMatrixQWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.vertex_count = 0
        self.table = QTableWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.apply_btn = QPushButton("Применить", self)
        layout.addWidget(self.table)
        layout.addWidget(self.apply_btn)
        self.setLayout(layout)
        self.table.installEventFilter(self)
        self.matrix_copy = None

        self.apply_btn.clicked.connect(self.apply_matrix)

    def set_matrix(self, matrix):
        self.matrix_copy = [row[:] for row in matrix]
        self.vertex_count = len(matrix)
        self.table.setColumnCount(len(matrix))
        self.table.setRowCount(len(matrix))
        self.table.setHorizontalHeaderLabels([str(i) for i in range(len(matrix))])
        self.table.setVerticalHeaderLabels([str(i) for i in range(len(matrix))])
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                cell = QTableWidgetItem(str(matrix[i][j]))
                if j < i:
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                elif i == j:
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(i, j, cell)
                else:
                    self.table.setItem(i, j, cell)
        self.table.resizeColumnsToContents()

    def update_graph(self):
        matrix = [[0] * self.vertex_count for _ in range(self.vertex_count)]
        for i in range(self.vertex_count):
            for j in range(self.vertex_count):
                print(self.table.item(i, j).text())
                matrix = int(self.table.item(i, j).text())
        self.parent.update_graph(matrix)

    #
    def apply_matrix(self):
        try:
            matrix = [[0] * self.vertex_count for _ in range(self.vertex_count)]
            for i in range(self.vertex_count):
                for j in range(i, self.vertex_count):
                    value1 = int(self.table.item(i, j).text())
                    matrix[i][j] = matrix[j][i] = value1
            self.parent.update_graph(matrix)
        except Exception as err:
            self.set_matrix(self.matrix_copy)
            self.parent.output_error(f"Неверно введены данные")

    def validate_matrix(self, matrix):
        for i in range(self.vertex_count):
            for j in range(self.vertex_count):
                value = self.table.item(i, j)
