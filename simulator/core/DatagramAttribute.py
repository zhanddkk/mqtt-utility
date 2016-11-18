head_name_list = ('SubSystem,'
                  'DataPath,Name,'
                  'Description,'
                  'Type,'
                  'Format,'
                  'MaxSize,'
                  'Default,'
                  'Min,'
                  'Max,'
                  'ChoiceList,'
                  'ScaleUnit,'
                  'Precision,'
                  'IsAlarm,'
                  'IsEvtLog,'
                  'CmdTimeOut,'
                  'Producer,'
                  'Producer_0 ,'
                  'Producer_1 ,'
                  'Producer_2 ,'
                  'Producer_3 ,'
                  'Consumer,'
                  'Consumer_0 ,'
                  'Consumer_1 ,'
                  'Consumer_2 ,'
                  'Consumer_3 ,'
                  'HashID')
producer_name_list = ('UC', 'SLC_UPS', 'SLC_NMC', 'HMI', 'Tuner')
consumer_name_list = ('UC', 'SLC_UPS', 'SLC_NMC', 'HMI', 'Tuner')
integer_data_type_info = {
    'int8_t': [-128, 127],
    'int16_t': [-32768, 32767],
    'int32_t': [-2147483648, 2147483647],
    'bool': [0, 1],
    'uint8_t': [0, 0xff],
    'uint16_t': [0, 0xffff],
    'uint32_t': [0, 0xffffffff],
    "BOOL": [0, 1],
    "8BS": [-128, 127],
    "8BUS": [0, 0xff],
    "16BS": [-32768, 32767],
    "16BUS": [0, 0xffff],
    "32BS": [-2147483648, 2147483647],
    "32BUS": [0, 0xffffffff],
}


class DatagramAttribute:
    def __init__(self, info_from_csv):
        self._text_attribute = info_from_csv
        self.data_list = []
        pass

    @property
    def text_attribute(self):
        return self._text_attribute

    @property
    def sub_system(self):
        return self._text_attribute.SubSystem

    @property
    def data_path(self):
        return self._text_attribute.DataPath
        pass

    @property
    def name(self):
        return self._text_attribute.Name
        pass

    @property
    def description(self):
        return self._text_attribute.Description
        pass

    @property
    def type(self):
        return self._text_attribute.Type
        pass

    @property
    def format(self):
        return self._text_attribute.Format
        pass

    @property
    def max_size(self):
        return self.convert_str_num(self._text_attribute.MaxSize)
        pass

    @property
    def default(self):
        if self._text_attribute.Format in integer_data_type_info:
            def_val = self.convert_str_num(self._text_attribute.Default)
            if def_val is None:
                def_val = 0
            return def_val
        else:
            if self._text_attribute.Format == '32BFL':
                try:
                    def_val = float(self._text_attribute.Default)
                except ValueError:
                    def_val = 0.0
                    pass
                return def_val
            elif self._text_attribute.Format == 'BINARY_BLOC':
                import json
                structure_format = self.choice_list
                try:
                    def_val_dic = json.loads(self._text_attribute.Default)
                except json.JSONDecodeError:
                    return None

                def_val = []
                for (k, d) in structure_format.items():
                    try:
                        def_val.append(def_val_dic[k])
                    except KeyError:
                        if d in integer_data_type_info:
                            def_val.append(0)
                        else:
                            val = None
                            if d == 'string':
                                val = ''
                            elif d == 'float':
                                val = 0.0
                            def_val.append(val)
                            pass
                        pass
                    pass
                return def_val
                pass
            return self._text_attribute.Default
        pass

    @property
    def min(self):
        return self.convert_str_num(self._text_attribute.Min)

    @property
    def max(self):
        return self.convert_str_num(self._text_attribute.Max)

    @property
    def choice_list(self):
        return self.__parser_choice_list(self._text_attribute.ChoiceList)
        pass

    @property
    def scale_unit(self):
        return self._text_attribute.ScaleUnit
        pass

    @property
    def precision(self):
        return self.convert_str_num(self._text_attribute.Precision)

    @property
    def is_alarm(self):
        tmp_str = self._text_attribute.IsAlarm.upper()
        if tmp_str == "NO":
            return False
        elif tmp_str == "YES":
            return True
        else:
            return None
        pass

    @property
    def is_evt_log(self):
        tmp_str = self._text_attribute.IsEvtLog.upper()
        if tmp_str == "NO":
            return False
        elif tmp_str == "YES":
            return True
        else:
            return None
        pass

    @property
    def producer(self):
        producer_list = []
        data_list = (
            self._text_attribute.Producer,
            self._text_attribute.Producer_0,
            self._text_attribute.Producer_1,
            self._text_attribute.Producer_2,
            self._text_attribute.Producer_3
        )
        try:
            for index, item in enumerate(data_list):
                if item.upper() == 'YES':
                    producer_list.append(producer_name_list[index])
        except IndexError:
            pass
        return producer_list
        pass

    @property
    def consumer(self):
        consumer_list = []
        data_list = (
            self._text_attribute.Consumer,
            self._text_attribute.Consumer_0,
            self._text_attribute.Consumer_1,
            self._text_attribute.Consumer_2,
            self._text_attribute.Consumer_3
        )
        try:
            for index, item in enumerate(data_list):
                if item.upper() == 'YES':
                    consumer_list.append(consumer_name_list[index])
        except IndexError:
            pass
        return consumer_list

    @property
    def hash_id(self):
        try:
            hash_id = int(self._text_attribute.HashID, base=16)
        except ValueError:
            hash_id = 0xFFFFFFF
        return hash_id

    def __parser_choice_list(self, list_string=""):
        import json
        choice_list = {}
        try:
            choice_list = json.loads(list_string, object_pairs_hook=self.json_object_pairs_hook)
        except json.JSONDecodeError:
            pass
        return choice_list

    @staticmethod
    def convert_str_num(string_num=""):
        num = None
        if string_num.isdigit():
            num = int(string_num, base=10)
        else:
            string_num = string_num.upper()
            if string_num.find('.') >= 0:
                try:
                    num = float(string_num)
                except ValueError:
                    pass
            if string_num.find('X') == 1:
                try:
                    num = int(string_num, base=16)
                except ValueError:
                    pass
        return num
        pass

    @staticmethod
    def json_object_pairs_hook(list_data):
        import collections
        return collections.OrderedDict(list_data)
        pass
    pass

if __name__ == '__main__':
    pass
