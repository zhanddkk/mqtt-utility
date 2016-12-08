from PyQt5.QtCore import Qt
from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel
from simulator.core import PayloadPackage


class GeneralValueEditTreeViewModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, action=0, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        self.action = action
        if action == PayloadPackage.E_DATAGRAM_ACTION_ALLOW:
            header = ('AllowedData',)
            pass
        else:
            header = (self.datagram.attribute.format,)
        super(GeneralValueEditTreeViewModel, self).__init__(header, parent)
    pass

    def update(self):
        self.beginResetModel()
        value = self.datagram.data_list[self.dev_index].get_value(self.action)
        self.root_item.append_child(ValueTreeViewItem([value], self.root_item))
        self.endResetModel()

    def get_value(self):
        item = self.root_item.child(0)
        # print(self, type(item.data(0)))
        return item.data(0)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
