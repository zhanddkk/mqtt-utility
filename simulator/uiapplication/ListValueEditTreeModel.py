from PyQt5.QtCore import Qt
from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class ListValueEditTreeModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        self.action = 0
        self.value_size = datagram.attribute.max_size
        header = ('Index', self.datagram.attribute.format,)
        super(ListValueEditTreeModel, self).__init__(header, parent)
    pass

    def update(self):
        self.beginResetModel()
        value = self.datagram.data_list[self.dev_index].get_value(self.action)
        if self.value_size is not None and self.value_size > 1:
            for i in range(0, self.value_size):
                try:
                    self.root_item.append_child(ValueTreeViewItem([i, value[i]], self.root_item))
                except IndexError:
                    self.root_item.append_child(ValueTreeViewItem([i, None], self.root_item))
                except TypeError:
                    self.root_item.append_child(ValueTreeViewItem([i, None], self.root_item))
        else:
            self.root_item.append_child(ValueTreeViewItem([0, value], self.root_item))
        self.endResetModel()

    def get_value(self):
        value = []
        row = self.root_item.child_count()
        for i in range(0, row):
            item = self.root_item.child(i)
            value.append(item.data(1))
        if len(value) == 0:
            return None
        elif len(value) == 1:
            return value[0]
        else:
            return value
        pass

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.column() == 1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
