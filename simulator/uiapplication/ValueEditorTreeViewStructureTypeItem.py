from ValueTreeViewItem import ValueTreeViewItem


class ValueEditorTreeViewStructureTypeItem(ValueTreeViewItem):
    def __init__(self, name, value, attribute, parent):
        super(ValueEditorTreeViewStructureTypeItem, self).__init__(item_data=[name, value],
                                                                   hide_data=attribute,
                                                                   parent=parent)

    @property
    def value(self):
        _value = []
        for item in self.child_items:
            _value.append(item.value)
        return _value
        pass

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
            return '...'
            pass
        else:
            return None

    def set_data(self, column, value):
        if column != 2:
            return False
        else:
            self.item_data[1] = value
            return True
    pass
