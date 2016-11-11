class ValueTreeViewItem(object):
    def __init__(self, data, parent=None):
        self.parent_item = parent
        self.user_data = data
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
        return len(self.user_data)

    def data(self, column):
        try:
            return self.user_data[column]
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
            self.user_data[column] = value
            return True
        except IndexError:
            return False
    pass
