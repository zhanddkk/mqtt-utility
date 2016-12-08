from PyQt5.QtCore import Qt
from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel
# from simulator.core import PayloadPackage


class BitMapValueEditModel(ValueTreeViewModel):
    def __init__(self, datagram, index, bit_format, value=None, parent=None):
        self.datagram = datagram
        self.dev_index = index[1]
        self.action = index[2]
        self.bit_format = bit_format
        self.value = value
        header = ('Name', 'Value')
        super(BitMapValueEditModel, self).__init__(header, parent)
    pass

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        if self.value is None:
            value = self.datagram.data_list[self.dev_index].get_value(self.action)
        else:
            value = self.value
        for bit_field in reversed(self.bit_format.fields):
            line_data = [bit_field]
            tmp_val = value & ((1 << getattr(self.bit_format, bit_field)[0]) - 1)
            dsp_val = str(tmp_val)
            choice_list = getattr(self.bit_format, bit_field)[1]
            if type(choice_list) is dict:
                if tmp_val in choice_list:
                    dsp_val += ' | ' + getattr(self.bit_format, bit_field)[1][tmp_val]
            value >>= getattr(self.bit_format, bit_field)[0]
            line_data.append(dsp_val)
            self.root_item.append_child(ValueTreeViewItem(line_data, self.root_item))
        self.endResetModel()

    def get_value(self):
        val = 0
        i = 0
        for bit_field in self.bit_format.fields:
            i += 1
            row = len(self.bit_format.fields) - i
            item = self.root_item.child(row)
            val <<= getattr(self.bit_format, bit_field)[0]
            tmp_val = str(item.data(1))
            tmp_val = tmp_val.split('|')[0].strip(' ')
            try:
                tmp_val = tmp_val.upper()
                if tmp_val.startswith('0X'):
                    tmp_val = int(tmp_val, base=16)
                else:
                    tmp_val = int(tmp_val)
            except ValueError:
                print('ERROR:', 'input value error')
                pass
            val |= tmp_val & ((1 << getattr(self.bit_format, bit_field)[0]) - 1)
        self.value = val
        return val

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
