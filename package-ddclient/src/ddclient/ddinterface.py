import json
from ctypes import *
from collections import OrderedDict
from namedlist import namedlist as named_list
try:
    from .dditem import data_dictionary_item_type
    from .valuetype import standard_value_attribute_dictionary, get_value_type_standard_template, ValueType
except SystemError:
    from dditem import data_dictionary_item_type
    from valuetype import standard_value_attribute_dictionary, get_value_type_standard_template, ValueType

enum_item_attribute_type = named_list('EnumItemAttributeType', 'value, comment')

basic_type_name_map = {
    'bool': 'Bool',
    'float': 'Float',

    'int8_t': 'Int8',
    'int16_t': 'Int16',
    'int32_t': 'Int32',
    'uint8_t': 'UInt8',
    'uint16_t': 'UInt16',
    'uint32_t': 'UInt32',

    'BOOL': 'Bool',
    '8BS': 'Int8',
    '8BUS': 'UInt8',
    '16BS': 'Int16',
    '16BUS': 'UInt16',
    '32BS': 'Int32',
    '32BUS': 'UInt32',
    '32BFL': 'Float',
}

special_basic_type_name_map = {
    'char': 'Char',  # Only to be used to identify if the value is string
}

special_type_name_map = {
    'STRING': 'StringType',
    'BINARY_BLOC': 'ArrayType'
}

datagram_type_name_map = {
    'COMMAND': 'Command',
    'SETTING': 'Setting',
    'STATUS': 'Status',
    'GENERAL': 'General',
    'MEASURE': 'Measure'
}


def json_object_pairs_hook(list_data):
    return OrderedDict(list_data)
    pass


