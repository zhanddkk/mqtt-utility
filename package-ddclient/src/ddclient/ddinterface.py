import json
from ctypes import *
from collections import OrderedDict
from namedlist import namedlist as named_list
try:
    from .dditem import data_dictionary_item_type
except SystemError:
    from dditem import data_dictionary_item_type

basic_type_attribute_class = named_list('BasicTypeAttribute', 'range, size, type')
udt_type_attribute_class = named_list('UserDefineType', 'name, size, type, content, comment')
structure_type_item_attribute_class = named_list('StructureTypeItemAttribute',
                                                 'system_tag, basic_type, array_count, special_data, comment')
enum_type_item_attribute_class = named_list('EnumTypeItemAttribute', 'value, comment')

basic_type_name_map = {
    'bool': 'Bool',
    'char': 'Char',     # Only to be used to identify if the value is string
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

basic_type_attribute = {
    'Bool': basic_type_attribute_class(range=[0, 1], size=1, type=c_bool),
    'Int8': basic_type_attribute_class(range=[-128, 127], size=1, type=c_int8),
    'Int16': basic_type_attribute_class(range=[-32768, 32767], size=2, type=c_int16),
    'Int32': basic_type_attribute_class(range=[-2147483648, 2147483647], size=4, type=c_int32),
    'UInt8': basic_type_attribute_class(range=[0, 0xff], size=1, type=c_uint8),
    'UInt16': basic_type_attribute_class(range=[0, 0xffff], size=2, type=c_uint16),
    'UInt32': basic_type_attribute_class(range=[0, 0xffffffff], size=4, type=c_uint32),
    'Float': basic_type_attribute_class(range=[3.4E-38, 3.4E38], size=4, type=c_float),
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
            if to_type in basic_type_attribute:
                c_type = basic_type_attribute[to_type].type
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
    def parse_structure_format(data_dictionary_item_source):
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
                _name = 'NO DEFINE'
            ret_dict = OrderedDict()
            for (key, data) in structure_format.items():
                item = structure_type_item_attribute_class('BasicType', None, 1, None, None)
                if type(data) is list:
                    try:
                        item.basic_type = basic_type_name_map[data[0]]
                        # item.comment = data[1]
                        if isinstance(data[1], int):
                            # 'system_tag, basic_type, array_count, special_data, comment'
                            if item.basic_type == 'Char':
                                item.system_tag = 'StringType'
                            else:
                                item.system_tag = 'ArrayType'
                                item.special_data = structure_type_item_attribute_class(
                                    system_tag='BasicType',
                                    basic_type=item.basic_type,
                                    array_count=1,
                                    special_data=None,
                                    comment=None
                                )
                            item.array_count = data[1]
                            item.comment = data[2]
                    except KeyError:
                        print('ERROR:', 'Structure can only support basic type')
                        return None
                    except IndexError:
                        pass
                    pass
                elif type(data) is str:
                    try:
                        item.basic_type = basic_type_name_map[data]
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
        if ret_dict:
            structure = udt_type_attribute_class(name=_name,
                                                 size=None,
                                                 type='Structure',
                                                 content=ret_dict,
                                                 comment='')
            return structure
        else:
            return None

    @staticmethod
    def parse_enum_choice_list(data_dictionary_item_source):
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
                _name = 'NO DEFINE'
            ret_dict = OrderedDict()
            for (key, data) in structure_format.items():
                item = enum_type_item_attribute_class(0, None)
                if type(data) is list:
                    try:
                        if type(data[0]) is not int:
                            print('ERROR:', 'Enum value can only be UInt32')
                            return None
                        item.value = c_uint32(data[0]).value
                        item.comment = str(data[1])
                    except IndexError:
                        pass
                    pass
                elif type(data) is int:
                    item.value = c_uint32(data).value
                else:
                    print('ERROR:', 'Parse enum failed with bad item', key, data)
                    return None
                    pass
                ret_dict[key] = item
        except ValueError:
            return None
        if ret_dict:
            enum = udt_type_attribute_class(name=_name,
                                            size=None,
                                            type='Enum',
                                            content=ret_dict,
                                            comment='')
            return enum
        else:
            return None
        pass

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
            data_dictionary_item.basic_type = basic_type_name_map[data_dictionary_item_source.Format[0]]
            data_dictionary_item.system_tag = 'BasicType'
        except KeyError:
            pass

        data_dictionary_item.max_size = self.convert(data_dictionary_item_source.MaxSize[0], 'UInt32')
        if data_dictionary_item.max_size is None:
            print('ERROR:', 'Can\'t parse the max size ', data_dictionary_item_source.MaxSize[0])
            return False
        if data_dictionary_item.type == 'Command':
            if data_dictionary_item.basic_type != 'UInt32':
                print('ERROR:', 'Command type must be UInt32, but not', data_dictionary_item.basic_type)
                return False
            else:
                if data_dictionary_item.max_size != 1:
                    print('ERROR:', 'Command type datagram\'s max size must be 1 but not',
                          data_dictionary_item.max_size)
                    return False
                data_dictionary_item.array_count = data_dictionary_item.max_size
                pass
        elif data_dictionary_item.type == 'Status':
            '''
            if attribute.basic_type != 'UInt32':
                print('ERROR:', 'Status type must be UInt32, but not', attribute.basic_type)
                return False
            else:
                if attribute.max_size != 1:
                    print('ERROR:', 'Enum type datagram\'s max size must be 1 but not', attribute.max_size)
                    return False
                attribute.array_count = attribute.max_size
                attribute.system_tag = 'EnumType'
                attribute.choice_list = self.parse_enum_choice_list(attribute_text)
                if attribute.choice_list is None:
                    print('ERROR:', 'Enum type must have the choice list')
                    return False
                pass
            '''
            if data_dictionary_item.system_tag != 'BasicType':
                print('ERROR:', 'Status type\'s system tag must be BasicType, but not', data_dictionary_item.system_tag)
                return False
            if data_dictionary_item.basic_type != 'UInt32':
                print('WARNING:', 'Status type shall be UInt32, but not', data_dictionary_item.basic_type,
                      'so automatically set it as UInt32')
                data_dictionary_item.basic_type = 'UInt32'

            if data_dictionary_item.max_size != 1:
                print('ERROR:', 'Status type datagram\'s max size must be 1 but not', data_dictionary_item.max_size)
                return False
            data_dictionary_item.array_count = data_dictionary_item.max_size
            data_dictionary_item.system_tag = 'EnumType'
            data_dictionary_item.choice_list = self.parse_enum_choice_list(data_dictionary_item_source)
            if data_dictionary_item.choice_list is None:
                print('ERROR:', 'Enum type must have the choice list')
                return False
        elif data_dictionary_item.type == 'Measure':
            if data_dictionary_item.basic_type != 'Float':
                print('ERROR:', 'Measure type must be Float, but not', data_dictionary_item.basic_type)
                return False
            else:
                if data_dictionary_item.max_size > 3:
                    print('ERROR:', 'Enum type datagram\'s max size must be less then 3 but it is',
                          data_dictionary_item.max_size)
                    return False
                elif data_dictionary_item.max_size > 1:
                    data_dictionary_item.system_tag = 'ArrayType'
                else:
                    pass
                data_dictionary_item.array_count = data_dictionary_item.max_size
                pass
            pass
        else:
            if data_dictionary_item.basic_type is None:
                if data_dictionary_item_source.Format[0] in special_type_name_map:
                    data_dictionary_item.system_tag = special_type_name_map[data_dictionary_item_source.Format[0]]
                    if data_dictionary_item.system_tag == 'StringType':
                        data_dictionary_item.basic_type = 'Char'
                        data_dictionary_item.array_count = 1
                        pass
                    elif data_dictionary_item.system_tag == 'ArrayType':
                        data_dictionary_item.structure_format = self.parse_structure_format(data_dictionary_item_source)
                        if data_dictionary_item.structure_format is not None:
                            data_dictionary_item.system_tag = 'StructureType'
                            data_dictionary_item.array_count = 1
                            pass
                        else:
                            data_dictionary_item.basic_type = 'UInt8'
                            data_dictionary_item.array_count = data_dictionary_item.max_size
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
                data_dictionary_item.choice_list = self.parse_enum_choice_list(data_dictionary_item_source)
                if data_dictionary_item.choice_list is None:
                    pass
                else:
                    data_dictionary_item.system_tag = 'EnumType'
                    if data_dictionary_item.basic_type != 'UInt32':
                        print('WARNING:', 'Enum type shall be UInt32 but not', data_dictionary_item.basic_type,
                              'so automatically set it as UInt32')
                        data_dictionary_item.basic_type = 'UInt32'
                    pass
                pass
                data_dictionary_item.array_count = data_dictionary_item.max_size
        pass

    def parse_default_value(self, data_dictionary_item, data_dictionary_item_source):
        default_text = data_dictionary_item_source.Default[0]
        if (data_dictionary_item.system_tag == 'BasicType') or (data_dictionary_item.system_tag == 'EnumType'):
            data_dictionary_item.default = self.convert(default_text, data_dictionary_item.basic_type)
            return True
            pass
        elif data_dictionary_item.system_tag == 'ArrayType':
            if data_dictionary_item.type == 'Measure':
                tmp_value = self.convert(default_text, data_dictionary_item.basic_type)
                if tmp_value is not None:
                    data_dictionary_item.default = [tmp_value for i in range(data_dictionary_item.array_count)]
            return True
            pass
        elif data_dictionary_item.system_tag == 'StructureType':
            try:
                default_value_dict = json.loads(default_text)
            except ValueError:
                return True
            default_value = []
            for (key, data) in data_dictionary_item.structure_format.content.items():
                if data.system_tag == 'BasicType':
                    c_type = basic_type_attribute[data.basic_type].type
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
        elif data_dictionary_item.system_tag == 'StringType':
            data_dictionary_item.default = default_text
        else:
            print('ERROR:', 'Can not support the system tag', data_dictionary_item.system_tag)
            return False
            pass
        pass

    def parse_range_info(self, data_dictionary_item, data_dictionary_item_source):
        if (data_dictionary_item.system_tag == 'BasicType') or (data_dictionary_item.system_tag == 'EnumType'):
            data_dictionary_item.min = self.convert(data_dictionary_item_source.Min[0], data_dictionary_item.basic_type)
            data_dictionary_item.max = self.convert(data_dictionary_item_source.Max[0], data_dictionary_item.basic_type)

            if data_dictionary_item.max is None:
                try:
                    choice_point_dict = json.loads(data_dictionary_item_source.Max[0])
                except ValueError:
                    return True
                selectable_point = []
                for (key, data) in choice_point_dict.items():
                    if type(data) is list:
                        data = data[0]
                    if type(data) is int:
                        data = c_uint32(data).value
                        if key in data_dictionary_item.choice_list.content:
                            if data == data_dictionary_item.choice_list.content[key].value:
                                selectable_point.append(data)
                            else:
                                print('WARNING:', 'Item', key, ':', data, 'and enum defined value',
                                      data_dictionary_item.choice_list.content[key].value, 'mismatch')
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
        elif data_dictionary_item.system_tag == 'ArrayType':
            if data_dictionary_item.type == 'Measure':
                _min = self.convert(data_dictionary_item_source.Min[0], data_dictionary_item.basic_type)
                _max = self.convert(data_dictionary_item_source.Max[0], data_dictionary_item.basic_type)
                if _min is not None:
                    data_dictionary_item.min = [_min for i in range(data_dictionary_item.array_count)]
                if _max is not None:
                    data_dictionary_item.max = [_max for i in range(data_dictionary_item.array_count)]
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
