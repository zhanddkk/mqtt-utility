from namedlist import namedlist as _type_creator
from collections import OrderedDict, namedtuple

bit_attribute_type = _type_creator('BitAttribute', 'wide, names')

_cmd_code_names = {
    'Rest': 0,
    'Set': 1,
}

_cmd_ack_code_names = {
    'Idle': 0x10,
    'Received': 0x11,
    'Completed': 0x12,
    'Locked': 0x13,
    'Refused': 0x14
}

_producer_names = {
    'UC': 0,
    'SLC_UPS': 1,
    'SLC_NMC': 2,
    'HMI': 3,
    'TUNER': 4
}

command_bit_map = OrderedDict(
    (
        ('cmd_code', bit_attribute_type(wide=8, names=_cmd_code_names)),
        ('sequence', bit_attribute_type(wide=16, names=None)),
        ('producer', bit_attribute_type(wide=8, names=_producer_names)),
    )
)

command_response_bit_map = OrderedDict(
    (
        ('ack_code', bit_attribute_type(wide=8, names=_cmd_ack_code_names)),
        ('sequence', bit_attribute_type(wide=16, names=None)),
        ('producer', bit_attribute_type(wide=8, names=_producer_names)),
    )
)

setting_response_bit_map = OrderedDict(
    (
        ('error_code', bit_attribute_type(wide=16, names={'OK': 0})),
        ('producer', bit_attribute_type(wide=16, names=_producer_names)),
    )
)


class BitMapParser:
    bit_map_type = _type_creator('BitMapType', 'name, value, bit_fields, wide')
    bit_fields_type = namedtuple('BitFields', 'start, end')

    def __init__(self, bit_map, type_name='BitMapValueType'):
        self.__bit_map = bit_map
        self.__output_value_type = _type_creator(type_name, bit_map.keys())

        attribute = dict()

        _start = 0
        _end = 0
        for _key, _data in self.__bit_map.items():
            _end += _data.wide
            attribute[_key] = self.bit_map_type(name=None,
                                                value=None,
                                                bit_fields=self.bit_fields_type(_start, _end - 1),
                                                wide=_data.wide)
            _start = _end

        self.__output_value = self.__output_value_type(**attribute)
        pass

    @staticmethod
    def __get_name(names, value):
        try:
            for _key, _data in names.items():
                if _data == value:
                    return _key
        except AttributeError:
            pass
        return None

    @property
    def value(self):
        _value = 0
        for _bit in self.__output_value:
            _bit_value = _bit.value & ((1 << _bit.wide) - 1) if isinstance(_bit.value, int) else 0
            _bit_start = _bit.bit_fields.start
            _value |= _bit_value << _bit_start
            pass
        return _value
        pass

    def decode(self, value):
        if not isinstance(value, int):
            print('ERROR:', 'The input value must be int type')
            return None

        if self.__bit_map:
            for _key, _data in self.__bit_map.items():
                names = _data.names
                _bit = getattr(self.__output_value, _key)
                _bit.value = value & ((1 << _data.wide) - 1)
                _bit.name = self.__get_name(names, _bit.value)
                value >>= _data.wide
        return self.__output_value
        pass

    def encode(self, *args, **kwargs):
        _index = 0
        for field_name in getattr(self.__output_value, '_fields'):
            _bit = getattr(self.__output_value, field_name)
            try:
                _value = args[_index]
                if field_name in kwargs:
                    raise TypeError('{} got multiple values for argument \'{}\''.format('encode()', field_name))

                _bit.value = _value
                _index += 1
            except IndexError:
                try:
                    _bit.value = kwargs[field_name]
                except KeyError:
                    _bit.value = None
                    pass
                pass
            _bit.name = self.__get_name(self.__bit_map[field_name].names, _bit.value)
        return self.value
        pass

    pass


def demo():
    a = BitMapParser(command_bit_map)
    a.decode(0x02000500)
    print(a.decode(0x02000500))
    a.encode(1, 2, 3)
    print('0x{value:>08X}'.format(value=a.value))
    a.encode(cmd_code=4, sequence=5, producer=6)
    print('0x{value:>08X}'.format(value=a.value))
    a.encode(0, sequence=8, producer=9)
    print('0x{value:>08X}'.format(value=a.value))
    a.encode()
    print('0x{value:>08X}'.format(value=a.value))
    pass

if __name__ == '__main__':
    demo()
    pass


# The legacy of the interface
bit_map_item_type = _type_creator('BitMapItem', 'bit_wide, value_dict')
bit_map_item_Data_type = _type_creator('BitMapItemData', 'key, value')
command_bit_map_format_type = _type_creator('CommandBitMapFormat', 'ack_cmd_code, sequence, producer')
setting_response_bit_map_format_type = _type_creator('SettingResponseBitMapFormat', 'error_code, producer')

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
    for bit_field in getattr(bit_map_format, '_fields'):
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
