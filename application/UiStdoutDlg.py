# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiStdoutDlg.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StdoutDlg(object):
    def setupUi(self, StdoutDlg):
        StdoutDlg.setObjectName("StdoutDlg")
        StdoutDlg.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(StdoutDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.stdout_text_edit = QtWidgets.QTextEdit(StdoutDlg)
        self.stdout_text_edit.setObjectName("stdout_text_edit")
        self.gridLayout.addWidget(self.stdout_text_edit, 0, 0, 1, 1)

        self.retranslateUi(StdoutDlg)
        QtCore.QMetaObject.connectSlotsByName(StdoutDlg)

    def retranslateUi(self, StdoutDlg):
        _translate = QtCore.QCoreApplication.translate
        StdoutDlg.setWindowTitle(_translate("StdoutDlg", "Stdout"))

