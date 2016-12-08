from PyQt5.QtCore import QAbstractTableModel, Qt


class DataMonitorTableViewModel(QAbstractTableModel):
    def __init__(self, datagram_manager, parent=None):
        super(DataMonitorTableViewModel, self).__init__(parent)
        self.datagram_manager = datagram_manager
        self.datagram_index = datagram_manager.index_list

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.datagram_index)

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
                hash_id = self.datagram_index[row][0]
                dev_index = self.datagram_index[row][1]
            except KeyError:
                return None
                pass
            except IndexError:
                return None
                pass
            if column == 0:
                return '0x' + '{0:0>8}'.format(hex(hash_id)[2:].upper())
            elif column == 1:
                return str(dev_index + 1)
            elif column == 2:
                dg = self.datagram_manager.datagram_dict[hash_id]
                d = dg.data_list[dev_index]
                return str(d.get_value(self.datagram_index[row][2]))
                pass
            elif column == 3:
                dg = self.datagram_manager.datagram_dict[hash_id]
                d = dg.data_list[dev_index]
                return str(d.get_topic(self.datagram_index[row][2]))
                pass
            else:
                return None
    pass
