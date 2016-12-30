from ValueTreeViewItem import ValueTreeViewItem


class ValueEditorTreeViewBasicTypeItem(ValueTreeViewItem):
    def __init__(self, name, value, attribute, parent):
        super(ValueEditorTreeViewBasicTypeItem, self).__init__(item_data=[name, value],
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
            return str(self.item_data[1])
            pass
        else:
            return None

    def set_data(self, column, value):
        if column != 2:
            return False
        else:
            if self.hide_data.basic_type == 'Bool':
                try:
                    if value == 'True':
                        self.item_data[1] = True
                    elif value == 'False':
                        self.item_data[1] = False
                    else:
                        return False
                except ValueError:
                    return False
                    pass
            elif self.hide_data.basic_type == 'Float':
                try:
                    self.item_data[1] = float(value)
                except ValueError:
                    return False
                    pass
            else:
                value = value.upper()
                try:
                    if value.startswith('0X'):
                        self.item_data[1] = int(value, base=16)
                    else:
                        self.item_data[1] = int(value)
                except ValueError:
                    return False
                    pass
        return True
    pass

