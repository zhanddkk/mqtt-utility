import datetime


class Datagram:
    def __init__(self, property_data):
        self.__value = []
        self.__history_value = []       # [operation, date_time, value] operation : 0(receive), 1(send)
        self.__buf = []
        self.__max_history_len = 10
        self.__property = property_data
        self.__id = property_data.hash_id
        self.__topic = self.__parser_topic(property_data.data_path,
                                           property_data.name,
                                           property_data.sub_system)
        self.__device_number = len(self.__topic)

        for i in range(self.__device_number):
            self.__value.append(None)
            self.__history_value.append([])
            self.__buf.append([None])

    pass

    @property
    def id(self):
        return self.__id

    @property
    def values(self):
        return self.__value

    @property
    def topics(self):
        return self.__topic
        pass

    @property
    def device_number(self):
        return self.__device_number

    @property
    def history(self):
        return self.__history_value

    @property
    def property(self):
        return self.__property

    def get_value(self, index=0):
        try:
            return self.__value[index]
        except IndexError:
            print('Index error')
            return None

    def set_value(self, val, index=0):
        try:
            self.__value[index] = val
        except IndexError:
            print('Index error')
            pass

    def get_topic(self, index=0):
        try:
            return self.__topic[index]
        except IndexError:
            print('Index error')
            return None

    def set_buf(self, val, index=0):
        try:
            self.__buf[index][0] = val
        except IndexError:
            print('Index error')
        pass

    def save_history(self, index, operation):
        try:
            if len(self.__history_value[index]) > self.__max_history_len:
                self.__history_value[index].remove(self.__history_value[index][0])
            if operation == 0:
                self.__history_value[index].append([operation, datetime.datetime.now(), self.__value[index]])
            else:
                self.__history_value[index].append([operation, datetime.datetime.now(), self.__buf[index][0]])
        except IndexError:
            print('Index error')
            pass

    @staticmethod
    def __parser_topic(path='', name='', system=''):
        topic = []

        system = system.strip(' ')
        if system != '':
            system = 'UPS_System\\' + system
        else:
            system = 'UPS_System'
        path = path.strip(' ')
        if path != '':
            path = '\\' + path
        name = name.strip(' ')
        if name != '':
            name = '\\' + name

        start = path.find('[')
        end = path.find(']')

        if (start == -1) or (end == -1) or (start >= end) or (start < 1) or (end < 1):
            topic.append(system + path + name)
        else:
            num = path[start + 1:end]
            if num.isdigit():
                device_number = int(num, base=10)
                front = path[:start]
                behind = path[end + 1:]
                for i in range(device_number):
                    tmp = system + front + str(i + 1) + behind + name
                    topic.append(tmp)
            else:
                topic.append(system + path + name)
        return topic
        pass
    pass

if __name__ == "__main__":
    a = ['123', 'test']
    print(a)
    a.remove(a[0])
    print(a)
    pass
