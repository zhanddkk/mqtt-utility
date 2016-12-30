from ValueTreeViewItem import ValueTreeViewItem


class ValueEditorTreeViewRootItem(ValueTreeViewItem):
    def __init__(self):
        super(ValueEditorTreeViewRootItem, self).__init__(('Name', 'Type', 'Data'))

    @property
    def value(self):
        _value = []
        for item in self.child_items:
            _value.append(item.value)
        if _value:
            if len(_value) == 1:
                return _value[0]
            else:
                return _value
        else:
            return None
    pass
