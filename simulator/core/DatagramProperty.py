import json


class DatagramProperty:
    def __init__(self, property_data):
        self.__property_data = property_data
        self.__producer_name_list = ('UC', 'SLC_UPS', 'SLC_NMC', 'HMI', 'Tuner')
        self.__consumer_name_list = ('UC', 'SLC_UPS', 'SLC_NMC', 'HMI', 'Tuner')
    pass

    @property
    def sub_system(self):
        return self.__property_data.SubSystem

    @property
    def data_path(self):
        return self.__property_data.DataPath
        pass

    @property
    def name(self):
        return self.__property_data.Name
        pass

    @property
    def description(self):
        return self.__property_data.Description
        pass

    @property
    def type(self):
        return self.__property_data.Type
        pass

    @property
    def format(self):
        return self.__property_data.Format
        pass

    @property
    def max_size(self):
        return self.convert_str_num(self.__property_data.MaxSize)
        pass

    @property
    def default(self):
        return self.__property_data.Default
        pass

    @property
    def min(self):
        return self.convert_str_num(self.__property_data.Min)

    @property
    def max(self):
        return self.convert_str_num(self.__property_data.Max)

    @property
    def choice_list(self):
        return self.__parser_choice_list(self.__property_data.ChoiceList)
        pass

    @property
    def scale_unit(self):
        return self.__property_data.ScaleUnit
        pass

    @property
    def precision(self):
        return self.convert_str_num(self.__property_data.Precision)

    @property
    def is_alarm(self):
        tmp_str = self.__property_data.IsAlarm.upper()
        if tmp_str == "NO":
            return False
        elif tmp_str == "YES":
            return True
        else:
            return None
        pass

    @property
    def is_evt_log(self):
        tmp_str = self.__property_data.IsEvtLog.upper()
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
            self.__property_data.Producer_UC,
            self.__property_data.Producer_SLC_UPS,
            self.__property_data.Producer_SLC_NMC,
            self.__property_data.Producer_HMI,
            self.__property_data.Producer_Tuner
        )
        try:
            for index, item in enumerate(data_list):
                if item.upper() == 'YES':
                    producer_list.append(self.__producer_name_list[index])
        except IndexError:
            pass
        return producer_list
        pass

    @property
    def consumer(self):
        consumer_list = []
        data_list = (
            self.__property_data.Consumer_UC,
            self.__property_data.Consumer_SLC_UPS,
            self.__property_data.Consumer_SLC_NMC,
            self.__property_data.Consumer_HMI,
            self.__property_data.Consumer_Tuner
        )
        try:
            for index, item in enumerate(data_list):
                if item.upper() == 'YES':
                    consumer_list.append(self.__consumer_name_list[index])
        except IndexError:
            pass
        return consumer_list

    @property
    def hash_id(self):
        try:
            hash_id = int(self.__property_data.HashID, base=16)
        except ValueError:
            hash_id = 0xFFFFFFF
        return hash_id

    def __parser_choice_list(self, list_string=""):
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


