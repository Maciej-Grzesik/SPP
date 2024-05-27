import sys
from PyQt5.QtWidgets import *
from window import Window


def main():
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# zabezpieczenie kodu