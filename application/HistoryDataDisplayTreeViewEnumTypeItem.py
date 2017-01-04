from ValueTreeViewItem import ValueTreeViewItem


class HistoryDataDisplayTreeViewEnumTypeItem(ValueTreeViewItem):
    def __init__(self, name, value, attribute, parent):
        super(HistoryDataDisplayTreeViewEnumTypeItem, self).__init__(item_data=[name, value],
                                                                     hide_data=attribute,
                                                                     parent=parent)

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
            for _key, _data in self.hide_data.special_data.items():
                if _data == self.item_data[1]:
                    return '{value} | {name}'.format(value=_data, name=_key)
            return str(self.item_data[1])
            pass
        else:
            return None

    def set_data(self, column, value):
        return False
    pass
