
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
        if tmp_str == "FALSE":
            return False
        elif tmp_str == "TRUE":
            return True
        else:
            return None
        pass

    @property
    def is_evt_log(self):
        tmp_str = self._is_evt_log.upper()
        if tmp_str == "FALSE":
            return False
        elif tmp_str == "TRUE":
            return True
        else:
            return None
        pass

    @property
    def producer(self):
        pass

    @property
    def consumer(self):
        pass

    @property
    def hash_id(self):
        if self._hash_id.isdigit():
            return eval(self._hash_id)
        else:
            return None
        pass

    def __parser_choice_list(self, list_string=""):
        choice_list = {}
        list_string = list_string.expandtabs(0)
        list_string = list_string.replace(' ', '')
        list_string = list_string.replace('{', '')
        list_string = list_string.rstrip('}')
        item = list_string.split('}')

        for cell in item:
            tmp = cell.split(';')
            choice_list[tmp[0]] = tmp[1]
        return choice_list


