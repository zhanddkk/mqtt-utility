from simulator.datadictionary.DataProperty import DataProperty


class Datagram:
    def __init__(self, data=[], index={}):
        self._value = []
        self.data_property = DataProperty(data, index)
        self._topic = self.__parser_topic(self.data_property.data_path,
                                          self.data_property.name,
                                          self.data_property.sub_system)
        self._device_number = len(self._topic)
        for i in range(self._device_number):
            self._value.append(None)
    pass

    @property
    def id(self):
        return self.data_property.hash_id

    @property
    def topic_list(self):
        return self._topic
        pass

    @property
    def device_num(self):
        return len(self._topic)

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, val=[0, None]):
        if val[0] >= self._device_number:
            val[0] = -1
        self._value[val[0]] = val[1]
        pass

    def get_value(self, index=0):
        if index >= self._device_number:
            index = -1
        return self._value[index]

    def set_value(self, val, index=0):
        if index >= self._device_number:
            index = -1
        self._value[index] = val

    def get_topic(self, index=0):
        if index >= self._device_number:
            index = -1
        return self._topic[index]

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
                device_number = eval(num)
                front = path[:start]
                behind = path[end + 1:]
                for i in range(device_number):
                    tmp = system + front + str(i + 1) + behind + name
                    topic.append(tmp)
            else:
                topic.append(system + path + name)
        return topic
        pass




