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

class MainApp(QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.ui = Ui_SimulatorUI()
        self.ui.setupUi(self)

        self.datagram = DatagramManager()
        self.load_csv('../datadictionarysource/default_data_dictionary.csv')

        self.data_dictionary = TreeModel(None)
        self.import_datagram(self.data_dictionary, self.datagram)

        self.ui.treeViewDataDictionary.setModel(self.data_dictionary)
        self.ui.treeViewDataDictionary.selectionModel().selectionChanged.connect(
            self.on_treeViewDataDictionary_selectionModel_selectionChanged)

    def load_csv(self, filename=""):
        self.datagram.import_datagram(filename)
        pass

    @staticmethod
    def import_datagram(tree_model=TreeModel(None), dg_m=DatagramManager(), header=()):
        tree_model.rootItem = TreeItem(("Topic Node", "Value", "Hash ID"))
        parent = [tree_model.rootItem]

        for this_index in dg_m.index_list:
            dg = dg_m.get_datagram(this_index[0])
            item = TreeItem([dg.get_topic(this_index[1]), dg.data_property.default, this_index[0]], parent[-1])
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
