import datetime
from .NamedList import named_list
history_data_item_type = named_list('HistoryDataType', 'operation, data_time, value, additional_data')


class DatagramDeviceDataHistory:
    def __init__(self, history_max_len=20):
        self.__data = []
        self.__history_max_len = history_max_len
        pass

    @property
    def data(self):
        return self.__data

    @property
    def len(self):
        return len(self.__data)

    def append_data(self, operation, value, additional_data=None):
        data_time = datetime.datetime.now()
        self.data.append(history_data_item_type(operation, data_time, value, additional_data))
        if len(self.__data) > self.__history_max_len:
            self.__data.remove(self.__data[0])

    pass


if __name__ == '__main__':
    pass
