from ValueTreeViewItem import ValueTreeViewItem


class DataDictionaryTreeViewDatagramItem(ValueTreeViewItem):
    def __init__(self, item_data, device_index, parent=None):
        super(DataDictionaryTreeViewDatagramItem, self).__init__(item_data, parent=parent, hide_data=device_index)
        self.is_selected_to_watch = False
        pass

    @property
    def datagram_index(self):
        return self.hide_data
        pass

    def data(self, column):
        try:
            return '√ {}'.format(self.item_data[column]) if self.is_selected_to_watch else self.item_data[column]
        except IndexError:
            return None
        pass
    pass


if __name__ == '__main__':
    pass
