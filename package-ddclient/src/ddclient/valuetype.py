try:
    from collections import OrderedDict as _OrderedDict
except SystemError:
    _OrderedDict = None
from ctypes import *


class ValueType(object):

    _fields = ('system_tag', 'basic_type', 'array_count', 'size', 'type_name', 'special_data', 'comment')
    _type_names_dict = {
        'BasicType': 'Basic',
        'EnumType': 'Enum',
        'ArrayType': 'Array',
        'StructureType': 'Struct',
        'StringType': 'String',
        'BitmapType': 'Bitmap'
    }
    _system_tags = tuple(_type_names_dict.keys())
    _basic_types = ('Bool', 'Int8', 'UInt8', 'Int16', 'UInt16', 'Int32', 'UInt32', 'Float', 'UInt64')

    @property
    def fields(self):
        return self._fields

    @property
    def system_tags(self):
        return self._system_tags

    @property
    def basic_types(self):
        return self._basic_types

    @property
    def default_type_names(self):
        return self._type_names_dict.values()

    def __init__(self, system_tag, basic_type, size, type_name='Default', array_count=1, special_data=None, comment=''):
        if isinstance(system_tag, str):
            if system_tag in self._system_tags:
                self.__system_tag = system_tag
            else:
                raise TypeError('{} is not supported by system tag'.format(system_tag))
            pass
        else:
            raise TypeError('system tag must be string type of python')

        if isinstance(basic_type, str):
            if basic_type in self._basic_types:
                self.__basic_type = basic_type
            else:
                raise TypeError('{} is not supported by basic type'.format(basic_type))
            pass
        else:
            if basic_type is None:
                self.__basic_type = None
            else:
                raise TypeError('basic type must be string type of python')

        if isinstance(array_count, int):
            self.__array_count = array_count
        else:
            raise TypeError('array count must be int type of python')

        if isinstance(size, int) or (size is None):
            self.__size = size
        else:
            raise TypeError('size must be int type of python')
        pass
        self.__special_data = special_data
        if isinstance(comment, str):
            self.__comment = comment
        else:
            raise TypeError('comment must be string type of python')
        self.__type_name = type_name
        if isinstance(comment, str):
            self.__type_name = type_name
        else:
            raise TypeError('comment must be string type of python')
        pass

    @property
    def system_tag(self):
        return self.__system_tag

    @system_tag.setter
    def system_tag(self, value):
        if isinstance(value, str):
            if value in self._system_tags:
                self.__system_tag = value
            else:
                raise TypeError('{} is not supported by system tag'.format(value))
            pass
        else:
            raise TypeError('system tag must be string type of python')

    @property
    def basic_type(self):
        return self.__basic_type

    @basic_type.setter
    def basic_type(self, value):
        if isinstance(value, str):
            if value in self._basic_types:
                self.__basic_type = value
            else:
                raise TypeError('{} is not supported by basic type'.format(value))
            pass
        else:
            if value is None:
                self.__basic_type = None
            else:
                raise TypeError('basic type must be string type of python')

    @property
    def array_count(self):
        return self.__array_count

    @array_count.setter
    def array_count(self, value):
        if isinstance(value, int):
            self.__array_count = value
        else:
            raise TypeError('array count must be int type of python')
        pass

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        if isinstance(value, int) or (value is None):
            self.__size = value
        else:
            raise TypeError('size must be int type of python')
        pass

    @property
    def special_data(self):
        return self.__special_data

    @special_data.setter
    def special_data(self, value):
        self.__special_data = value

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, value):
        if isinstance(value, str):
            self.__comment = value
        else:
            raise TypeError('comment must be string type of python')

    @property
    def type_name(self):
        return self.__type_name if self.__type_name != 'Default' else\
            self._type_names_dict[self.__system_tag] if self.__system_tag != 'BasicType' else self.__basic_type

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__,
                                 ', '.join('{0}={1!r}'.format(name, getattr(self, name)) for name in self._fields))
        pass

    def __dict__(self):
        # In 2.6, return a dict.
        # Otherwise, return an OrderedDict
        t = _OrderedDict if _OrderedDict is not None else dict
        return t(zip(self._fields, self))
        pass

    def __iter__(self):
        return (getattr(self, field_name) for field_name in self._fields)

    def __getitem__(self, item):
        if isinstance(item, str):
            try:
                return getattr(self, item)
            except AttributeError:
                raise KeyError('{} is invalid key'.format(item))
        elif isinstance(item, int):
            try:
                return getattr(self, self._fields[item])
            except IndexError:
                raise IndexError('{} is out of the index range({})'.format(item, len(self._fields)))
        else:
            raise KeyError('{}'.format(item))
        pass

    pass


bool_attribute = ValueType(system_tag='BasicType',
                           basic_type='Bool',
                           size=1,
                           special_data=c_bool)

u_int8_attribute = ValueType(system_tag='BasicType',
                             basic_type='UInt8',
                             size=1,
                             special_data=c_uint8)

u_int16_attribute = ValueType(system_tag='BasicType',
                              basic_type='UInt16',
                              size=2,
                              special_data=c_uint16)

u_int32_attribute = ValueType(system_tag='BasicType',
                              basic_type='UInt32',
                              size=4,
                              special_data=c_uint32)

int8_attribute = ValueType(system_tag='BasicType',
                           basic_type='Int8',
                           size=1,
                           special_data=c_int8)

int16_attribute = ValueType(system_tag='BasicType',
                            basic_type='Int16',
                            size=2,
                            special_data=c_int16)

int32_attribute = ValueType(system_tag='BasicType',
                            basic_type='Int32',
                            size=4,
                            special_data=c_int32)

float_attribute = ValueType(system_tag='BasicType',
                            basic_type='Float',
                            size=4,
                            special_data=c_float)

string_attribute = ValueType(system_tag='StringType',
                             basic_type=None,
                             size=None,
                             special_data=None)

u_int64_attribute = ValueType(system_tag='BasicType',
                              basic_type='UInt64',
                              size=8,
                              special_data=c_uint64)

standard_value_attribute_dictionary = {
    'Bool': bool_attribute,
    'Int8': int8_attribute,
    'Int16': int16_attribute,
    'Int32': int32_attribute,
    'UInt8': u_int8_attribute,
    'UInt16': u_int16_attribute,
    'UInt32': u_int32_attribute,
    'Float': float_attribute,
    'String': string_attribute,
    'UInt64': u_int64_attribute
}


def get_value_type_standard_template(type_name):
    # Return a new object
    try:
        return ValueType(**standard_value_attribute_dictionary[type_name].__dict__())
    except KeyError:
        raise ValueError('{} is invalid type name'.format(type_name))
    pass


def demo():
    a = get_value_type_standard_template('UInt8')
    a.comment = 'test'
    b = get_value_type_standard_template('UInt8')
    print(a)
    print(b)
    print(a['system_tag'])
    print(a[1])
    pass


if __name__ == '__main__':
    demo()
    pass
