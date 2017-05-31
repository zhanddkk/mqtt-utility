from PyQt5.QtCore import QModelIndex
from ValueTreeViewItem import ValueTreeViewItem
from ValueTreeViewModel import ValueTreeViewModel
from DataDictionaryTreeViewItem import DataDictionaryTreeViewDatagramItem
from ddclient.dgpayload import E_DATAGRAM_ACTION_PUBLISH


class DataDictionaryTreeViewModel(ValueTreeViewModel):
    def __init__(self, datagram_manager, topic_indexes, msg_filter_cfg, parent=None):
        self.__datagram_manager = datagram_manager
        self.__topic_indexes = topic_indexes
        self.__msg_filter_cfg = msg_filter_cfg
        header = ('Data Dictionary Tree',)
        super(DataDictionaryTreeViewModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        for _index in self.__topic_indexes:
            _hash_id, _dev_index, _action = _index
            if _action != E_DATAGRAM_ACTION_PUBLISH:
                continue
            _dg = self.__datagram_manager.get_datagram(_hash_id)
            if _dg is None:
                continue
            _dev_data = _dg.get_device_data(_dev_index)
            if _dev_data is None:
                continue
            _item_name_list = _dev_data.get_topic(_action).split('/')
            if not _item_name_list:
                continue

            # Build items for tree view
            _item = self.root_item
            for i, _item_name in enumerate(_item_name_list):
                _is_find = False
                for _child_item in _item.child_items:
                    if _child_item.data(0) == _item_name:
                        _item = _child_item
                        _is_find = True
                if not _is_find:
                    if i + 1 == len(_item_name_list):
                        _item_tmp = DataDictionaryTreeViewDatagramItem((_item_name,), _index, _item)
                        _item_tmp.is_selected_to_watch = self.__msg_filter_cfg.is_item_exist(_hash_id, _dev_index)
                    else:
                        _item_tmp = ValueTreeViewItem((_item_name,), _item)
                    _item.append_child(_item_tmp)
                    _item = _item_tmp
            pass
        self.endResetModel()
        pass

    def select_to_watch(self, index, state):
        _item = self.get_item(index)
        try:
            _item.is_selected_to_watch = state
            _hash_id = _item.datagram_index[0]
            _dev_index = _item.datagram_index[1]
            if state:
                self.__msg_filter_cfg.add_item(_hash_id, _dev_index)
            else:
                self.__msg_filter_cfg.remove_item(_hash_id, _dev_index)
            getattr(self.dataChanged, 'emit')(index, index)
        except AttributeError:
            pass
        pass

    def update_selections(self):
        # Update all items
        _row_count = self.rowCount(QModelIndex())
        for _row in range(_row_count):
            _model_index = self.index(_row, 0, QModelIndex())
            self.__update_selection(_model_index)
            pass
        pass

    def __update_selection(self, _model_index):
        _item = self.get_item(_model_index)
        _row_count = _item.child_count()

        # Loop for all children's index
        for _row in range(_row_count):
            _child_model_index = _model_index.child(_row, 0)
            self.__update_selection(_child_model_index)
            pass

        # Update current index
        try:
            _hash_id = _item.datagram_index[0]
            _dev_index = _item.datagram_index[1]
            if self.__msg_filter_cfg.is_item_exist(_hash_id, _dev_index):
                self.select_to_watch(_model_index, True)
            else:
                self.select_to_watch(_model_index, False)
        except AttributeError:
            pass
        pass
