from ValueTreeViewItem import ValueTreeViewItem
from ValueTreeViewModel import ValueTreeViewModel


class DataDictionaryTreeViewModel(ValueTreeViewModel):
    def __init__(self, datagram_manager, topic_indexes, parent=None):
        self.__datagram_manager = datagram_manager
        self.__topic_indexes = topic_indexes
        header = ('Data Dictionary Tree',)
        super(DataDictionaryTreeViewModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        for index in self.__topic_indexes:
            hash_id = index[0]
            instance = index[1]
            action = index[2]
            datagram = self.__datagram_manager.get_datagram(hash_id)
            if datagram is None:
                continue
            dev_data = datagram.get_device_data(instance)
            if dev_data is None:
                continue
            item_name_list = dev_data.get_topic(action).split('/')

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
