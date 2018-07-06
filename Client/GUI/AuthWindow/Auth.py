# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Auth.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Authorisation(QtWidgets.QDialog):
    def setupUi(self, Authorisation):
        Authorisation.setObjectName("Authorisation")
        Authorisation.setWindowModality(QtCore.Qt.WindowModal)
        Authorisation.resize(278, 108)
        Authorisation.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Authorisation)
        self.buttonBox.setGeometry(QtCore.QRect(10, 70, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Authorisation)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 261, 51))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.LoginLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.LoginLabel.setObjectName("LoginLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.LoginLabel)
        self.LoginInputBox = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.LoginInputBox.setObjectName("LoginInputBox")
        #self.LoginInputBox.text().
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LoginInputBox)
        self.PassLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.PassLabel.setObjectName("PassLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.PassLabel)
        self.PassInputBox = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.PassInputBox.setObjectName("PassInputBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.PassInputBox)

        self.retranslateUi(Authorisation)
        self.buttonBox.accepted.connect(Authorisation.accept)
        self.buttonBox.rejected.connect(Authorisation.reject)
        QtCore.QMetaObject.connectSlotsByName(Authorisation)

    def retranslateUi(self, Authorisation):
        _translate = QtCore.QCoreApplication.translate
        Authorisation.setWindowTitle(_translate("Authorisation", "Authorisation Form"))
        self.LoginLabel.setText(_translate("Authorisation", "Login"))
        self.PassLabel.setText(_translate("Authorisation", "Password"))

