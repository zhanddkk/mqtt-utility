# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiLogWin.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogWindow(object):
    def setupUi(self, LogWindow):
        LogWindow.setObjectName("LogWindow")
        LogWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(LogWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.log_plain_text_edit = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.log_plain_text_edit.setFont(font)
        self.log_plain_text_edit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.log_plain_text_edit.setReadOnly(True)
        self.log_plain_text_edit.setObjectName("log_plain_text_edit")
        self.gridLayout.addWidget(self.log_plain_text_edit, 0, 0, 1, 1)
        LogWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(LogWindow)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(20, 20))
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        LogWindow.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar)
        LogWindow.insertToolBarBreak(self.toolBar)
        self.actionClear = QtWidgets.QAction(LogWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/ico/LogClear.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClear.setIcon(icon)
        self.actionClear.setObjectName("actionClear")
        self.actionFilter = QtWidgets.QAction(LogWindow)
        self.actionFilter.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ico/ico/LogFilter.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFilter.setIcon(icon1)
        self.actionFilter.setObjectName("actionFilter")
        self.toolBar.addAction(self.actionFilter)
        self.toolBar.addAction(self.actionClear)

        self.retranslateUi(LogWindow)
        QtCore.QMetaObject.connectSlotsByName(LogWindow)

    def retranslateUi(self, LogWindow):
        _translate = QtCore.QCoreApplication.translate
        LogWindow.setWindowTitle(_translate("LogWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("LogWindow", "toolBar"))
        self.actionClear.setText(_translate("LogWindow", "Clear"))
        self.actionFilter.setText(_translate("LogWindow", "Filter"))

import UiResource_rc
