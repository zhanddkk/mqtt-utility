from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem


class ValueViewModel(QAbstractItemModel):
    def __init__(self, header, parent=None):
        super(ValueViewModel, self).__init__(parent)
        self.root_item = ValueTreeViewItem(header, None)
        self.update()

    def update(self):
        pass

    def get_value(self):
        pass

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.root_item.column_count()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root_item.data(section)

        return None

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def get_item(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.root_item

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.get_item(index)
        result = item.set_data(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result
