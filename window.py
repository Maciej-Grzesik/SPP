import serial
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from button import Button
from connection import SerialThread
from plot import PlotGraph
from serial.tools import list_ports


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('Systemy Pomiarowe - Projekt')
        self.setStyleSheet("background-color: #212121")
        self.setFixedSize(1280, 720)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.plot_widget = PlotGraph()
        self.layout.addWidget(self.plot_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.init_buttons()

        self.serial_thread = None

    def init_buttons(self):
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 0, 10, 10)
        button_layout.setSpacing(50)


        self.port_combo = QComboBox(self)
        self.port_combo.setFixedWidth(150)
        self.port_combo.setStyleSheet("background-color:white")
        self.port_combo.setContentsMargins(10, 0, 0, 0)
        self.populate_ports()

        connect_button = Button("Connect/Start")
        connect_button.clicked.connect(self.start_serial_thread)

        pause_button = Button("Pause")
        pause_button.clicked.connect(self.pause_plot)

        clear_button = Button("Clear data")
        clear_button.clicked.connect(self.plot_widget.clear_data)

        save_button = Button("Save")
        save_button.clicked.connect(self.save_file)
        save_button.setContentsMargins(0, 0, 10, 0)

        button_layout.addWidget(self.port_combo, alignment=Qt.AlignLeft)
        button_layout.addWidget(connect_button)
        button_layout.addWidget(pause_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(save_button, alignment=Qt.AlignRight)


        self.layout.addLayout(button_layout)

    def populate_ports(self):
        ports = list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)

    def start_serial_thread(self):
        port = self.port_combo.currentText()
        if port:
            self.serial_thread = SerialThread(port)
            self.serial_thread.distance_signal.connect(self.plot_widget.update_plot)
            self.serial_thread.start()

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                for i in range(len(self.plot_widget.distance_data)):
                    f.write(f"{round(0.1*i, 2)},{self.plot_widget.distance_data[i]} \n")


    def pause_plot(self):
        self.serial_thread.running = False
