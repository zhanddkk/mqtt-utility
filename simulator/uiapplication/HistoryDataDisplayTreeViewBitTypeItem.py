from ValueTreeViewItem import ValueTreeViewItem


class HistoryDataDisplayTreeViewBitTypeItem(ValueTreeViewItem):
    def __init__(self, name, value, bit_fields, attribute, parent):
        super(HistoryDataDisplayTreeViewBitTypeItem, self).__init__(item_data=[name, value],
                                                                    hide_data=attribute,
                                                                    parent=parent)
        self.__bit_fields = bit_fields

    @property
    def value(self):
        return self.item_data[1]

    @property
    def bit_fields(self):
        return self.__bit_fields

    def column_count(self):
        return 4

    def data(self, column):
        if column == 0:
            return self.item_data[0]
            pass
        elif column == 1:
            return 'bit {start}:{end}'.format(start=self.__bit_fields[0], end=self.__bit_fields[1])
            pass
        elif column == 2:
            if self.hide_data.names:
                for _key, _data in self.hide_data.names.items():
                    if _data == self.item_data[1]:
                        return '{value} | {name}'.format(value=_data, name=_key)
            return str(self.item_data[1])
            pass
        else:
            return None

    def set_data(self, column, value):
        return False
    pass
