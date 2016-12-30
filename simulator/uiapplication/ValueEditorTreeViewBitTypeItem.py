from ValueTreeViewItem import ValueTreeViewItem


class ValueEditorTreeViewBitTypeItem(ValueTreeViewItem):
    def __init__(self, name, value, bit_fields, attribute, parent):
        super(ValueEditorTreeViewBitTypeItem, self).__init__(item_data=[name, value],
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
        return 3

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
        if column != 2:
            return False
        else:
            value_name = value.split('|')
            if len(value_name) == 1:
                _value = value_name[0].strip(' ').upper()
                try:
                    if _value.startswith('0X'):
                        self.item_data[1] = int(_value, base=16)
                    else:
                        self.item_data[1] = int(_value)
                except ValueError:
                    return False
                    pass
                pass
            elif len(value_name) == 2:
                _value = value_name[0].strip(' ').upper()
                _name = value_name[1].strip(' ')
                try:
                    if _value.startswith('0X'):
                        _value = int(_value, base=16)
                    else:
                        _value = int(_value)
                except ValueError:
                    return False
                    pass
                try:
                    if _value == self.hide_data.names[_name]:
                        self.item_data[1] = _value
                    else:
                        return False
                except KeyError:
                    return False
                except TypeError:
                    return False
                pass
            else:
                return False
            return True
    pass
