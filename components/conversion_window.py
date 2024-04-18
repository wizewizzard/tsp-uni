from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QPushButton, QTableWidget
from PyQt5 import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.interpolate import make_interp_spline, interp1d
import numpy as np

class ConversionPointEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ConversionWindow(QWidget):
    def __init__(self, communication, cfg):
        super().__init__()
        self.data = []
        self.communication = communication
        self.communication.point.connect(self.append_point)

        self.setGeometry(0, 0, 1024, 800)
        self.stop_calculation_btn = QPushButton(cfg['text']['stop_calculation_text'])
        # self.ok_btn = QPushButton("Ok", self)
        self.fig = Figure()
        layout = QVBoxLayout()
        self.canvas = FigureCanvas(self.fig)
        # self.ok_btn.clicked.connect(self.accept)
        self.axes = self.fig.add_subplot(111)

        layout.addWidget(self.canvas)
        layout.addWidget(self.stop_calculation_btn)
        # layout.addWidget(self.ok_btn)
        self.setLayout(layout)
        self.stop_calculation_btn.clicked.connect(self.closeEvent)

    def closeEvent(self, event):
        self.communication.stop_signal.emit(True)
        self.close()

    def append_point(self, point):
        self.data.append((point.x, point.y))
        if len(self.data) > 4:
            data = np.array(self.data)
            x, y = data.T
            no_duplicates_x = []
            no_duplicates_y = []
            for i in range(len(x) - 1):
                if x[i] != x[i + 1]:
                    no_duplicates_x.append(x[i])
                    no_duplicates_y.append(y[i])

            x = np.array(no_duplicates_x)
            y = np.array(no_duplicates_y)

            X_Y_Spline = interp1d(x, y, kind = "cubic")
            X_ = np.linspace(x.min(), x.max(), 500)
            Y_ = X_Y_Spline(X_)
            self.axes.cla()
            self.axes.plot(X_, Y_)
            self.axes.scatter(x, y)
            self.fig.canvas.draw_idle()
