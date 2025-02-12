# main.py
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from themes import set_dark_theme

def main():
    app = QApplication(sys.argv)
    set_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
