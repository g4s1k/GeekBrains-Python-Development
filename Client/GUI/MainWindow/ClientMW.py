# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClientMW.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(761, 551)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(2, 0, 756, 510))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.Chat = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.Chat.setEnabled(True)
        self.Chat.setMinimumSize(QtCore.QSize(450, 450))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(11)
        self.Chat.setFont(font)
        self.Chat.setReadOnly(True)
        self.Chat.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.Chat.setObjectName("Chat")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Chat)
        self.UsersList = QtWidgets.QListView(self.formLayoutWidget)
        self.UsersList.setMinimumSize(QtCore.QSize(300, 450))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(12)
        self.UsersList.setFont(font)
        self.UsersList.setAutoScroll(False)
        self.UsersList.setTabKeyNavigation(True)
        self.UsersList.setObjectName("UsersList")
        #self.UsersList.
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.UsersList)
        self.InputBox = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.InputBox.setMinimumSize(QtCore.QSize(450, 0))
        self.InputBox.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(11)
        self.InputBox.setFont(font)
        self.InputBox.setObjectName("InputBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.InputBox)
        self.SendButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.SendButton.setMinimumSize(QtCore.QSize(303, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(12)
        self.SendButton.setFont(font)
        self.SendButton.setObjectName("SendButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.SendButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 761, 21))
        self.menubar.setObjectName("menubar")
        self.menuConnection = QtWidgets.QMenu(self.menubar)
        self.menuConnection.setObjectName("menuConnection")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionConnect = QtWidgets.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.actionAuthorisation = QtWidgets.QAction(MainWindow)
        self.actionAuthorisation.setObjectName("actionAuthorisation")
        self.actionRegistration = QtWidgets.QAction(MainWindow)
        self.actionRegistration.setObjectName("actionRegistration")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.menuConnection.addAction(self.actionConnect)
        self.menuConnection.addAction(self.actionAuthorisation)
        self.menuConnection.addAction(self.actionRegistration)
        self.menuConnection.addAction(self.actionDisconnect)
        self.menubar.addAction(self.menuConnection.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SendButton.setText(_translate("MainWindow", "Send"))
        self.menuConnection.setTitle(_translate("MainWindow", "Connection"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionAuthorisation.setText(_translate("MainWindow", "Log In"))
        self.actionRegistration.setText(_translate("MainWindow", "New user"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))
