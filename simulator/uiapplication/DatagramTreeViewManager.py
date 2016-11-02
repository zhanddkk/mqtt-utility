from simulator.uiapplication.DatagramTreeViewItem import DatagramTreeViewItem


class DatagramTreeViewManager:
    def __init__(self, datagram_manager):
        self.id_list = datagram_manager.index_list
        self.datagram_manager = datagram_manager

    def build_list_view(self, root_item):
        for ids in self.id_list:
            hash_id = 0xffffffff
            try:
                hash_id = ids[0]
            except IndexError:
                pass
            dg = self.datagram_manager.get_datagram_by_id(hash_id)
            dev_index = 0
            try:
                dev_index = ids[1]
            except IndexError:
                pass
            child_item = DatagramTreeViewItem(dg, dev_index, root_item)
            root_item.append_child(child_item)
        pass

    def get_list_view_row(self, hash_id, device_index):
        is_find = False
        row = 0
        for index, ids in enumerate(self.id_list):
            try:
                _hash_id = ids[0]
                _dev_index = ids[1]
            except IndexError:
                print('Index error when get row')
                return None
            if (_hash_id == hash_id) and (_dev_index == device_index):
                row += index
                is_find = True
                break
        if is_find:
            return row
        else:
            return None
        pass
    pass