class DataDictionaryInterfaceV0:
    def __init__(self):
        pass

    @staticmethod
    def convert(str_num, to_type=None):
        num = None
        if to_type is not None:
            if to_type in getattr(ValueType, '_basic_types'):
                c_type = standard_value_attribute_dictionary[to_type].special_data
                if to_type != 'Float':
                    if str_num.isdigit():
                        try:
                            num = int(str_num, base=10)
                            num = c_type(num).value
                        except ValueError:
                            pass
                    else:
                        str_num = str_num.upper()
                        if str_num.find('X') == 1:
                            try:
                                num = int(str_num, base=16)
                                num = c_type(num).value
                            except ValueError:
                                pass
                        else:
                            try:
                                num = int(float(str_num))
                                num = c_type(num).value
                                print('WARNING:', 'Input value({}) and value type({}) are not match'.format(
                                    str_num,
                                    to_type))
                            except ValueError:
                                pass
                            pass
                        pass
                else:
                    try:
                        num = float(str_num)
                        num = c_type(num).value
                    except ValueError:
                        pass
                    pass
                pass
            else:
                pass
        else:
            if str_num.isdigit():
                num = int(str_num, base=10)
            else:
                str_num = str_num.upper()
                if str_num.find('.') >= 0:
                    try:
                        num = float(str_num)
                    except ValueError:
                        pass
                if str_num.find('X') == 1:
                    try:
                        num = int(str_num, base=16)
                    except ValueError:
                        pass
            pass
        return num
        pass

    @staticmethod
    def parse_structure_special_data(data_dictionary_item_source):
        try:
            structure_format = json.loads(data_dictionary_item_source.ChoiceList[0],
                                          object_pairs_hook=json_object_pairs_hook)
            if 'UniversalChoiceList' in structure_format:
                _name = structure_format['UniversalChoiceList']
                if _name in structure_format:
                    structure_format = structure_format[_name]
                else:
                    print('ERROR:', 'Structure format not be defined')
                    return None
            else:
                _name = 'Default'
            ret_dict = OrderedDict()

            for (key, data) in structure_format.items():
                if type(data) is list:
                    try:
                        try:
                            _basic_type = special_basic_type_name_map[data[0]]
                        except KeyError:
                            _basic_type = basic_type_name_map[data[0]]
                            item = None
                        try:
                            if isinstance(data[1], int):
                                if _basic_type == 'Char':
                                    item = get_value_type_standard_template('String')
                                    item.size = data[1]
                                    item.array_count = data[1]
                                elif _basic_type in getattr(ValueType, '_basic_types'):
                                    _sub_type = standard_value_attribute_dictionary[_basic_type]
                                    item = ValueType(system_tag='ArrayType',
                                                     basic_type=_basic_type,
                                                     size=data[1] * _sub_type.size,
                                                     array_count=data[1],
                                                     special_data=_sub_type)
                                else:
                                    print('ERROR:', '{} is not supported in structure'.format(data[0]))
                                    return None
                                    pass
                                item.comment = data[2]
                            elif isinstance(data[1], str):
                                item = get_value_type_standard_template(_basic_type)
                                item.comment = data[1]
                            else:
                                item = standard_value_attribute_dictionary[_basic_type]
                                pass
                        except IndexError:
                            if item is None:
                                item = standard_value_attribute_dictionary[_basic_type]
                            pass

                    except KeyError:
                        print('ERROR:', 'Structure can only support basic type')
                        return None
                    pass
                elif isinstance(data, str):
                    try:
                        _basic_type = basic_type_name_map[data]
                        item = standard_value_attribute_dictionary[_basic_type]
                    except KeyError:
                        print('ERROR:', 'Structure can only support basic type')
                        return None
                else:
                    print('ERROR:', 'Parse structure failed with bad item', key, data)
                    return None
                    pass
                ret_dict[key] = item
        except ValueError:
            return None
        return _name, ret_dict

    @staticmethod
    def parse_enum_special_data(data_dictionary_item_source):
        try:
            structure_format = json.loads(data_dictionary_item_source.ChoiceList[0],
                                          object_pairs_hook=json_object_pairs_hook)
            if 'UniversalChoiceList' in structure_format:
                _name = structure_format['UniversalChoiceList']
                if _name in structure_format:
                    structure_format = structure_format[_name]
                else:
                    print('ERROR:', 'Enum choice list not be defined')
                    return None
            else:
                _name = 'Default'

            ret_dict = OrderedDict()
            for (key, data) in structure_format.items():
                item = enum_item_attribute_type(0, None)
                if isinstance(data, list):
                    try:
                        if not isinstance(data[0], int):
                            print('ERROR:', 'Enum value can only be UInt32')
                            return None
                        item.value = c_uint32(data[0]).value
                        item.comment = str(data[1])
                    except IndexError:
                        pass
                    pass
                elif isinstance(data, int):
                    item.value = c_uint32(data).value
                else:
                    print('ERROR:', 'Parse enum failed with bad item', key, data)
                    return None
                    pass
                ret_dict[key] = item
        except ValueError:
            return None
        return _name, ret_dict

    def parse_basic_info(self, data_dictionary_item, data_dictionary_item_source):
        data_dictionary_item.root_system = data_dictionary_item_source.RootSystem[0]
        data_dictionary_item.sub_system = data_dictionary_item_source.SubSystem[0]
        data_dictionary_item.data_path = data_dictionary_item_source.DataPath[0]
        data_dictionary_item.name = data_dictionary_item_source.Name[0]
        data_dictionary_item.description = data_dictionary_item_source.Description[0]

        if data_dictionary_item_source.Type[0] in datagram_type_name_map:
            data_dictionary_item.type = datagram_type_name_map[data_dictionary_item_source.Type[0]]
        else:
            print('ERROR:', 'Can not parse the basic info with the type', data_dictionary_item_source.Type[0])
            return False

        try:
            _basic_type = basic_type_name_map[data_dictionary_item_source.Format[0]]
            data_dictionary_item.value_type = standard_value_attribute_dictionary[_basic_type]
        except KeyError:
            pass

        _max_size = self.convert(data_dictionary_item_source.MaxSize[0], 'UInt32')
        if _max_size is None:
            print('ERROR:', 'Can\'t parse the max size ', data_dictionary_item_source.MaxSize[0])
            return False

        if data_dictionary_item.type == 'Command':
            if data_dictionary_item.value_type is None:
                print('ERROR:', 'Command type parse value type failed')
                return False
            if data_dictionary_item.value_type.basic_type != 'UInt32':
                print('ERROR:', 'Command type must be UInt32, but not', data_dictionary_item.value_type.basic_type)
                return False
            else:
                if _max_size != 1:
                    print('ERROR:', 'Command type datagram\'s max size must be 1 but not',
                          _max_size)
                    return False
                pass
        elif data_dictionary_item.type == 'Status':
            if data_dictionary_item.value_type is None:
                print('ERROR:', 'Status type parse value type failed')
                return False

            if _max_size != 1:
                print('ERROR:', 'Status type datagram\'s max size must be 1 but not', _max_size)
                return False

            if data_dictionary_item.value_type.basic_type != 'UInt32':
                print('WARNING:', 'Status type shall be UInt32, but not', data_dictionary_item.value_type.basic_type,
                      'so automatically set it as UInt32')

            _enum_define_data = self.parse_enum_special_data(data_dictionary_item_source)
            if _enum_define_data is None:
                print('ERROR:', 'Enum type must have the choice list')
                return False

            data_dictionary_item.value_type = ValueType(system_tag='EnumType',
                                                        basic_type='UInt32',
                                                        size=4,
                                                        type_name=_enum_define_data[0])
            data_dictionary_item.value_type.special_data = _enum_define_data[1]

        elif data_dictionary_item.type == 'Measure':
            if data_dictionary_item.value_type.basic_type != 'Float':
                print('ERROR:', 'Measure type must be Float, but not', data_dictionary_item.value_type.basic_type)
                return False
            else:
                if _max_size > 3:
                    print('ERROR:', 'Enum type datagram\'s max size must be less then 3 but it is',
                          _max_size)
                    return False
                elif _max_size > 1:
                    _sub_type = data_dictionary_item.value_type
                    data_dictionary_item.value_type = ValueType(system_tag='ArrayType',
                                                                basic_type=_sub_type.basic_type,
                                                                size=_max_size * _sub_type.size,
                                                                array_count=_max_size,
                                                                special_data=_sub_type)
                else:
                    pass
                pass
            pass
        else:
            if data_dictionary_item.value_type is None:
                if data_dictionary_item_source.Format[0] in special_type_name_map:
                    _system_tag = special_type_name_map[data_dictionary_item_source.Format[0]]
                    if _system_tag == 'StringType':
                        data_dictionary_item.value_type = get_value_type_standard_template('String')
                        data_dictionary_item.value_type.size = _max_size
                        pass
                    elif _system_tag == 'ArrayType':
                        _structure_define_data = self.parse_structure_special_data(data_dictionary_item_source)
                        if _structure_define_data is not None:
                            data_dictionary_item.value_type = ValueType(system_tag='StructureType',
                                                                        basic_type=None,
                                                                        size=_max_size,
                                                                        type_name=_structure_define_data[0],
                                                                        special_data=_structure_define_data[1])
                            pass
                        else:
                            data_dictionary_item.value_type = ValueType(
                                system_tag='ArrayType',
                                basic_type='UInt8',
                                size=_max_size,
                                array_count=_max_size,
                                special_data=standard_value_attribute_dictionary['UInt8'])
                            pass
                        pass
                    else:
                        pass
                    pass
                else:
                    print('ERROR:', 'Can not parse the basic info with the format',
                          data_dictionary_item_source.Format[0])
                    return False
                pass
            else:
                _enum_define_data = self.parse_enum_special_data(data_dictionary_item_source)
                if _enum_define_data is None:
                    if _max_size > 1:
                        _sub_type = data_dictionary_item.value_type
                        data_dictionary_item.value_type = ValueType(
                            system_tag='ArrayType',
                            basic_type=_sub_type.basic_type,
                            size=_max_size * _sub_type.size,
                            array_count=_max_size,
                            special_data=standard_value_attribute_dictionary[_sub_type.basic_type])
                    pass
                else:
                    if data_dictionary_item.value_type.basic_type != 'UInt32':
                        print('WARNING:', 'Enum type shall be UInt32 but not',
                              data_dictionary_item.value_type.basic_type,
                              'so automatically set it as UInt32')

                    data_dictionary_item.value_type = ValueType(system_tag='EnumType',
                                                                basic_type='UInt32',
                                                                size=4,
                                                                type_name=_enum_define_data[0])
                    data_dictionary_item.value_type.special_data = _enum_define_data[1]
                    pass
                pass
        pass

    def parse_default_value(self, data_dictionary_item, data_dictionary_item_source):
        default_text = data_dictionary_item_source.Default[0]
        if (data_dictionary_item.value_type.system_tag == 'BasicType') or\
                (data_dictionary_item.value_type.system_tag == 'EnumType'):
            data_dictionary_item.default = self.convert(default_text, data_dictionary_item.value_type.basic_type)
            return True
            pass
        elif data_dictionary_item.value_type.system_tag == 'ArrayType':
            if data_dictionary_item.type == 'Measure':
                tmp_value = self.convert(default_text, data_dictionary_item.value_type.basic_type)
                if tmp_value is not None:
                    data_dictionary_item.default = [tmp_value
                                                    for i in range(data_dictionary_item.value_type.array_count)]
            return True
            pass
        elif data_dictionary_item.value_type.system_tag == 'StructureType':
            try:
                default_value_dict = json.loads(default_text)
            except ValueError:
                return True
            default_value = []
            for (key, data) in data_dictionary_item.value_type.special_data.items():
                if data.system_tag == 'BasicType':
                    c_type = data.special_data
                    if key in default_value_dict:
                        try:
                            val = c_type(default_value_dict[key]).value
                        except TypeError as exception:
                            val = c_type(0).value
                            print('WARNING:', 'Item', key, data, 'value is parsed failed,',
                                  exception, 'so automatically set it as', val)
                            pass
                        pass
                    else:
                        val = c_type(0).value
                        print('WARNING:', 'Item', key, data,
                              'not defines the default value, so automatically set it as', val)
                        pass
                    default_value.append(val)
                    pass
                else:
                    print('ERROR:', 'Structure can only support basic type but not', data.system_tag)
                    return False
                    pass
                pass
            if default_value:
                data_dictionary_item.default = default_value
            return True
        elif data_dictionary_item.value_type.system_tag == 'StringType':
            data_dictionary_item.default = default_text
        else:
            print('ERROR:', 'Can not support the system tag', data_dictionary_item.value_type.system_tag)
            return False
            pass
        pass

    def parse_range_info(self, data_dictionary_item, data_dictionary_item_source):
        if (data_dictionary_item.value_type.system_tag == 'BasicType') or\
                (data_dictionary_item.value_type.system_tag == 'EnumType'):
            data_dictionary_item.min = self.convert(data_dictionary_item_source.Min[0],
                                                    data_dictionary_item.value_type.basic_type)
            data_dictionary_item.max = self.convert(data_dictionary_item_source.Max[0],
                                                    data_dictionary_item.value_type.basic_type)

            if data_dictionary_item.max is None:
                try:
                    choice_point_dict = json.loads(data_dictionary_item_source.Max[0])
                except ValueError:
                    return True
                selectable_point = []
                for (key, data) in choice_point_dict.items():
                    if isinstance(data, list):
                        data = data[0]
                    if isinstance(data, int):
                        data = c_uint32(data).value
                        if key in data_dictionary_item.value_type.special_data:
                            if data == data_dictionary_item.value_type.special_data[key].value:
                                selectable_point.append(data)
                            else:
                                print('WARNING:', 'Item', key, ':', data, 'and enum defined value',
                                      data_dictionary_item.value_type.special_data[key].value, 'mismatch')
                        else:
                            print('WARNING:', 'Item', key, ':', data, 'is not defined in the enum')
                        pass
                    else:
                        print('ERROR:', 'Enum type must be UInt32')
                        return False
                    pass
                if selectable_point:
                    selectable_point.sort()
                    data_dictionary_item.selectable_point = selectable_point
                return True
            pass
        elif data_dictionary_item.value_type.system_tag == 'ArrayType':
            if data_dictionary_item.type == 'Measure':
                _min = self.convert(data_dictionary_item_source.Min[0], data_dictionary_item.value_type.basic_type)
                _max = self.convert(data_dictionary_item_source.Max[0], data_dictionary_item.value_type.basic_type)
                if _min is not None:
                    data_dictionary_item.min = [_min for i in range(data_dictionary_item.value_type.array_count)]
                if _max is not None:
                    data_dictionary_item.max = [_max for i in range(data_dictionary_item.value_type.array_count)]
            return True
        else:
            return True
        pass

    @staticmethod
    def parse_is_alarm(data_dictionary_item, data_dictionary_item_source):
        tmp_str = data_dictionary_item_source.IsAlarm[0].upper()
        if tmp_str == "NO":
            data_dictionary_item.is_alarm = False
            return True
        elif tmp_str == "YES":
            data_dictionary_item.is_alarm = True
            return True
        else:
            data_dictionary_item.is_alarm = False
            print('WAINING:', 'Alarm value info [' + tmp_str + '] is error, so automatically set it as',
                  data_dictionary_item.is_alarm)
            return True
        pass

    @staticmethod
    def parse_is_evt_log(data_dictionary_item, data_dictionary_item_source):
        tmp_str = data_dictionary_item_source.IsEvtLog[0].upper()
        if tmp_str == "NO":
            data_dictionary_item.is_event_log = False
            return True
        elif tmp_str == "YES":
            data_dictionary_item.is_event_log = True
            return True
        else:
            data_dictionary_item.is_event_log = False
            print('WAINING:', 'Event log value info [' + tmp_str + '] is error, so automatically set it as',
                  data_dictionary_item.is_event_log)
            return True
        pass

    @staticmethod
    def parse_producer(data_dictionary_item, data_dictionary_item_source):
        data_dictionary_item.producer = []
        for item in getattr(data_dictionary_item_source.Producer, '_fields'):
            val = getattr(data_dictionary_item_source.Producer, item)[0].upper()
            if val == 'YES':
                data_dictionary_item.producer.append(item)
            pass
        if not data_dictionary_item.producer:
            print('WARNING:', 'Can\'t get any producer', data_dictionary_item_source.Producer)
        return True

    @staticmethod
    def parse_consumer(data_dictionary_item, data_dictionary_item_source):
        data_dictionary_item.consumer = []
        data_dictionary_item.no_setting_req_consumer = []
        for item in getattr(data_dictionary_item_source.Consumer, '_fields'):
            val = getattr(data_dictionary_item_source.Consumer, item)[0].upper()
            if val == 'YES':
                data_dictionary_item.consumer.append(item)
            elif val == 'RO':
                data_dictionary_item.consumer.append(item)
                data_dictionary_item.no_setting_req_consumer.append(item)
            pass
        if not data_dictionary_item.consumer:
            print('WARNING:', 'Can\'t get any consumer', data_dictionary_item_source.Consumer)
        return True

    def get_data_dictionary_item(self, data_dictionary_item_source):
        data_dictionary_item =\
            data_dictionary_item_type(*[None for i in range(len(getattr(data_dictionary_item_type, '_fields')))])
        if self.parse_basic_info(data_dictionary_item, data_dictionary_item_source) is False:
            return None
        if self.parse_default_value(data_dictionary_item, data_dictionary_item_source) is False:
            return None
        if self.parse_range_info(data_dictionary_item, data_dictionary_item_source) is False:
            return None
        data_dictionary_item.scale_unit = data_dictionary_item_source.ScaleUnit[0]
        data_dictionary_item.precision = self.convert(data_dictionary_item_source.Precision[0], 'UInt32')
        if self.parse_is_alarm(data_dictionary_item, data_dictionary_item_source) is False:
            return None
        if self.parse_is_evt_log(data_dictionary_item, data_dictionary_item_source) is False:
            return None
        data_dictionary_item.cmd_time_out = self.convert(data_dictionary_item_source.CmdTimeOut[0], 'UInt32')
        if self.parse_producer(data_dictionary_item, data_dictionary_item_source) is False:
            return None
        if self.parse_consumer(data_dictionary_item, data_dictionary_item_source) is False:
            return None
        data_dictionary_item.hash_id = self.convert(data_dictionary_item_source.HashID[0], 'UInt32')
        return data_dictionary_item
        pass
    pass

data_dictionary_interface = (
    DataDictionaryInterfaceV0(),
)

if __name__ == '__main__':
    pass
