

class DatagramTreeViewItem(object):
    def __init__(self, datagram, device_index, parent=None, display_data=None):
        self.parent_item = parent
        self.datagram = datagram
        self.id = device_index
        self.display_data = display_data
        self.child_items = []
        pass

    def append_child(self, item):
        self.child_items.append(item)
        pass

    def child(self, row):
        try:
            return self.child_items[row]
        except IndexError:
            return None
        pass

    def child_count(self):
        return len(self.child_items)
        pass

    def column_count(self):
        if self.display_data:
            return len(self.display_data)
        else:
            return 3
        pass

    def data(self, column):
        if self.display_data:
            try:
                return self.display_data[column]
            except IndexError:
                return None
        else:
            if column == 0:
                return self.datagram.get_topic(self.id)
                pass
            elif column == 1:
                return self.datagram.get_value(self.id)
                pass
            elif column == 2:
                try:
                    hash_str = '0x' + hex(self.datagram.id)[2:].upper()
                    return hash_str
                except IndexError:
                    return None
                except TypeError:
                    return None
                pass
            else:
                return None
        pass

    def parent(self):
        return self.parent_item
        pass

    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        else:
            return 0
        pass

    pass
