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

        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.layout.addWidget(self.plot_widget)

        self.distance_data = []
        self.acceleration_data = []
        self.max_data_points = 100
        self.time_window = (0, self.max_data_points)

        self.threshold1 = 100
        self.threshold2 = 200
        self.threshold3 = 300

        self.threshold1_input = QLineEdit(self)
        self.threshold1_input.setText(str(self.threshold1))
        self.threshold1_input.setPlaceholderText("Threshold 1")
        self.threshold1_input.setStyleSheet("color: white;")
        #self.threshold1_input.textChanged.connect(self.update_threshold1)

        self.threshold2_input = QLineEdit(self)
        self.threshold2_input.setText(str(self.threshold2))
        self.threshold2_input.setPlaceholderText("Threshold 2")
        self.threshold2_input.setStyleSheet("color: white;")
        #self.threshold2_input.textChanged.connect(self.update_threshold2)

        self.threshold3_input = QLineEdit(self)
        self.threshold3_input.setText(str(self.threshold3))
        self.threshold3_input.setPlaceholderText("Threshold 3")
        self.threshold3_input.setStyleSheet("color: white;")
        #self.threshold3_input.textChanged.connect(self.update_threshold3)

        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(self.threshold1_input)
        threshold_layout.addWidget(self.threshold2_input)
        threshold_layout.addWidget(self.threshold3_input)

        self.layout.addLayout(threshold_layout)

        self.acceleration_input = QLineEdit(self)
        self.acceleration_input.setReadOnly(True)
        self.acceleration_input.setPlaceholderText("Acceleration: 0 m/s²")
        self.acceleration_input.setStyleSheet("color: white; font-size: 16px; background-color: #333;")
        self.layout.addWidget(self.acceleration_input)

        # self.serial_thread = SerialThread()
        # self.serial_thread.distance_signal.connect(self.update_plot)
        # self.serial_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

        self.acceleration_timer = QTimer(self)
        self.acceleration_timer.timeout.connect(self.calculate_and_update_acceleration)
        self.acceleration_timer.start(1000)

    def update_plot(self, distance=None):
        self.append_distance(distance)

        self.update_time_window()

        self.plot_widget.clear()
        self.plot_widget.setXRange(*self.time_window)
        self.plot_widget.plot(self.distance_data, pen=pg.mkPen("w"))

        if self.distance_data:
            self.update_y_range()

    def append_distance(self, distance):
        if distance is not None:
            self.distance_data.append(distance)

            self.handle_background_change(distance)

    def update_time_window(self) -> None:
        left_time_window_limit = int(len(self.distance_data) / self.max_data_points)
        self.time_window = (left_time_window_limit * 100, left_time_window_limit * 100 + self.max_data_points)

    def update_y_range(self):
        if self.distance_data[-1] != self.distance_data[-2]:
            recent_data = self.distance_data[-self.max_data_points:]
            self.plot_widget.setYRange(min(recent_data), max(recent_data))

    def handle_background_change(self, distance):
        if distance < self.threshold1_input:
            background_color = QColor(235, 52, 52, 50)
            self.plot_widget.setBackground(background_color)
        elif distance < self.threshold2_input:
            background_color = QColor(255, 140, 0, 50)
            self.plot_widget.setBackground(background_color)
        elif distance < self.threshold3_input:
            background_color = QColor(255, 255, 0, 50)
            self.plot_widget.setBackground(background_color)
        else:
            self.plot_widget.setBackground("#212121")

    def calculate_acceleration(self):
        if len(self.distance_data) >= 3:
            d1 = self.distance_data[-3] / 1000.0
            d2 = self.distance_data[-2] / 1000.0
            d3 = self.distance_data[-1] / 1000.0
            t = 0.1

            v1 = (d2 - d1) / t
            v2 = (d3 - d2) / t

            acceleration = (v2 - v1) / t
            self.acceleration_data.append(acceleration)

    def update_acceleration_input(self):
        if self.acceleration_data:
            self.acceleration_input.setText(f"Acceleration: {self.acceleration_data[-1]:.2f} m/s²")

    def calculate_and_update_acceleration(self):
        self.calculate_acceleration()
        self.update_acceleration_input()

    # def update_threshold1(self):
    #     text = self.threshold1_input.text()
    #     try:
    #         new_threshold = int(text)
    #         if new_threshold < self.threshold2 and new_threshold < self.threshold3:
    #             self.threshold1 = new_threshold
    #         else:
    #             self.threshold1_input.setText(str(self.threshold1))
    #     except ValueError:
    #         pass
    #
    # def update_threshold2(self):
    #     text = self.threshold2_input.text()
    #     try:
    #         new_threshold = int(text)
    #         if self.threshold1 < new_threshold < self.threshold3:
    #             self.threshold2 = new_threshold
    #         else:
    #             self.threshold2_input.setText(str(self.threshold2))
    #     except ValueError:
    #         pass
    #
    # def update_threshold3(self):
    #     text = self.threshold3_input.text()
    #     try:
    #         new_threshold = int(text)
    #         if self.threshold1 < self.threshold2 < new_threshold:
    #             self.threshold3 = new_threshold
    #         else:
    #             self.threshold3_input.setText(str(self.threshold3))
    #     except ValueError:
    #         pass

    def clear_data(self):
        self.distance_data.clear()
