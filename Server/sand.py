from PyQt5.QtWidgets import QWidget, QApplication, QListView, QAbstractItemView
from PyQt5 import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal
import sys



class Item(QStandardItem):
    def __init__(self):
        super().__init__()
        self.Id = 1

    @property
    def id(self):
        return self.Id


class w(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ItemView QListView")
        self.setFixedWidth(210)
        self.setFixedHeight(100)

        fruits = ["Buttons in GroupBox", "TextBox in GroupBox", "Label in GroupBox", "TextEdit"]

        view = QListView(self)
        #view.setEditTriggers(QAbstractItemView.DoubleClicked)
        view.doubleClicked.connect(self.haha)


        self.model = QStandardItemModel()

        for f in fruits:
            item = QStandardItem()
            item.setText(f)
            item.setEditable(False)
            item.Id = 1
            self.model.appendRow(item)
        view.setModel(self.model)
        self.show()

    def haha(self, index):
        item = self.model.itemFromIndex(index)
        lol = QWidget()
        lol.setWindowTitle(str(item.Id))
        lol.show()
        self.lol = lol

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = w()
    sys.exit(app.exec_())