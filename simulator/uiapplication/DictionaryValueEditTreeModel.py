from PyQt5.QtCore import Qt
from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class DictionaryValueEditTreeModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        self.action = 0
        header = ('Name', self.datagram.attribute.format)
        super(DictionaryValueEditTreeModel, self).__init__(header, parent)
    pass

    def update(self):
        value = self.datagram.data_list[self.dev_index].get_value(self.action)
        name = 'USER DEFINE'
        for (k, d) in self.datagram.attribute.choice_list.items():
            if d[0] == value:
                name = str(d[0]) + ' | ' + k
                break
        self.root_item.append_child(ValueTreeViewItem([name, value], self.root_item))

    def get_value(self):
        item = self.root_item.child(0)
        return item.data(1)
        pass

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        flag = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if (index.column() == 0) or (self.get_item(index).data(0) == 'USER DEFINE'):
            flag = flag | Qt.ItemIsEditable
        return flag

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.get_item(index)
        column = index.column()
        result = item.set_data(column, value)
        if column == 0:
            if value == 'USER DEFINE':
                result_value = False
            else:
                try:
                    value = value.split('|')[1].strip(' ')
                    result_value = item.set_data(1, self.datagram.attribute.choice_list[value][0])
                except KeyError:
                    result_value = item.set_data(1, None)
            index_value = self.index(index.row(), 1, self.parent(index))
            if result_value:
                self.dataChanged.emit(index_value, index_value)

        if result:
            self.dataChanged.emit(index, index)

        return result
