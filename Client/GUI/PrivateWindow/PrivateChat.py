# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PrivateChat.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PrivateChat(QtWidgets.QWidget):
    def setupUi(self, PrivateChat):
        PrivateChat.setObjectName("PrivateChat")
        PrivateChat.resize(709, 538)
        self.verticalLayoutWidget = QtWidgets.QWidget(PrivateChat)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 711, 539))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.MainUserLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(12)
        self.MainUserLabel.setFont(font)
        self.MainUserLabel.setObjectName("MainUserLabel")
        self.horizontalLayout_4.addWidget(self.MainUserLabel)
        self.RecipLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(12)
        self.RecipLabel.setFont(font)
        self.RecipLabel.setObjectName("RecipLabel")
        self.horizontalLayout_4.addWidget(self.RecipLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.Chat = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.Chat.setMinimumSize(QtCore.QSize(0, 450))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(10)
        self.Chat.setFont(font)
        self.Chat.setUndoRedoEnabled(False)
        self.Chat.setReadOnly(True)
        self.Chat.setObjectName("Chat")
        self.verticalLayout.addWidget(self.Chat)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.InputBox = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.InputBox.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(11)
        self.InputBox.setFont(font)
        self.InputBox.setObjectName("InputBox")
        self.horizontalLayout_3.addWidget(self.InputBox)
        self.SendButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.SendButton.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(11)
        self.SendButton.setFont(font)
        self.SendButton.setObjectName("SendButton")
        self.horizontalLayout_3.addWidget(self.SendButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(PrivateChat)
        QtCore.QMetaObject.connectSlotsByName(PrivateChat)

    def retranslateUi(self, PrivateChat):
        _translate = QtCore.QCoreApplication.translate
        PrivateChat.setWindowTitle(_translate("PrivateChat", "Chat"))
        self.MainUserLabel.setText(_translate("PrivateChat", "User"))
        self.RecipLabel.setText(_translate("PrivateChat", "Recipient"))
        self.SendButton.setText(_translate("PrivateChat", "Send"))

