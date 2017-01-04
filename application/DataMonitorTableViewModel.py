from PyQt5.QtCore import QAbstractTableModel, Qt


class DataMonitorTableViewModel(QAbstractTableModel):
    def __init__(self, datagram_manager, parent=None):
        super(DataMonitorTableViewModel, self).__init__(parent)
        self.__datagram_manager = datagram_manager
        self.__topic_indexes = []

    @property
    def topic_indexes(self):
        return self.__topic_indexes

    def get_row(self, hash_id, instance, action):
        try:
            return self.__topic_indexes.index((hash_id, instance, action))
            pass
        except ValueError:
            return None
            pass
        pass

    def update(self, topic_indexes):
        self.beginResetModel()
        self.__topic_indexes = list(topic_indexes)
        self.endResetModel()
        pass

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__topic_indexes)

    def columnCount(self, parent=None, *args, **kwargs):
        return 4

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Hash ID'
            elif section == 1:
                return 'Device Index'
            elif section == 2:
                return 'Value'
            elif section == 3:
                return 'Topic'
            else:
                return None
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section

        return None

    def data(self, index, int_role=None):
        row = index.row()
        column = index.column()
        if int_role == Qt.DisplayRole:
            try:
                hash_id = self.__topic_indexes[row][0]
                instance = self.__topic_indexes[row][1]
                action = self.__topic_indexes[row][2]
            except IndexError:
                return None
                pass
            if column == 0:
                return '0x{hash_id:>08X}'.format(hash_id=hash_id)
            elif column == 1:
                return str(instance + 1)
            elif column == 2:
                dg = self.__datagram_manager.get_datagram(hash_id)
                if dg is None:
                    return None
                value = dg.get_device_data_value(instance, action)
                return str(value)
                pass
            elif column == 3:
                dg = self.__datagram_manager.get_datagram(hash_id)
                if dg is None:
                    return None
                dev_data = dg.get_device_data(instance)
                topic = dev_data.get_topic(action)
                return topic
                pass
            else:
                return None
    pass
