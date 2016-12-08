from PyQt5.QtCore import Qt
from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class StructValueEditModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        self.action = 0
        header = ('Name', 'Type', 'Value')
        super(StructValueEditModel, self).__init__(header, parent)
    pass

    def update(self):
        value = self.datagram.data_list[self.dev_index].get_value(self.action)
        i = 0
        for (k, d) in self.datagram.attribute.choice_list.items():
            if value is not None:
                self.root_item.append_child(ValueTreeViewItem([k, d[0], value[i]], self.root_item))
            else:
                self.root_item.append_child(ValueTreeViewItem([k, d[0], None], self.root_item))
            i += 1

    def get_value(self):
        value = []
        row = self.root_item.child_count()
        for i in range(0, row):
            item = self.root_item.child(i)
            # print(type(item.data(2)))
            value.append(item.data(2))
        return value
        pass

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        flag = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 2:
            flag = flag | Qt.ItemIsEditable
        return flag
