# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiMessageBrowserWindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MessageBrowserWindow(object):
    def setupUi(self, MessageBrowserWindow):
        MessageBrowserWindow.setObjectName("MessageBrowserWindow")
        MessageBrowserWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MessageBrowserWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.filter_config_file_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.filter_config_file_line_edit.setReadOnly(True)
        self.filter_config_file_line_edit.setObjectName("filter_config_file_line_edit")
        self.gridLayout.addWidget(self.filter_config_file_line_edit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.message_browser_plain_text_edit = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.message_browser_plain_text_edit.setFont(font)
        self.message_browser_plain_text_edit.setReadOnly(True)
        self.message_browser_plain_text_edit.setObjectName("message_browser_plain_text_edit")
        self.gridLayout.addWidget(self.message_browser_plain_text_edit, 1, 0, 1, 2)
        MessageBrowserWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MessageBrowserWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        MessageBrowserWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpenFilterConfigFile = QtWidgets.QAction(MessageBrowserWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/ico/LogFilter.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenFilterConfigFile.setIcon(icon)
        self.actionOpenFilterConfigFile.setObjectName("actionOpenFilterConfigFile")
        self.actionSaveFilterConfigFile = QtWidgets.QAction(MessageBrowserWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ico/ico/Save.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveFilterConfigFile.setIcon(icon1)
        self.actionSaveFilterConfigFile.setObjectName("actionSaveFilterConfigFile")
        self.actionSaveAsFilterConfigFile = QtWidgets.QAction(MessageBrowserWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ico/ico/SaveAs.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveAsFilterConfigFile.setIcon(icon2)
        self.actionSaveAsFilterConfigFile.setObjectName("actionSaveAsFilterConfigFile")
        self.actionStartToWatch = QtWidgets.QAction(MessageBrowserWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/ico/ico/Start.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStartToWatch.setIcon(icon3)
        self.actionStartToWatch.setObjectName("actionStartToWatch")
        self.actionStopToWatch = QtWidgets.QAction(MessageBrowserWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/ico/ico/Stop.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStopToWatch.setIcon(icon4)
        self.actionStopToWatch.setObjectName("actionStopToWatch")
        self.actionClearAllMessages = QtWidgets.QAction(MessageBrowserWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/ico/ico/LogClear.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClearAllMessages.setIcon(icon5)
        self.actionClearAllMessages.setObjectName("actionClearAllMessages")
        self.toolBar.addAction(self.actionOpenFilterConfigFile)
        self.toolBar.addAction(self.actionSaveFilterConfigFile)
        self.toolBar.addAction(self.actionSaveAsFilterConfigFile)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStartToWatch)
        self.toolBar.addAction(self.actionStopToWatch)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClearAllMessages)

        self.retranslateUi(MessageBrowserWindow)
        QtCore.QMetaObject.connectSlotsByName(MessageBrowserWindow)

    def retranslateUi(self, MessageBrowserWindow):
        _translate = QtCore.QCoreApplication.translate
        MessageBrowserWindow.setWindowTitle(_translate("MessageBrowserWindow", "MainWindow"))
        self.label.setText(_translate("MessageBrowserWindow", "Config:"))
        self.toolBar.setWindowTitle(_translate("MessageBrowserWindow", "toolBar"))
        self.actionOpenFilterConfigFile.setText(_translate("MessageBrowserWindow", "Open Filter Config File"))
        self.actionSaveFilterConfigFile.setText(_translate("MessageBrowserWindow", "Save Filter Config File"))
        self.actionSaveAsFilterConfigFile.setText(_translate("MessageBrowserWindow", "Save As Filter Config File"))
        self.actionStartToWatch.setText(_translate("MessageBrowserWindow", "Start To Watch"))
        self.actionStopToWatch.setText(_translate("MessageBrowserWindow", "Stop To Watch"))
        self.actionClearAllMessages.setText(_translate("MessageBrowserWindow", "Clear All"))

import UiResource_rc
