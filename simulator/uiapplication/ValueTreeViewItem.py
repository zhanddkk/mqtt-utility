class ValueTreeViewItem(object):
    def __init__(self, item_data, parent=None, hide_data=None):
        self.parent_item = parent
        self.item_data = item_data
        self.hide_data = hide_data
        self.child_items = []
        pass

    def clear_children(self):
        self.child_items.clear()

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
        return len(self.item_data)

    def data(self, column):
        try:
            return self.item_data[column]
        except IndexError:
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

    def set_data(self, column, value):
        try:
            self.item_data[column] = value
            return True
        except IndexError:
            return False
    pass
