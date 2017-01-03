from .NamedList import named_list
bit_map_item_type = named_list('BitMapItem', 'bit_wide, value_dict')
bit_map_item_Data_type = named_list('BitMapItemData', 'key, value')
command_bit_map_format_type = named_list('CommandBitMapFormat', 'ack_cmd_code, sequence, producer')
setting_response_bit_map_format_type = named_list('SettingResponseBitMapFormat', 'error_code, producer')

cmd_bit_format = command_bit_map_format_type(ack_cmd_code=bit_map_item_type(8, {0: 'Rest',
                                                                                1: 'Set',
                                                                                0x10: 'Idle',
                                                                                0x11: 'Receive',
                                                                                0x12: 'Completed',
                                                                                0x13: 'Locked',
                                                                                0x14: 'Refused'}),
                                             sequence=bit_map_item_type(16, None),
                                             producer=bit_map_item_type(8, {0: 'UC',
                                                                            1: 'SLC_UPS',
                                                                            2: 'SLC_NMC',
                                                                            3: 'HMI',
                                                                            4: 'TUNER'}))

setting_response_bit_map_format = setting_response_bit_map_format_type(error_code=bit_map_item_type(16, {0: 'OK'}),
                                                                       producer=bit_map_item_type(16, {0: 'UC',
                                                                                                       1: 'SLC_UPS',
                                                                                                       2: 'SLC_NMC',
                                                                                                       3: 'HMI',
                                                                                                       4: 'TUNER'}))


def bit_map_parser(value, bit_map_format):
    val_tmp = []
    for bit_field in bit_map_format.fields:
        bit_wide = getattr(bit_map_format, bit_field).bit_wide
        value_dict = getattr(bit_map_format, bit_field).value_dict
        _key = value & ((1 << bit_wide) - 1)
        if value_dict is None:
            _value = None
            pass
        else:
            if _key in value_dict:
                _value = value_dict[_key]
            else:
                _value = None
        val_tmp.append(bit_map_item_Data_type(key=_key, value=_value))
        value >>= bit_wide
    # print(val_tmp)
    return type(bit_map_format)(*val_tmp)
    pass


if __name__ == '__main__':
    pass
