from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class ListValueDspTreeModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        self.action = 0
        self.value_size = datagram.attribute.max_size
        header = ['Operation', 'Time', self.datagram.attribute.format]
        if self.value_size and self.value_size > 1:
            for i in range(1, self.value_size):
                header.append(self.datagram.attribute.format)
        super(ListValueDspTreeModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        try:
            history_values = self.datagram.data_list[self.dev_index].get_history(self.action)
            for history in reversed(history_values):
                if self.value_size is not None and self.value_size > 1:
                    item_data = [history.opt_str, history.time_str]
                    for i in range(0, self.value_size):
                        try:
                            item_data.append(history.value[i])
                        except IndexError:
                            item_data.append(None)
                        except TypeError:
                            item_data.append(None)
                else:
                    item_data = (history.opt_str, history.time_str, history.value)
                self.root_item.append_child(ValueTreeViewItem(item_data, self.root_item))
        except IndexError:
            print('ERROR:', 'Index error')
        self.endResetModel()
        pass
