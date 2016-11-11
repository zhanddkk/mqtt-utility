from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueViewModel


class ListValueDspTreeModel(ValueViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        self.value_size = datagram.property.max_size
        header = ['Operation', 'Time', self.datagram.property.format]
        if self.value_size and self.value_size > 1:
            for i in range(1, self.value_size):
                header.append(self.datagram.property.format)
        super(ListValueDspTreeModel, self).__init__(header, parent)

    def update(self):
        self.root_item.clear_children()
        try:
            history_values = self.datagram.history[self.dev_index]
            for history in reversed(history_values):
                opt = 'Receive' if history[0] == 0 else 'Send'
                time = history[1].strftime("%Y-%m-%d %H:%M:%S")
                if self.value_size is not None and self.value_size > 1:
                    item_data = [opt, time]
                    for i in range(0, self.value_size):
                        try:
                            item_data.append(history[2][i])
                        except IndexError:
                            item_data.append(None)
                        except TypeError:
                            item_data.append(None)
                else:
                    item_data = (opt, time, history[2])
                self.root_item.append_child(ValueTreeViewItem(item_data, self.root_item))
        except IndexError:
            print('Index error')
            return
        pass
