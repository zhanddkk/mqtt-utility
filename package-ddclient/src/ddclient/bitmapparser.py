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

    @property
    def value_as_bitmap(self):
        return self.__output_value

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
                    # Keep default if not set
                    # _bit.value = None
                    pass
                pass
            _bit.name = self.__get_name(self.__bit_map[field_name].names, _bit.value)
        return self.value
        pass

    @property
    def bit_names(self):
        return getattr(self.__output_value, '_fields')
        pass

    def __getitem__(self, item):
        if isinstance(item, str):
            try:
                return getattr(self.__output_value, item).value
            except AttributeError:
                raise KeyError('{} is invalid key'.format(item))
            pass
        elif isinstance(item, int):
            try:
                return getattr(self.__output_value, self.bit_names[item]).value
            except IndexError:
                raise IndexError('{} is out of the index range({})'.format(item, len(self.bit_names)))
            pass
        else:
            raise KeyError('{} is invalid key'.format(item))
            pass
        pass

    def __setitem__(self, key, value):
        if isinstance(key, str):
            try:
                if isinstance(value, int):
                    _data = self.__bit_map[key]
                    _bit = getattr(self.__output_value, key)
                    _bit.value = value & ((1 << _data.wide) - 1)
                    _bit.name = self.__get_name(_data.names, _bit.value)
                else:
                    raise ValueError('{} is invalid for bit\'s value, it must be int type'.format(value))
            except AttributeError:
                raise KeyError('{} is invalid key'.format(key))
            pass
        elif isinstance(key, int):
            try:
                _key = self.bit_names[key]
                if isinstance(value, int):
                    _data = self.__bit_map[_key]
                    _bit = getattr(self.__output_value, _key)
                    _bit.value = value & ((1 << _data.wide) - 1)
                    _bit.name = self.__get_name(_data.names, _bit.value)
                else:
                    raise ValueError('{} is invalid for bit\'s value, it must be int type'.format(value))
            except IndexError:
                raise IndexError('{} is out of the index range({})'.format(key, len(self.bit_names)))
            pass
        else:
            raise KeyError('{} is invalid key'.format(key))
            pass
        pass

    def __iter__(self):
        return (item.value for item in self.__output_value)

    def __repr__(self):
        return '0x{0:X}|{1}({2})'.format(
            self.value,
            self.__class__.__name__,
            ', '.join('{0}={1!r}'.format(name, getattr(self.__output_value, name)) for name in self.bit_names))
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
    print(a)
    a['cmd_code'] = 1
    print(a)
    for i in a:
        print(i)
    print(a[2])
    print(a['cmd_code'])
    pass

if __name__ == '__main__':
    demo()
    pass
