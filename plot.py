from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
import pyqtgraph as pg

from connection import SerialThread


class PlotGraph(QWidget):
    def __init__(self, parent=None):
        super(PlotGraph, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.plot_widget = pg.PlotWidget()
        self.setFixedSize(960, 630)

        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.layout.addWidget(self.plot_widget)

        self.distance_data = []
        self.max_data_points = 100
        self.time_window = (0, self.max_data_points)

        self.serial_thread = SerialThread()
        self.serial_thread.distance_signal.connect(self.update_plot)
        self.serial_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def update_plot(self, distance=None):
        self.append_distance(distance)

        self.update_time_window()

        self.plot_widget.clear()
        self.plot_widget.setXRange(*self.time_window)
        self.plot_widget.plot(self.distance_data, pen=pg.mkPen("w"))

    def append_distance(self, distance):
        if distance is not None:
            self.distance_data.append(distance)

            if distance < 100:
                background_color = QColor(235, 52, 52, 50)
                self.plot_widget.setBackground(background_color)
            elif distance < 200:
                background_color = QColor(255, 140, 0, 50)
                self.plot_widget.setBackground(background_color)
            elif distance < 300:
                background_color = QColor(255, 255, 0, 50)
                self.plot_widget.setBackground(background_color)
            else:
                self.plot_widget.setBackground("#212121")

    def update_time_window(self) -> None:
        left_time_window_limit = int(len(self.distance_data) / self.max_data_points)
        self.time_window = (left_time_window_limit * 100, left_time_window_limit * 100 + self.max_data_points)
