from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel


class DataDictionaryTreeViewModel(ValueTreeViewModel):
    def __init__(self, datagram_manager, parent=None):
        self.datagram_manager = datagram_manager
        header = ('Topic Tree',)
        super(DataDictionaryTreeViewModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        for index in self.datagram_manager.index_list:
            datagram = self.datagram_manager.datagram_dict[index[0]]
            data = datagram.data_list[index[1]]
            item_name_list = data.get_topic(index[2]).split('/')
            item = self.root_item
            for i, item_name in enumerate(item_name_list):
                is_find = False
                for child_item in item.child_items:
                    if child_item.data(0) == item_name:
                        item = child_item
                        is_find = True
                if is_find is not True:
                    if i + 1 == len(item_name_list):
                        item_tmp = ValueTreeViewItem((item_name,), item, index)
                    else:
                        item_tmp = ValueTreeViewItem((item_name,), item)
                    item.append_child(item_tmp)
                    item = item_tmp
            pass
        self.endResetModel()
        pass
