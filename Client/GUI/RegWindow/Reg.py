# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Reg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Registration(QtWidgets.QDialog):
    def setupUi(self, Registration):
        Registration.setObjectName("Registration")
        Registration.setWindowModality(QtCore.Qt.WindowModal)
        Registration.resize(278, 138)
        Registration.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Registration)
        self.buttonBox.setGeometry(QtCore.QRect(10, 100, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Registration)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 261, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.LoginLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.LoginLabel.setObjectName("LoginLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.LoginLabel)
        self.LoginInputBox = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.LoginInputBox.setObjectName("LoginInputBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.LoginInputBox)
        self.PassLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.PassLabel.setObjectName("PassLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.PassLabel)
        self.PassInputBox = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.PassInputBox.setObjectName("PassInputBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.PassInputBox)
        self.UsernameInputBox = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.UsernameInputBox.setObjectName("UsernameInputBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.UsernameInputBox)
        self.NameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.NameLabel.setObjectName("NameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.NameLabel)

        self.retranslateUi(Registration)
        self.buttonBox.accepted.connect(Registration.accept)
        self.buttonBox.rejected.connect(Registration.reject)
        QtCore.QMetaObject.connectSlotsByName(Registration)

    def retranslateUi(self, Registration):
        _translate = QtCore.QCoreApplication.translate
        Registration.setWindowTitle(_translate("Registration", "Registration Form"))
        self.LoginLabel.setText(_translate("Registration", "Login"))
        self.PassLabel.setText(_translate("Registration", "Password"))
        self.NameLabel.setText(_translate("Registration", "Username"))

