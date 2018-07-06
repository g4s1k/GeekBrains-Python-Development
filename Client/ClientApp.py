import sys
from PyQt5.QtWidgets import QApplication
from Net.myclient import MyClient
from GUI.MainWindow.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = MyClient()
    mw = MainWindow(client)
    sys.exit(app.exec_())