from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class DictionaryValueDspTreeModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        header = ('Operation', 'Time', 'Name', self.datagram.attribute.format)
        super(DictionaryValueDspTreeModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        try:
            d = self.datagram.data_list[self.dev_index]
            for history in reversed(d.history):
                name = 'NO DEFINE'
                value = history.value
                for (k, d) in self.datagram.attribute.choice_list.items():
                    if d == value:
                        name = k
                        break
                self.root_item.append_child(ValueTreeViewItem((history.opt_str, history.time_str, name, value),
                                                              self.root_item))
        except IndexError:
            print('ERROR:', 'Index error')
        self.endResetModel()
        pass
