from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
from ValueTreeViewItem import ValueTreeViewItem
from HistoryDataDisplayTreeViewBasicTypeItem import HistoryDataDisplayTreeViewBasicTypeItem
from HistoryDataDisplayTreeViewStringTypeItem import HistoryDataDisplayTreeViewStringTypeItem
from HistoryDataDisplayTreeViewBitmapTypeItem import HistoryDataDisplayTreeViewBitmapTypeItem
from HistoryDataDisplayTreeViewBitTypeItem import HistoryDataDisplayTreeViewBitTypeItem
from HistoryDataDisplayTreeViewArrayTypeItem import HistoryDataDisplayTreeViewArrayTypeItem
from HistoryDataDisplayTreeViewStructureTypeItem import HistoryDataDisplayTreeViewStructureTypeItem
from HistoryDataDisplayTreeViewEnumTypeItem import HistoryDataDisplayTreeViewEnumTypeItem


class HistoryDataDisplayTreeViewModel(QAbstractItemModel):
    def __init__(self, display_reversed=True, parent=None):
        super(HistoryDataDisplayTreeViewModel, self).__init__(parent)
        self.root_item = ValueTreeViewItem(('Time/Name', 'Operation/Type', 'Data'), None)
        self.__history_data = None
        self.__value_attribute = None
        self.__additional_data_value_attribute = None
        self.is_reversed = display_reversed
        self.__build_types = {
            'BasicType': self.__build_basic_type,
            'BitmapType': self.__build_bitmap_type,
            'EnumType': self.__build_enum_type,
            'StringType': self.__build_string_type,
            'ArrayType': self.__build_array_type,
            'StructureType': self.__build_structure_type
        }

    def set_value(self, history_data, value_attribute, additional_data_value_attribute=None):
        if (history_data is None) or (value_attribute is None):
            return False
        self.__history_data = history_data
        self.__value_attribute = value_attribute
        self.__additional_data_value_attribute = additional_data_value_attribute
        self.__update()
        pass

    def __update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        if self.is_reversed:
            _tmp_data = reversed(self.__history_data)
        else:
            _tmp_data = self.__history_data
        for item in _tmp_data:
            _value_root_item = ValueTreeViewItem((item.data_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                  'Send' if item.operation == 0 else 'Receive',
                                                  '<{}>'.format(item.value)), self.root_item)
            self.root_item.append_child(_value_root_item)
            self.__build(name='Value', value=item.value, attribute=self.__value_attribute, parent_item=_value_root_item)
            if (self.__additional_data_value_attribute is None) or (item.additional_data is None):
                continue
            self.__build(name=item.additional_data.name,
                         value=item.additional_data.value,
                         attribute=self.__additional_data_value_attribute,
                         parent_item=_value_root_item)
        self.endResetModel()
        pass

    def __build(self, name, value, attribute, parent_item):
        try:
            self.__build_types[attribute.system_tag](name=name,
                                                     value=value,
                                                     attribute=attribute,
                                                     parent_item=parent_item)
        except KeyError:
            pass
        pass

    def __build_structure_type(self, name, value, attribute, parent_item):
        _parent_item = HistoryDataDisplayTreeViewStructureTypeItem(name=name,
                                                                   value=value,
                                                                   attribute=attribute,
                                                                   parent=parent_item)
        parent_item.append_child(_parent_item)
        _attribute = attribute.special_data
        i = 0
        for _key, _data in _attribute.items():
            try:
                _value = value[i]
            except IndexError:
                _value = None
            except TypeError:
                _value = None
            self.__build(name='{name}'.format(name=_key),
                         value=_value,
                         attribute=_data,
                         parent_item=_parent_item)
            i += 1
            pass
        pass

    def __build_array_type(self, name, value, attribute, parent_item):
        _parent_item = HistoryDataDisplayTreeViewArrayTypeItem(name=name,
                                                               value=value,
                                                               attribute=attribute,
                                                               parent=parent_item)
        parent_item.append_child(_parent_item)
        for i in range(attribute.array_count):
            _attribute = attribute.special_data
            try:
                _value = value[i]
            except IndexError:
                _value = None
            except TypeError:
                _value = None
            self.__build(name='[{index}]'.format(index=i),
                         value=_value,
                         attribute=_attribute,
                         parent_item=_parent_item)
        pass

    @staticmethod
    def __build_basic_type(name, value, attribute, parent_item):
        parent_item.append_child(HistoryDataDisplayTreeViewBasicTypeItem(name=name,
                                                                         value=value,
                                                                         attribute=attribute,
                                                                         parent=parent_item))
        pass

    @staticmethod
    def __build_string_type(name, value, attribute, parent_item):
        parent_item.append_child(HistoryDataDisplayTreeViewStringTypeItem(name=name,
                                                                          value=value,
                                                                          attribute=attribute,
                                                                          parent=parent_item))
        pass

    @staticmethod
    def __build_bitmap_type(name, value, attribute, parent_item):
        _parent_item = HistoryDataDisplayTreeViewBitmapTypeItem(name=name,
                                                                value=value,
                                                                attribute=attribute,
                                                                parent=parent_item)
        parent_item.append_child(_parent_item)
        if attribute.special_data:
            if type(value) is not int:
                _start = 0
                _end = 0
                for _key, _data in attribute.special_data.items():
                    _end += _data.wide
                    _sub_item = HistoryDataDisplayTreeViewBitTypeItem(name=_key,
                                                                      value='Invalid',
                                                                      bit_fields=(_start, _end - 1),
                                                                      attribute=_data,
                                                                      parent=_parent_item)
                    _parent_item.append_child(_sub_item)
                    _start = _end
                pass
            else:
                _start = 0
                _end = 0
                for _key, _data in attribute.special_data.items():
                    _end += _data.wide
                    bit_value = value & ((1 << _data.wide) - 1)
                    _sub_item = HistoryDataDisplayTreeViewBitTypeItem(name=_key,
                                                                      value=bit_value,
                                                                      bit_fields=(_start, _end - 1),
                                                                      attribute=_data,
                                                                      parent=_parent_item)
                    _parent_item.append_child(_sub_item)
                    value >>= _data.wide
                    _start = _end
            pass

    @staticmethod
    def __build_enum_type(name, value, attribute, parent_item):
        parent_item.append_child(HistoryDataDisplayTreeViewEnumTypeItem(name=name,
                                                                        value=value,
                                                                        attribute=attribute,
                                                                        parent=parent_item))
        pass

    def columnCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.root_item.column_count()

    def data(self, index, role=None):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root_item.data(section)

        return None

    def index(self, row, column, parent=None, *args, **kwargs):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def parent(self, index=None):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def get_item(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.root_item
    pass

if __name__ == '__main__':
    pass
