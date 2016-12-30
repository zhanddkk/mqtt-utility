# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiWaitingDlg.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WaitingDialog(object):
    def setupUi(self, WaitingDialog):
        WaitingDialog.setObjectName("WaitingDialog")
        WaitingDialog.resize(170, 33)
        self.gridLayout = QtWidgets.QGridLayout(WaitingDialog)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.time_lcd_number = QtWidgets.QLCDNumber(WaitingDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_lcd_number.sizePolicy().hasHeightForWidth())
        self.time_lcd_number.setSizePolicy(sizePolicy)
        self.time_lcd_number.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.time_lcd_number.setStyleSheet("color: rgb(170, 170, 127);")
        self.time_lcd_number.setFrameShape(QtWidgets.QFrame.Panel)
        self.time_lcd_number.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.time_lcd_number.setSmallDecimalPoint(False)
        self.time_lcd_number.setDigitCount(10)
        self.time_lcd_number.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.time_lcd_number.setObjectName("time_lcd_number")
        self.gridLayout.addWidget(self.time_lcd_number, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(WaitingDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(WaitingDialog)
        QtCore.QMetaObject.connectSlotsByName(WaitingDialog)

    def retranslateUi(self, WaitingDialog):
        _translate = QtCore.QCoreApplication.translate
        WaitingDialog.setWindowTitle(_translate("WaitingDialog", "Waiting..."))
        self.label.setText(_translate("WaitingDialog", "Waiting..."))

