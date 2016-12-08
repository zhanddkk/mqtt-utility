from simulator.uiapplication.ValueTreeViewItem import ValueTreeViewItem
from simulator.uiapplication.ValueTreeViewModel import ValueTreeViewModel
# from simulator.core import PayloadPackage


class BitMapValueDspModel(ValueTreeViewModel):
    def __init__(self, datagram, index, bit_format, parent=None):
        self.datagram = datagram
        self.dev_index = index[1]
        self.action = index[2]
        self.bit_format = bit_format
        header = ['Operation', 'Time']
        for bit_field in reversed(self.bit_format.fields):
            header.append(bit_field)

        super(BitMapValueDspModel, self).__init__(header, parent)

    def update(self):
        self.beginResetModel()
        self.root_item.clear_children()
        try:
            history_values = self.datagram.data_list[self.dev_index].get_history(self.action)
            for history in reversed(history_values):
                line_data = [history.opt_str, history.time_str]
                value = history.value
                for bit_field in reversed(self.bit_format.fields):
                    tmp_val = value & ((1 << getattr(self.bit_format, bit_field)[0]) - 1)
                    dsp_val = str(tmp_val)
                    choice_list = getattr(self.bit_format, bit_field)[1]
                    if type(choice_list) is dict:
                        if tmp_val in choice_list:
                            dsp_val += ' | ' + getattr(self.bit_format, bit_field)[1][tmp_val]
                    value >>= getattr(self.bit_format, bit_field)[0]
                    line_data.append(dsp_val)
                self.root_item.append_child(ValueTreeViewItem(line_data, self.root_item))
        except IndexError:
            print('ERROR:', 'Index error')
        self.endResetModel()
        pass


def print_bit_map(bit_format, value):
    for bit_field in reversed(bit_format.fields):
        tmp_val = value & ((1 << getattr(bit_format, bit_field)[0]) - 1)
        dsp_val = str(tmp_val)
        choice_list = getattr(bit_format, bit_field)[1]
        if type(choice_list) is dict:
            if tmp_val in choice_list:
                dsp_val += ' | ' + getattr(bit_format, bit_field)[1][tmp_val]
        value >>= getattr(bit_format, bit_field)[0]
        print(bit_field, '=', dsp_val)
    pass


def encode_bit_map(bit_format, *args):

    pass

if __name__ == '__main__':
    from simulator.core.NameClass import NameClass
    cmd_bit_format_class = NameClass('CmdBitFormatClass', 'producer, sequence, ack_cmd_code').new_class
    setting_response_bit_format_class = NameClass('SettingRespBitFormatClass', 'producer, error_code').new_class

    cmd_bit_format = cmd_bit_format_class(producer=[8, {0: 'UC', 1: 'SLC_UPS', 2: 'SLC_NMC', 3: 'HMI', 4: 'TUNER'}],
                                          sequence=[16, None],
                                          ack_cmd_code=[8, {0: 'Rest', 1: 'Set', 0x10: 'Idle',
                                                            0x11: 'Receive',
                                                            0x12: 'Completed',
                                                            0x13: 'Locked',
                                                            0x14: 'Refused'}])
    setting_response_bit_format = setting_response_bit_format_class(producer=[16, {0: 'UC',
                                                                                   1: 'SLC_UPS',
                                                                                   2: 'SLC_NMC',
                                                                                   3: 'HMI',
                                                                                   4: 'TUNER'}],
                                                                    error_code=[16, {0: 'OK'}])
    command = (3 << 24) | (7 << 8) | 0x13
    response = (4 << 16) | 5

    print_bit_map(cmd_bit_format, command)
    print_bit_map(setting_response_bit_format, response)

    command_bit_fields = [19, 7, 3]

    pass
