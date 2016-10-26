from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from simulator.uiform.SimulatorUI import Ui_SimulatorUI
from simulator.datadictionary.DatagramManager import DatagramManager
from simulator.datadictionary.Datagram import Datagram


class TreeItem(object):
    def __init__(self, data=[], parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            self.parentItem.childItems.index(self)

        return 0

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value

        return True


class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem()
        # self.dat = DatagramManager()
        self.import_data(data)

    def import_data(self, data):
        pass

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result


'''
class TreeItem(object):
    def __init__(self, data=(), parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            data = [None for v in range(columns)]
            item = TreeItem(data, self)
            self.childItems.insert(position, item)

        return True

    def insertColumns(self, position, columns):
        if position < 0 or position > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.insert(position, None)

        for child in self.childItems:
            child.insertColumns(position, columns)

        return True

    def parent(self):
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

    def removeColumns(self, position, columns):
        if position < 0 or position + columns > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.pop(position)

        for child in self.childItems:
            child.removeColumns(position, columns)

        return True

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value
        print(self.itemData)

        return True


class TreeModel(QAbstractItemModel):
    def __init__(self, headers, data=None, parent=None):
        super(TreeModel, self).__init__(parent)
        headers = ("Topic Node", "Value", "Hash ID")
        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)
        # self.dat = DatagramManager()
        self.import_data(data)

    def import_data(self, data):
        pass

    def columnCount(self, parent=QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0

        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def insertColumns(self, position, columns, parent=QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)
        print(result)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result
'''


class DataManagerModel(QAbstractItemModel):
    def __init__(self, data=DatagramManager(), parent=None):
        super(DataManagerModel, self).__init__(parent)
        self.header = ["Topic Node", "Value", "Hash ID"]
        self.data = data
        pass

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.header)
        pass

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.data.hash_id_list)
        pass

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        column = index.column()
        row = index.row()
        try:
            hash_id = self.data.hash_id_list[row]
        except IndexError:
            return None
        dg = self.data.get_datagram(hash_id)
        if column == 0:
            return dg.get_topic(0)
        elif column == 1:
            return str(dg.data_property.default)
        elif column == 2:
            return hash_id
        else:
            return None

    def headerData(self, p_int, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.header[p_int]
            except IndexError:
                return None

        return None
        pass

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            child_item = None
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()
            # parent_item = parent.internalPointer()
            # child_item = "234"
            # return self.createIndex(row, column, child_item)

    def parent(self, index):
        return QModelIndex()


class MainApp(QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.ui = Ui_SimulatorUI()
        self.ui.setupUi(self)

        self.datagram = DatagramManager()
        self.load_csv('../datadictionarysource/default_data_dictionary.csv')

        # self.data_dictionary = TreeModel(None)
        # self.import_datagram(self.data_dictionary, self.datagram)

        # self.data_dictionary.rootItem = TreeItem(("Topic Node", "Value", "Hash ID2"))
        self.datagram_manager_model = DataManagerModel(self.datagram)
        self.ui.treeViewDataDictionary.setModel(self.datagram_manager_model)

        # self.ui.treeViewDataDictionary.setModel(self.data_dictionary)
        # self.ui.treeViewDataDictionary.selectionModel().selectionChanged.connect(
        #    self.on_treeViewDataDictionary_selectionModel_selectionChanged)
        # self.ui.treeViewDataDictionary.selectionModel().selectionChanged.connect(self.updateActions)

    def load_csv(self, filename=""):
        self.datagram.import_datagram(filename)
        pass

    @staticmethod
    def import_datagram(tree_model=TreeModel(None), dg_m=DatagramManager(), header=()):
        tree_model.rootItem = TreeItem(("Topic Node", "Value", "Hash ID"))
        parent = [tree_model.rootItem]

        for this_id in dg_m.hash_id_list:
            dg = dg_m.get_datagram(this_id)
            for i in range(dg.device_num):
                '''
                node_list = dg.get_topic(i).split('\\')
                for j in range(len(node_list)):
                    is_find = False
                    node_list[j] = node_list[j].strip('\\')
                    for sub_item in parent[-1].childItems:
                        if sub_item.itemData[0] == node_list[j]:
                            parent[-1] = sub_item
                    if not is_find:
                        item = TreeItem((node_list[j], dg.get_value(i)), parent[-1])
                        parent[-1].appendChild(item)
                '''
                # item = TreeItem((dg.get_topic(i), dg.get_value(i), dg.id), parent[-1])
                item = TreeItem([dg.get_topic(i), dg.get_value(i), dg.id], parent[-1])
                parent[-1].appendChild(item)
        pass

    @pyqtSlot()
    def on_pushButtonPublish_clicked(self):
        sender = self.sender()
        index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        model = self.ui.treeViewDataDictionary.model()
        a = model.parent(index)
        child = model.index(index.row(), 1, a)
        model.setData(child, self.ui.textEditValue.toPlainText(), Qt.EditRole)
        self.ui.treeViewDataDictionary.closePersistentEditor(index)
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def on_treeViewDataDictionary_selectionModel_selectionChanged(self):
        current_index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        row = current_index.row()
        topic = current_index.sibling(row, 0).data()
        hash_id = current_index.sibling(row, 2).data()
        dg = self.datagram.get_datagram(hash_id)
        self.ui.treeWidgetDataInfo.topLevelItem(0).setText(1, dg.data_property.sub_system)
        self.ui.treeWidgetDataInfo.topLevelItem(1).setText(1, dg.data_property.data_path)
        self.ui.treeWidgetDataInfo.topLevelItem(2).setText(1, dg.data_property.name)
        self.ui.treeWidgetDataInfo.topLevelItem(3).setText(1, dg.data_property.description)
        self.ui.treeWidgetDataInfo.topLevelItem(4).setText(1, dg.data_property.type)
        self.ui.treeWidgetDataInfo.topLevelItem(5).setText(1, dg.data_property.format)
        self.ui.treeWidgetDataInfo.topLevelItem(6).setText(1, str(dg.data_property.max_size))
        self.ui.treeWidgetDataInfo.topLevelItem(7).setText(1, dg.data_property.default)
        self.ui.treeWidgetDataInfo.topLevelItem(8).setText(1, str(dg.data_property.min))
        self.ui.treeWidgetDataInfo.topLevelItem(9).setText(1, str(dg.data_property.max))
        str_list = []
        str_tmp = ""
        choice_list = dg.data_property.choice_list
        if choice_list != {}:
            for (k, d) in choice_list.items():
                str_list.append(k + "\t: " + str(d))
            str_list.sort()
            for s in str_list:
                str_tmp = str_tmp + s + '\n'
            str_tmp = str_tmp.rstrip('\n')
        self.ui.treeWidgetDataInfo.topLevelItem(10).setText(1, str_tmp)
        self.ui.treeWidgetDataInfo.topLevelItem(11).setText(1, dg.data_property.scale_unit)
        self.ui.treeWidgetDataInfo.topLevelItem(12).setText(1, str(dg.data_property.precision))
        self.ui.treeWidgetDataInfo.topLevelItem(13).setText(1, str(dg.data_property.is_alarm))
        self.ui.treeWidgetDataInfo.topLevelItem(14).setText(1, str(dg.data_property.is_evt_log))

        self.ui.treeWidgetDataInfo.topLevelItem(15).setText(1, str(dg.data_property.producer))
        self.ui.treeWidgetDataInfo.topLevelItem(16).setText(1, str(dg.data_property.consumer))

        self.ui.treeWidgetDataInfo.topLevelItem(17).setText(1, hex(dg.data_property.hash_id))
        self.statusBar().showMessage("Clicked: " + topic + " @ " + hex(hash_id))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
