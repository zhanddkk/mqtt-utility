from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueViewModel


class DictionaryValueDspTreeModel(ValueViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        header = ('Operation', 'Time', 'Name', self.datagram.property.format)
        super(DictionaryValueDspTreeModel, self).__init__(header, parent)

    def update(self):
        self.root_item.clear_children()
        try:
            history_values = self.datagram.history[self.dev_index]
            for history in reversed(history_values):
                opt = 'Receive' if history[0] == 0 else 'Send'
                time = history[1].strftime("%Y-%m-%d %H:%M:%S")
                name = 'NO DEFINE'
                value = history[2]
                for (k, d) in self.datagram.property.choice_list.items():
                    if d == value:
                        name = k
                        break
                self.root_item.append_child(ValueTreeViewItem((opt, time, name, value), self.root_item))
        except IndexError:
            print('Index error')
            return
        pass
