from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
from ValueEditorTreeViewArrayTypeItem import ValueEditorTreeViewArrayTypeItem
from ValueEditorTreeViewBasicTypeItem import ValueEditorTreeViewBasicTypeItem
from ValueEditorTreeViewBitmapTypeItem import ValueEditorTreeViewBitmapTypeItem
from ValueEditorTreeViewBitTypeItem import ValueEditorTreeViewBitTypeItem
from ValueEditorTreeViewEnumTypeItem import ValueEditorTreeViewEnumTypeItem
from ValueEditorTreeViewRootItem import ValueEditorTreeViewRootItem
from ValueEditorTreeViewStringTypeItem import ValueEditorTreeViewStringTypeItem
from ValueEditorTreeViewStructureTypeItem import ValueEditorTreeViewStructureTypeItem


class ValueEditorTreeViewModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(ValueEditorTreeViewModel, self).__init__(parent)
        self.__value = None
        self.__attribute = None
        self.root_item = ValueEditorTreeViewRootItem()
        self.__build_types = {
            'BasicType': self.__build_basic_type,
            'BitmapType': self.__build_bitmap_type,
            'EnumType': self.__build_enum_type,
            'StringType': self.__build_string_type,
            'ArrayType': self.__build_array_type,
            'StructureType': self.__build_structure_type
        }

    @property
    def value(self):
        self.__value = self.root_item.value
        return self.__value

    def set_value(self, value, attribute):
        self.__value = value
        self.__attribute = attribute
        if self.__attribute is None:
            return False
        self.__update()
        return True

    def __update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        self.__build(name='Value', value=self.__value, attribute=self.__attribute, parent_item=self.root_item)
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
        _parent_item = ValueEditorTreeViewStructureTypeItem(name=name,
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
        _parent_item = ValueEditorTreeViewArrayTypeItem(name=name,
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
        if attribute.basic_type == 'Float':
            if type(value) is not float:
                if type(value) is int:
                    _value = float(value)
                else:
                    _value = 0.0
            else:
                _value = value
        elif attribute.basic_type == 'Bool':
            if type(value) is not bool:
                _value = False
            else:
                _value = value
        else:
            if type(value) is not int:
                _value = 0
            else:
                _value = value
        parent_item.append_child(ValueEditorTreeViewBasicTypeItem(name=name,
                                                                  value=_value,
                                                                  attribute=attribute,
                                                                  parent=parent_item))

    @staticmethod
    def __build_string_type(name, value, attribute, parent_item):
        if type(value) is not str:
            _value = ''
        else:
            _value = value
        parent_item.append_child(ValueEditorTreeViewStringTypeItem(name=name,
                                                                   value=_value,
                                                                   attribute=attribute,
                                                                   parent=parent_item))
        pass

    @staticmethod
    def __build_bitmap_type(name, value, attribute, parent_item):
        if type(value) is not int:
            _value = 0
        else:
            _value = value
        _parent_item = ValueEditorTreeViewBitmapTypeItem(name=name,
                                                         value=_value,
                                                         attribute=attribute,
                                                         parent=parent_item)
        parent_item.append_child(_parent_item)
        if attribute.special_data:
            _start = 0
            _end = 0
            for _key, _data in attribute.special_data.items():
                _end += _data.wide
                bit_value = _value & ((1 << _data.wide) - 1)
                _sub_item = ValueEditorTreeViewBitTypeItem(name=_key,
                                                           value=bit_value,
                                                           bit_fields=(_start, _end - 1),
                                                           attribute=_data,
                                                           parent=_parent_item)
                _parent_item.append_child(_sub_item)
                _value >>= _data.wide
                _start = _end

    @staticmethod
    def __build_enum_type(name, value, attribute, parent_item):
        if type(value) is not int:
            _value = 0
        else:
            _value = value
        parent_item.append_child(ValueEditorTreeViewEnumTypeItem(name=name,
                                                                 value=_value,
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

        item = self.get_item(index)
        if (item != self.root_item) and (index.column() == 2):
            if item.child_count() == 0:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return Qt.ItemIsEnabled

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

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.get_item(index)
        result = item.set_data(index.column(), value)
        try:
            if item.hide_data.wide > 0:
                _bit_value = item.value
                _bit_start = item.bit_fields[0]
                _bit_end = item.bit_fields[1]
                _parent = self.parent(index)
                _parent_item = self.get_item(_parent)
                _mask = ~(((1 << (_bit_end + 1)) - 1) - ((1 << _bit_start) - 1))
                _value = _parent_item.value & _mask
                _value |= _bit_value << _bit_start
                _parent_value_index = self.index(_parent.row(), 2, parent=_parent.parent())
                self.setData(_parent_value_index, _value, role=Qt.EditRole)
        except AttributeError:
            pass

        if result:
            getattr(self, 'dataChanged').emit(index, index)

        return result
