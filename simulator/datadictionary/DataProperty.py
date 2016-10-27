import re
import json

class DataProperty:
    def __init__(self, data=[], index={}):
        self._sub_system = data[index["SubSystem"]]
        self._data_path = data[index["DataPath"]]
        self._name = data[index["Name"]]
        self._description = data[index["Description"]]
        self._type = data[index["Type"]]
        self._format = data[index["Format"]]
        self._max_size = data[index["MaxSize"]]
        self._default = data[index["Default"]]
        self._min = data[index["Min"]]
        self._max = data[index["Max"]]
        self._choice_list = data[index["ChoiceList"]]
        self._scale_unit = data[index["ScaleUnit"]]
        self._precision = data[index["Precision"]]
        self._is_alarm = data[index["IsAlarm"]]
        self._is_evt_log = data[index["IsEvtLog"]]
        self._producer = data[index["Producer"]:index["Consumer"]]
        self._consumer = data[index["Consumer"]:index["HashID"]]
        self._hash_id = data[index["HashID"]]
        self.__producer_name_list = index["PropertyNameList"][1][index["Producer"]:index["Consumer"]]
        self.__consumer_name_list = index["PropertyNameList"][1][index["Consumer"]:index["HashID"]]
        pass

    @property
    def sub_system(self):
        return self._sub_system

    @property
    def data_path(self):
        return self._data_path
        pass

    @property
    def name(self):
        return self._name
        pass

    @property
    def description(self):
        return self._description
        pass

    @property
    def type(self):
        return self._type
        pass

    @property
    def format(self):
        return self._format
        pass

    @property
    def max_size(self):
        if self._max_size.isdigit():
            return eval(self._max_size)
        else:
            return None
        pass

    @property
    def default(self):
        return self._default
        pass

    @property
    def min(self):
        if self._min.isdigit():
            return eval(self._min)
        else:
            return None
        pass

    @property
    def max(self):
        if self._max.isdigit():
            return eval(self._max)
        else:
            return None
        pass

    @property
    def choice_list(self):
        return self.__parser_choice_list(self._choice_list)
        pass

    @property
    def scale_unit(self):
        return self._scale_unit
        pass

    @property
    def precision(self):
        if self._precision.isdigit():
            return eval(self._precision)
        else:
            return None
        pass

    @property
    def is_alarm(self):
        tmp_str = self._is_alarm.upper()
        if tmp_str == "NO":
            return False
        elif tmp_str == "YES":
            return True
        else:
            return None
        pass

    @property
    def is_evt_log(self):
        tmp_str = self._is_evt_log.upper()
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
        for index in range(len(self._producer)):
            tmp = self._producer[index].upper()
            if tmp == "YES":
                producer_list.append(self.__producer_name_list[index])
        return producer_list
        pass

    @property
    def consumer(self):
        consumer_list = []
        for index in range(len(self._consumer)):
            tmp = self._consumer[index].upper()
            if tmp == "YES":
                consumer_list.append(self.__consumer_name_list[index])
        return consumer_list
        pass

    @property
    def hash_id(self):
        tmp = '' + self._hash_id.upper()
        tmp_id = None
        if tmp.startswith('0X'):
            if re.match(r'[0-9A-F]+', tmp[2:]):
                tmp_id = eval(tmp)
        return tmp_id
        pass

    @staticmethod
    def __parser_choice_list(list_string=""):
        choice_list = {}
        try:
            choice_list = json.loads(list_string)
        except json.JSONDecodeError:
            pass
        return choice_list


