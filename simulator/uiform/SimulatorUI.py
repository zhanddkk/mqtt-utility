# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SimulatorUI.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SimulatorUI(object):
    def setupUi(self, SimulatorUI):
        SimulatorUI.setObjectName("SimulatorUI")
        SimulatorUI.resize(1024, 768)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/simulator.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SimulatorUI.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(SimulatorUI)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(2, 0, 2, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.treeWidgetDataInfo = QtWidgets.QTreeWidget(self.groupBox)
        self.treeWidgetDataInfo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidgetDataInfo.setAlternatingRowColors(True)
        self.treeWidgetDataInfo.setColumnCount(2)
        self.treeWidgetDataInfo.setObjectName("treeWidgetDataInfo")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetDataInfo)
        self.gridLayout_10.addWidget(self.treeWidgetDataInfo, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.textEditValue = QtWidgets.QTextEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.textEditValue.setFont(font)
        self.textEditValue.setObjectName("textEditValue")
        self.gridLayout_9.addWidget(self.textEditValue, 0, 2, 1, 1)
        self.pushButtonPublish = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButtonPublish.setObjectName("pushButtonPublish")
        self.gridLayout_9.addWidget(self.pushButtonPublish, 3, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        SimulatorUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SimulatorUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        SimulatorUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SimulatorUI)
        self.statusbar.setObjectName("statusbar")
        SimulatorUI.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(SimulatorUI)
        self.dockWidget.setEnabled(True)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.treeViewDataDictionary = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeViewDataDictionary.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeViewDataDictionary.setAlternatingRowColors(True)
        self.treeViewDataDictionary.setObjectName("treeViewDataDictionary")
        self.gridLayout_5.addWidget(self.treeViewDataDictionary, 1, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        SimulatorUI.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.dockWidget_3 = QtWidgets.QDockWidget(SimulatorUI)
        self.dockWidget_3.setObjectName("dockWidget_3")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.listViewLog = QtWidgets.QListView(self.dockWidgetContents_3)
        self.listViewLog.setObjectName("listViewLog")
        self.gridLayout_3.addWidget(self.listViewLog, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        SimulatorUI.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_3)
        self.toolBar = QtWidgets.QToolBar(SimulatorUI)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        SimulatorUI.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionConnectMqtt = QtWidgets.QAction(SimulatorUI)
        self.actionConnectMqtt.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ico/connect.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnectMqtt.setIcon(icon1)
        self.actionConnectMqtt.setObjectName("actionConnectMqtt")
        self.actionSetting = QtWidgets.QAction(SimulatorUI)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ico/set.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetting.setIcon(icon2)
        self.actionSetting.setObjectName("actionSetting")
        self.action_Load_CSV = QtWidgets.QAction(SimulatorUI)
        self.action_Load_CSV.setObjectName("action_Load_CSV")
        self.action_Exit = QtWidgets.QAction(SimulatorUI)
        self.action_Exit.setObjectName("action_Exit")
        self.menu_File.addAction(self.action_Load_CSV)
        self.menu_File.addAction(self.action_Exit)
        self.menubar.addAction(self.menu_File.menuAction())
        self.toolBar.addAction(self.actionConnectMqtt)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSetting)

        self.retranslateUi(SimulatorUI)
        QtCore.QMetaObject.connectSlotsByName(SimulatorUI)

    def retranslateUi(self, SimulatorUI):
        _translate = QtCore.QCoreApplication.translate
        SimulatorUI.setWindowTitle(_translate("SimulatorUI", "Simulator"))
        self.groupBox.setTitle(_translate("SimulatorUI", "Data Information"))
        self.treeWidgetDataInfo.headerItem().setText(0, _translate("SimulatorUI", "Name"))
        self.treeWidgetDataInfo.headerItem().setText(1, _translate("SimulatorUI", "Value"))
        __sortingEnabled = self.treeWidgetDataInfo.isSortingEnabled()
        self.treeWidgetDataInfo.setSortingEnabled(False)
        self.treeWidgetDataInfo.topLevelItem(0).setText(0, _translate("SimulatorUI", "SubSystem"))
        self.treeWidgetDataInfo.topLevelItem(1).setText(0, _translate("SimulatorUI", "DataPath"))
        self.treeWidgetDataInfo.topLevelItem(2).setText(0, _translate("SimulatorUI", "Name"))
        self.treeWidgetDataInfo.topLevelItem(3).setText(0, _translate("SimulatorUI", "Description"))
        self.treeWidgetDataInfo.topLevelItem(4).setText(0, _translate("SimulatorUI", "Type"))
        self.treeWidgetDataInfo.topLevelItem(5).setText(0, _translate("SimulatorUI", "Format"))
        self.treeWidgetDataInfo.topLevelItem(6).setText(0, _translate("SimulatorUI", "MaxSize"))
        self.treeWidgetDataInfo.topLevelItem(7).setText(0, _translate("SimulatorUI", "Default"))
        self.treeWidgetDataInfo.topLevelItem(8).setText(0, _translate("SimulatorUI", "Min"))
        self.treeWidgetDataInfo.topLevelItem(9).setText(0, _translate("SimulatorUI", "Max"))
        self.treeWidgetDataInfo.topLevelItem(10).setText(0, _translate("SimulatorUI", "ChoiceList"))
        self.treeWidgetDataInfo.topLevelItem(11).setText(0, _translate("SimulatorUI", "ScaleUnit"))
        self.treeWidgetDataInfo.topLevelItem(12).setText(0, _translate("SimulatorUI", "Precision"))
        self.treeWidgetDataInfo.topLevelItem(13).setText(0, _translate("SimulatorUI", "IsAlarm"))
        self.treeWidgetDataInfo.topLevelItem(14).setText(0, _translate("SimulatorUI", "IsEvtLog"))
        self.treeWidgetDataInfo.topLevelItem(15).setText(0, _translate("SimulatorUI", "Producer"))
        self.treeWidgetDataInfo.topLevelItem(16).setText(0, _translate("SimulatorUI", "Consumer"))
        self.treeWidgetDataInfo.topLevelItem(17).setText(0, _translate("SimulatorUI", "HashID"))
        self.treeWidgetDataInfo.setSortingEnabled(__sortingEnabled)
        self.groupBox_2.setTitle(_translate("SimulatorUI", "Publish Data"))
        self.pushButtonPublish.setText(_translate("SimulatorUI", "Publish"))
        self.menu_File.setTitle(_translate("SimulatorUI", "&File"))
        self.dockWidget.setWindowTitle(_translate("SimulatorUI", "Data Dictionary"))
        self.dockWidget_3.setWindowTitle(_translate("SimulatorUI", "Log"))
        self.toolBar.setWindowTitle(_translate("SimulatorUI", "toolBar"))
        self.actionConnectMqtt.setText(_translate("SimulatorUI", "ConnectMqtt"))
        self.actionSetting.setText(_translate("SimulatorUI", "Setting"))
        self.action_Load_CSV.setText(_translate("SimulatorUI", "&Load CSV"))
        self.action_Exit.setText(_translate("SimulatorUI", "&Exit"))

import simulator.uiresource.Simulator_rc
