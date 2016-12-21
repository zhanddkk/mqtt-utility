import json
from ctypes import *
from collections import OrderedDict

data_type_name_map = {
    "int8_t": ['Int8', 'Enum'],
    "int16_t": ['Int16', 'Enum'],
    "int32_t": ['Int32', 'Enum'],
    "bool": ['Bool', 'Enum'],
    "uint8_t": ['UInt8', 'Enum'],
    "uint16_t": ['UInt16', 'Enum'],
    "uint32_t": ['UInt32', 'Enum'],
    "BOOL": ['Bool'],
    "8BS": ['Int8', 'Enum'],
    "8BUS": ['UInt8', 'Enum'],
    "16BS": ['Int16', 'Enum'],
    "16BUS": ['UInt16', 'Enum'],
    "32BS": ['Int32', 'Enum'],
    "32BUS": ['UInt32', 'Enum'],
    "32BFL": ['Float'],
    "float": ['Float'],
    "BINARY_BLOC": ['ByteArray', 'Structure'],
    "STRING": ['String']
}

integer_data_type_name = [
    'Int8',
    'Int16',
    'Int32',
    'Bool',
    'UInt8',
    'UInt16',
    'UInt32'
]

decimals_data_type_name = ['Float']

general_data_type = {
    'Int8': {
        'range': [-128, 127],
        'size': 1,
        'type': c_int8
    },
    'Int16': {
        'range': [-32768, 32767],
        'size': 2,
        'type': c_int16
    },
    'Int32': {
        'range': [-2147483648, 2147483647],
        'size': 4,
        'type': c_int32
    },
    'Bool': {
        'range': [0, 1],
        'size': 1,
        'type': c_bool
    },
    'UInt8': {
        'range': [0, 0xff],
        'size': 1,
        'type': c_uint8
    },
    'UInt16': {
        'range': [0, 0xffff],
        'size': 2,
        'type': c_uint16
    },
    'UInt32': {
        'range': [0, 0xffffffff],
        'size': 4,
        'type': c_uint32
    },
    'Float': {
        'range': [3.4E-38, 3.4E38],
        'size': 4,
        'type': c_float
    }
}


def json_object_pairs_hook(list_data):
    return OrderedDict(list_data)
    pass


