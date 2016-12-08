from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class DictionaryValueDspTreeModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        self.action = 0
        header = ('Operation', 'Time', 'Name', self.datagram.attribute.format)
        super(DictionaryValueDspTreeModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        try:
            history_value = self.datagram.data_list[self.dev_index].get_history(self.action)
            for history in reversed(history_value):
                name = 'NO DEFINE'
                value = history.value
                for (k, d) in self.datagram.attribute.choice_list.items():
                    if d[0] == value:
                        name = k
                        break
                self.root_item.append_child(ValueTreeViewItem((history.opt_str, history.time_str, name, value),
                                                              self.root_item))
        except IndexError:
            print('ERROR:', 'Index error')
        self.endResetModel()
        pass
