from simulator.datadictionary.DataProperty import DataProperty


class Datagram:
    def __init__(self, data=[], index={}):
        self.topic = ""
        self.id = 0
        self.device_index = 1
        self.value = []
        self.data_property = DataProperty(data, index)
    pass

    def get_id(self):
        return self.id
        pass

    def get_topic(self):
        return self.topic
        pass

    def get_value(self, index=0):
        if index >= len(self.value):
            index = -1
        return self.value[index]
        pass

    def set_value(self, value, index=0):
        if index >= len(self.value):
            index = -1
        self.value[index] = value
        pass


