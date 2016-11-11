from PyQt5.QtCore import Qt
from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueViewModel


class GeneralValueEditTreeViewModel(ValueViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        header = (self.datagram.property.format,)
        super(GeneralValueEditTreeViewModel, self).__init__(header, parent)
    pass

    def update(self):
        value = self.datagram.get_value(self.dev_index)
        self.root_item.append_child(ValueTreeViewItem([value], self.root_item))

    def get_value(self):
        item = self.root_item.child(0)
        print(type(item.data(0)))
        return item.data(0)
        pass

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
