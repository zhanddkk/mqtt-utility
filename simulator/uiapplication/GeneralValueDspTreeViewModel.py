from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueViewModel


class GeneralValueDspTreeViewModel(ValueViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        header = ('Operation', 'Time', self.datagram.property.format)
        super(GeneralValueDspTreeViewModel, self).__init__(header, parent)

    def update(self):
        self.root_item.clear_children()
        try:
            history_values = self.datagram.history[self.dev_index]
            for history in reversed(history_values):
                opt = 'Receive' if history[0] == 0 else 'Send'
                time = history[1].strftime("%Y-%m-%d %H:%M:%S")
                value = history[2]
                self.root_item.append_child(ValueTreeViewItem((opt, time, value), self.root_item))
        except IndexError:
            print('Index error')
            return
        pass
