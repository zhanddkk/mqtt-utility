from ValueTreeViewItem import ValueTreeViewItem
from ValueTreeViewModel import ValueTreeViewModel
from DataDictionaryTreeViewItem import DataDictionaryTreeViewDatagramItem
from ddclient.dgpayload import E_DATAGRAM_ACTION_PUBLISH


class DataDictionaryTreeViewModel(ValueTreeViewModel):
    def __init__(self, datagram_manager, topic_indexes, parent=None):
        self.__datagram_manager = datagram_manager
        self.__topic_indexes = topic_indexes
        self.__item_map = {}
        header = ('Data Dictionary Tree',)
        super(DataDictionaryTreeViewModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        self.__item_map.clear()
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
            if not item_name_list:
                continue

            if action != E_DATAGRAM_ACTION_PUBLISH:
                _action_text = item_name_list.pop(0)
                item_name_list.append(_action_text)

            item = self.root_item
            for i, item_name in enumerate(item_name_list):
                is_find = False
                for child_item in item.child_items:
                    if child_item.data(0) == item_name:
                        item = child_item
                        is_find = True
                if is_find is not True:
                    if i + 1 == len(item_name_list):
                        if action == E_DATAGRAM_ACTION_PUBLISH:
                            item_tmp = DataDictionaryTreeViewDatagramItem((item_name,), index, item)
                        else:
                            item_tmp = ValueTreeViewItem((item_name,), item, index)
                        self.__item_map[(hash_id, instance)] = item_tmp
                    else:
                        item_tmp = ValueTreeViewItem((item_name,), item)
                    item.append_child(item_tmp)
                    item = item_tmp
            pass
        self.endResetModel()

    def set_selected_state_to_watch(self, index, state):
        _ret = False
        item = self.get_item(index)
        try:
            item.is_selected_to_watch = state
            getattr(self.dataChanged, 'emit')(index, index)
            _ret = True
        except AttributeError:
            pass
        return _ret
        pass

    @property
    def datagram_item_map(self):
        return self.__item_map

    def get_datagram_item(self, hash_id, device_index):
        try:
            return self.__item_map[(hash_id, device_index)]
        except IndexError:
            return None
        pass
