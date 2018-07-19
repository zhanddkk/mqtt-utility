# Internal class
class DisplayItemLine(object):
    def __init__(self, deep, value):
        self.__tree_flags = {}
        self.__deep = deep
        self.__value = value
        pass

    def add_tree_flag(self, pos, value):
        self.__tree_flags[pos] = value
        pass

    def __repr__(self):
        _ret = ''
        _last_end = 0
        for _pos, _value in sorted(self.__tree_flags.items(), key=lambda _d: _d[0]):
            _ret += '{value:>{space_len}s}'.format(value=_value, space_len=_pos - _last_end + len(_value))
            _last_end = _pos
        _value = self.__value
        _ret += '{value:>{space_len}s}'.format(value=_value,
                                               space_len=self.__deep * 2 - _last_end + len(_value))
        return _ret
        pass

    def __str__(self):
        return self.__repr__()

    @property
    def deep(self):
        return self.__deep
    pass


# API
class ValuePrinter:
    def __init__(self):
        self.print = self.__print
        pass

    @staticmethod
    def __print_basic_type_value(value, name, deep):
        if isinstance(value, int):
            _value_text = '{name:<10s}: 0x{value:X}({value})'.format(name=name, value=value)
            pass
        else:
            _value_text = '{name:<10s}: {value}'.format(name=name, value=value)
        _item = DisplayItemLine(deep=deep, value=_value_text)
        return _item
        pass

    @staticmethod
    def __print_enum_type_value(value, name, value_type, deep):
        for _key, _data in value_type.special_data.items():
            if _data.value == value:
                _value_text = '{name:<10s}: 0x{value:X}[{key_name}({value})]'.format(name=name,
                                                                                     value=_data.value,
                                                                                     key_name=_key)
                _item = DisplayItemLine(deep=deep, value=_value_text)
                return _item
        # No enum name
        _value_text = '{name:<10s}: {value}'.format(name=name, value=value)
        _item = DisplayItemLine(deep=deep, value=_value_text)
        return _item
        pass

    @staticmethod
    def __print_string_type_value(value, name, deep):
        _value_text = '{name:<10s}: {value}'.format(name=name, value=value)
        _item = DisplayItemLine(deep=deep, value=_value_text)
        return _item
        pass

    @staticmethod
    def __print_bitmap_type_value(value, name, value_type, deep):
        if isinstance(value, int):
            _value_text = '{name:<10s}: 0x{value:>08X}'.format(name=name, value=value)
        else:
            _value_text = '{name:<10s}: {value}({type})[Invalid Type]'.format(name=name,
                                                                              value=value,
                                                                              type=type(value).__name__)
        _item = DisplayItemLine(deep=deep, value=_value_text)
        if isinstance(value, int):
            _items = [_item]
            _start = 0
            _end = 0
            for _key, _data in value_type.special_data.items():
                _end += _data.wide
                _bit_value = value & ((1 << _data.wide) - 1)
                _key_name_text = None
                if _data.names:
                    for _key_name, _key_value in _data.names.items():
                        if _key_value == _bit_value:
                            _key_name_text = '{name}'.format(name=_key_name)
                if _key_name_text:
                    _sub_value_text = '{name:<10s}({bit_start}-{bit_end}): {value}({key_name})'\
                        .format(name=_key,
                                bit_start=_start,
                                bit_end=_end - 1,
                                value=_bit_value,
                                key_name=_key_name_text)
                else:
                    _sub_value_text = '{name:<10s}({bit_start}-{bit_end}): {value}'.format(name=_key,
                                                                                           bit_start=_start,
                                                                                           bit_end=_end - 1,
                                                                                           value=_bit_value)
                _sub_item = DisplayItemLine(deep=deep + 1, value=_sub_value_text)
                _items.append(_sub_item)
                value >>= _data.wide
                _start = _end
            _ret = _items
            pass
        else:
            _ret = _item
            pass
        return _ret
        pass

    def __print_array_type_value(self, value, name, value_type, deep):
        _sub_value_type = value_type.special_data
        if _sub_value_type.system_tag == 'BasicType':
            _value_text = '{name:<10s}: {value}'.format(name=name, value=value)
            _item = DisplayItemLine(deep=deep, value=_value_text)
            return _item
        else:
            _value_text = '{name}'.format(name=name)
            _item = DisplayItemLine(deep=deep, value=_value_text)
            _items = [_item]
            for i in range(value_type.array_count):
                try:
                    _value = value[i]
                except IndexError:
                    break
                except TypeError:
                    _value = None
                _sub_item = self.__print_value(value=_value,
                                               name='[{index}]'.format(index=i),
                                               value_type=_sub_value_type,
                                               deep=deep + 1)
                if _sub_item:
                    if isinstance(_sub_item, list):
                        _items += _sub_item
                    else:
                        _items.append(_sub_item)
            pass
            return _items
        pass

    def __print_structure_type_value(self, value, name, value_type, deep):
        i = 0
        _value_text = '{name}'.format(name=name)
        _item = DisplayItemLine(deep=deep, value=_value_text)
        _items = [_item]
        for _key, _data in value_type.special_data.items():
            try:
                _value = value[i]
            except IndexError:
                _value = None
            except TypeError:
                _value = None
            _sub_item = self.__print_value(name='{name}'.format(name=_key),
                                           value=_value,
                                           value_type=_data,
                                           deep=deep + 1)
            if _sub_item:
                if isinstance(_sub_item, list):
                    _items += _sub_item
                else:
                    _items.append(_sub_item)
            i += 1
            pass
        return _items
        pass

    def __print_value(self, value, name, value_type, deep):
        _ret = None
        if value_type.system_tag == 'BasicType':
            _ret = self.__print_basic_type_value(value=value, name=name, deep=deep)
            pass
        elif value_type.system_tag == 'EnumType':
            _ret = self.__print_enum_type_value(value=value, name=name, value_type=value_type, deep=deep)
            pass
        elif value_type.system_tag == 'StringType':
            _ret = self.__print_string_type_value(value=value, name=name, deep=deep)
            pass
        elif value_type.system_tag == 'ArrayType':
            _ret = self.__print_array_type_value(value=value, name=name, value_type=value_type, deep=deep)
            pass
        elif value_type.system_tag == 'BitmapType':
            _ret = self.__print_bitmap_type_value(value=value, name=name, value_type=value_type, deep=deep)
            pass
        elif value_type.system_tag == 'StructureType':
            _ret = self.__print_structure_type_value(value=value, name=name, value_type=value_type, deep=deep)
            pass
        else:
            pass
        return _ret
        pass

    def print_value(self, name, value, value_type, deep=0):
        if value_type is None:
            _item_line = DisplayItemLine(deep=deep, value='{}: {}'.format(name, value))
            self.print(str(_item_line))
            pass
        else:
            _ret_value = self.__print_value(value=value, name=name, value_type=value_type, deep=deep)
            if isinstance(_ret_value, list):
                for _item in _ret_value:
                    self.print(str(_item))
                    pass
            else:
                self.print(str(_ret_value))
        pass

    @staticmethod
    def __print(text):
        print(text)
        pass

    pass

if __name__ == '__main__':
    pass