class DatagramAttribute:
    def __init__(self, info_from_csv):
        self._text_attribute = info_from_csv
        self.__format = 'UInt32'
        self.__choice_list = None
        self.parser_base_info()
        self.__length = self.parser_length()
        self.__default = self.parser_default()
        self.__min = None
        self.__max = None
        self.__selection_limit = None
        self.parser_range()

    @staticmethod
    def convert(str_num, to_type=None):
        num = None
        if to_type is not None:
            if to_type in general_data_type:
                c_type = general_data_type[to_type]['type']
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

    def parser_enum(self, choice_list):
        ret_dict = OrderedDict()
        for (key, data) in choice_list.items():
            item_dat = data[0] if type(data) is list else data
            item_comment = data[1] if (type(data) is list) and (len(data) > 1) else ''
            try:
                item_dat = general_data_type[self.__format]['type'](item_dat).value
                pass
            except TypeError:
                print('ERROR:', 'enum\'s data type error')
                return None
            ret_dict[key] = [item_dat, item_comment]
        return ret_dict

    def parser_structure(self, choice_list):
        ret_dict = OrderedDict()
        for (key, data) in choice_list.items():
            item_dat = data[0] if type(data) is list else data
            item_comment = data[1] if (type(data) is list) and (len(data) > 1) else ''
            if item_dat in data_type_name_map:
                item_dat = data_type_name_map[item_dat][0]
                if item_dat in general_data_type:
                    pass
                else:
                    print('ERROR:', 'structure can only support general data type')
                    return None
            else:
                print('ERROR:', 'structure\'s data type error')
                return None
            ret_dict[key] = [item_dat, item_comment]
        return ret_dict

    def convert_choice_list(self, choice_list):
        if 'UniversalChoiceList' in choice_list:
            choice_list = choice_list[choice_list['UniversalChoiceList']]
        if (self.__format in general_data_type) and (self.__format != 'Float') and (self.__format != 'Bool'):
            return self.parser_enum(choice_list)
            pass
        elif self.__format == 'ByteArray':
            return self.parser_structure(choice_list)
            pass
        else:
            return None
            pass
        pass

    def parser_base_info(self):
        if self._text_attribute.Format[0] in data_type_name_map:
            self.__format = data_type_name_map[self._text_attribute.Format[0]][0]
            try:
                choice_list = json.loads(self._text_attribute.ChoiceList[0],
                                         object_pairs_hook=json_object_pairs_hook)
                self.__choice_list = self.convert_choice_list(choice_list)
                if self.__choice_list is not None:
                    self.__format = data_type_name_map[self._text_attribute.Format[0]][1]
            except ValueError:
                pass
            pass
        else:
            print('ERROR:', 'data format', self._text_attribute.Format[0], 'not be supported')
            pass

    def parser_length(self):
        if self.__format in general_data_type:
            num = self.convert(self._text_attribute.MaxSize[0], 'UInt32')
            return 1 if num is None else num
        else:
            return 1
        pass

    def parser_default(self):
        if self.__format in general_data_type:
            if self.__length > 1:
                def_val = []
                for i in range(self.__length):
                    def_val_tmp = self.convert(self._text_attribute.Default[0], self.__format)
                    if def_val_tmp is None:
                        if self.__format == 'Float':
                            def_val.append(0.0)
                        else:
                            def_val.append(0)
                    else:
                        def_val.append(def_val_tmp)
                pass
            else:
                def_val = self.convert(self._text_attribute.Default[0], self.__format)
                if def_val is None:
                    if self.__format == 'Float':
                        def_val = 0.0
                    else:
                        def_val = 0
            return def_val
            pass
        else:
            if self.__format == 'String':
                return self._text_attribute.Default[0]
            elif self.__format == 'ByteArray':
                # Not define
                return None
            elif self.__format == 'Structure':
                import json
                try:
                    def_val_dic = json.loads(self._text_attribute.Default[0])
                except ValueError:
                    return None

                def_val = []
                for (key, data) in self.__choice_list.items():
                    if data[0] in general_data_type:
                        val = general_data_type[data[0]]['type'](0).value
                    else:
                        val = None

                    if key in def_val_dic:
                        try:
                            tmp_def_val = def_val_dic[key]
                            if type(tmp_def_val) is list:
                                tmp_def_val = tmp_def_val[0]
                            val = general_data_type[data[0]]['type'](tmp_def_val).value
                        except TypeError:
                            pass
                        except IndexError:
                            pass
                    def_val.append(val)
                    pass
                return def_val
            elif self.__format == 'Enum':
                def_val = self.convert(self._text_attribute.Default[0], 'UInt32')
                return 0 if def_val is None else def_val
            pass
        pass

    def parser_range(self):
        self.__min = self.convert(self._text_attribute.Min[0], self.__format)
        self.__max = self.convert(self._text_attribute.Max[0], self.__format)
        if self.__max is None:
            if self.__format == 'Enum':
                import json
                try:
                    selection_limit_dict = json.loads(self._text_attribute.Default[0])
                except ValueError:
                    return None

                if type(selection_limit_dict) is not list:
                    return None

                selection_limit_val = []
                for (key, data) in selection_limit_dict.items():
                    if key in self.__choice_list:
                        try:
                            if type(data) is list:
                                val = data[0]
                            else:
                                val = data
                            if val == self.__choice_list[key][0]:
                                selection_limit_val.append(val)
                                pass
                            else:
                                pass
                        except IndexError:
                            pass
                        pass
                    else:
                        pass
                pass
                if selection_limit_val:
                    self.__selection_limit = selection_limit_val
            pass
        pass

    @property
    def text_attribute(self):
        return self._text_attribute

    @property
    def root_system(self):
        return self._text_attribute.RootSystem[0]

    @property
    def sub_system(self):
        return self._text_attribute.SubSystem[0]

    @property
    def data_path(self):
        return self._text_attribute.DataPath[0]
        pass

    @property
    def name(self):
        return self._text_attribute.Name[0]
        pass

    @property
    def description(self):
        return self._text_attribute.Description[0]
        pass

    @property
    def type(self):
        return self._text_attribute.Type[0]
        pass

    @property
    def format(self):
        return self.__format

    @property
    def max_size(self):
        num = self.convert(self._text_attribute.MaxSize[0], 'UInt32')
        return 1 if num is None else num
        pass

    @property
    def length(self):
        return self.__length

    @property
    def default(self):
        return self.__default

    @property
    def min(self):
        return self.__min

    @property
    def max(self):
        return self.__max

    @property
    def selection_limit(self):
        return self.__selection_limit

    @property
    def choice_list(self):
        return self.__choice_list

    @property
    def scale_unit(self):
        return self._text_attribute.ScaleUnit[0]
        pass

    @property
    def precision(self):
        num = self.convert(self._text_attribute.Precision[0], 'UInt8')
        return 1 if num is None else num

    @property
    def is_alarm(self):
        tmp_str = self._text_attribute.IsAlarm[0].upper()
        if tmp_str == "NO":
            return False
        elif tmp_str == "YES":
            return True
        else:
            return False
        pass

    @property
    def is_evt_log(self):
        tmp_str = self._text_attribute.IsEvtLog[0].upper()
        if tmp_str == "NO":
            return False
        elif tmp_str == "YES":
            return True
        else:
            return False
        pass

    @property
    def cmd_time_out(self):
        num = self.convert(self._text_attribute.CmdTimeOut[0], 'UInt32')
        return 1 if num is None else num

    @property
    def producer(self):
        producer_list = []
        for item in self._text_attribute.Producer.fields:
            val = getattr(self._text_attribute.Producer, item)
            if val[0].upper() == 'YES':
                producer_list.append(item)
            pass
        return producer_list
        pass

    @property
    def consumer(self):
        consumer_list = []
        for item in self._text_attribute.Consumer.fields:
            val = getattr(self._text_attribute.Consumer, item)
            if val[0].upper() == 'YES':
                consumer_list.append(item)
            pass
        return consumer_list

    @property
    def no_setting_req_consumer(self):
        no_setting_req_consumer_list = []
        for item in self._text_attribute.Consumer.fields:
            val = getattr(self._text_attribute.Consumer, item)
            if val[0].upper() == 'RO':
                no_setting_req_consumer_list.append(item)
            pass
        return no_setting_req_consumer_list

    @property
    def hash_id(self):
        num = self.convert(self._text_attribute.HashID[0], 'UInt32')
        return 0xffffffff if num is None else num
    pass


class DatagramAttributeV0V10(DatagramAttribute):
    pass


if __name__ == '__main__':
    import json
    a = '(123)'
    print(json.loads(a))
    pass
