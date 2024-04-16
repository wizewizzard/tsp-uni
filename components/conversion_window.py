from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QTableWidget
from PyQt5 import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.interpolate import make_interp_spline, interp1d
import numpy as np

class ConversionWindow(QDialog):
    def __init__(self, conversion):
        super().__init__()

        data = np.array(conversion)

        x, y = data.T
        _x = y
        _y = x
        no_duplicates_x = []
        no_duplicates_y = []
        for i in range(len(_x) - 1):
            if _x[i] != _x[i + 1]:
                no_duplicates_x.append(_x[i])
                no_duplicates_y.append(_y[i])

        x = np.array(no_duplicates_x)
        y = np.array(no_duplicates_y)

        X_Y_Spline = interp1d(x, y, kind = "cubic")
        X_ = np.linspace(x.min(), x.max(), 500)
        Y_ = X_Y_Spline(X_)

        self.setGeometry(0, 0, 800, 600)
        self.ok_btn = QPushButton("Ok", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.ok_btn.clicked.connect(self.accept)
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.axes.plot(X_, Y_)
        self.axes.scatter(x, y)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.ok_btn)
        self.setLayout(layout)

    def return_from_window(self):
        self.exec_()
