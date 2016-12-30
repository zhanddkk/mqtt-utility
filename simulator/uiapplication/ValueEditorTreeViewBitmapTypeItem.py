from ValueTreeViewItem import ValueTreeViewItem


class ValueEditorTreeViewBitmapTypeItem(ValueTreeViewItem):
    def __init__(self, name, value, attribute, parent):
        super(ValueEditorTreeViewBitmapTypeItem, self).__init__(item_data=[name, value],
                                                                hide_data=attribute,
                                                                parent=parent)

    @property
    def value(self):
        return self.item_data[1]

    def column_count(self):
        return 3

    def data(self, column):
        if column == 0:
            return self.item_data[0]
            pass
        elif column == 1:
            return self.hide_data.type_name
            pass
        elif column == 2:
            return '0b{:b}'.format(self.item_data[1])
            pass
        else:
            return None

    def set_data(self, column, value):
        if column != 2:
            return False
        else:
            if type(value) is int:
                self.item_data[1] = value
                return True
            else:
                return False
    pass
