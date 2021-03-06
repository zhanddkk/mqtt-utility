from ValueTreeViewItem import ValueTreeViewItem


class ValueEditorTreeViewEnumTypeItem(ValueTreeViewItem):
    def __init__(self, name, value, attribute, parent):
        super(ValueEditorTreeViewEnumTypeItem, self).__init__(item_data=[name, value],
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
            for _key, _data in self.hide_data.special_data.items():
                if _data.value == self.item_data[1]:
                    return '{value} | {name}'.format(value=_data.value, name=_key)
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
                    if _value == self.hide_data.special_data[_name].value:
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
