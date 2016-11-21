from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class GeneralValueDspTreeViewModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        header = ('Operation', 'Time', self.datagram.attribute.format)
        super(GeneralValueDspTreeViewModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        try:
            history_values = self.datagram.data_list[self.dev_index].history
            for history in reversed(history_values):
                value = history.value
                self.root_item.append_child(ValueTreeViewItem((history.opt_str, history.time_str, value),
                                                              self.root_item))
        except IndexError:
            print('ERROR:', 'Index error')
        self.endResetModel()
        pass
