from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from button import Button
from plot import PlotGraph


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('Systemy Pomiarowe - Projekt')
        self.setStyleSheet("background-color: #212121")
        self.setFixedSize(1280, 720)

        self.layout = QHBoxLayout(self)
        self.plot_widget = PlotGraph()
        self.layout.addWidget(self.plot_widget, alignment=Qt.AlignHCenter)
        self.init_buttons()

    def init_buttons(self):
        button_layout = QVBoxLayout()


        save_button = Button("Save")
        save_button.clicked.connect(self.save_file)
        # exit_button = Button("Exit")
        # spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        button_layout.addWidget(save_button, alignment=Qt.AlignCenter | Qt.AlignVCenter)
        # button_layout.addItem(spacer_item)
        # button_layout.addWidget(exit_button)

        self.layout.addLayout(button_layout)

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                for i in range(len(self.plot_widget.distance_data)):
                    f.write(f"{round(0.1*i, 2)},{self.plot_widget.distance_data[i]} \n")