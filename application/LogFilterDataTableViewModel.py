from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex


class LogFilterDataTableViewModel(QAbstractTableModel):
    def __init__(self, data_list=(), parent=None):
        super(LogFilterDataTableViewModel, self).__init__(parent)
        self.__data_list = list(data_list)

    @property
    def data_list(self):
        return self.__data_list
        pass

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data_list)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Hash ID'
            else:
                return None
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section

        return None

    def data(self, index, int_role=None):
        row = index.row()
        column = index.column()
        if int_role == Qt.DisplayRole or int_role == Qt.EditRole:
            try:
                hash_id = self.__data_list[row]
            except IndexError:
                return None
                pass
            if column == 0:
                return '0x{hash_id:>08X}'.format(hash_id=hash_id)
            else:
                return None

    def flags(self, index):
        if not index.isValid():
            return 0

        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, any_value, role=None):
        if role != Qt.EditRole:
            return False

        try:
            any_value = any_value.upper()
            if any_value.startswith('0X'):
                _value = int(any_value, base=16)
            else:
                _value = int(any_value)
            self.__data_list[index.row()] = _value
            getattr(self.dataChanged, 'emit')(index, index)
            return True
        except IndexError:
            return False
        except ValueError:
            return False

    def insertRow(self, position, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position)
        self.__data_list.insert(position, 0)
        self.endInsertRows()

        return True

    def removeRow(self, position, parent=QModelIndex(), *args, **kwargs):
        try:
            _data = self.__data_list[position]
        except IndexError:
            return False

        self.beginRemoveRows(parent, position, position)
        self.__data_list.remove(_data)
        self.endRemoveRows()
        return True
        pass

    pass


if __name__ == '__main__':
    pass
