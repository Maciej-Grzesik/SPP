import pyqtgraph
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Temperature vs time plot
        self.plot_graph = pyqtgraph.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        x = [1, 2, 3, 4, 5, 4, 3, 2, 1]
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.plot_graph.plot(y, x)

app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()
