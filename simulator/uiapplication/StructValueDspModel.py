from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class StructValueDspModel(ValueTreeViewModel):
    def __init__(self, datagram, dev_index, parent=None):
        self.datagram = datagram
        self.dev_index = dev_index
        self.action = 0
        header = ['Operation', 'Time']
        for (k, d) in self.datagram.attribute.choice_list.items():
            header.append(k + '\n' + d[0])
            pass
        super(StructValueDspModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        try:
            history_values = self.datagram.data_list[self.dev_index].get_history(self.action)
            for history in reversed(history_values):
                value = history.value
                data_list = [history.opt_str, history.time_str]
                for v in value:
                    data_list.append(v)
                self.root_item.append_child(ValueTreeViewItem(data_list, self.root_item))
        except IndexError:
            print('ERROR:', 'Index error')
        self.endResetModel()
        pass
