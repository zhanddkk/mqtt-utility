import datetime
from simulator.core.DataHistory import DataHistory
from simulator.core.RepeaterParameter import RepeaterParameter


class DatagramData:
    _value = None
    instance = 0
    _topic = ''
    _history_max_size = 10

    def __init__(self, instance, topic, default_value=None):
        self.instance = instance
        self._topic = topic
        self._value = default_value
        self.repeater_info = RepeaterParameter()
        self.history = []
        pass

    @property
    def history_max_size(self):
        return self._history_max_size

    @history_max_size.setter
    def history_max_size(self, val):
        if val < 1:
            val = 1
            print('ERROR:', 'history_max_size should be grater then zero', 'but input value = ', val)
            print('So, the history_max_size be set to 1')
        self._history_max_size = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        h = DataHistory()
        h.opt = 1
        h.time = datetime.datetime.now()
        h.value = val
        self._value = val
        self.history.append(h)
        if len(self.history) > self.history_max_size:
            self.history.remove(self.history[0])
        pass

    @property
    def topic(self):
        return self._topic

    def send_value(self, val):
        h = DataHistory()
        h.opt = 0
        h.time = datetime.datetime.now()
        h.value = val
        self.history.append(h)
        if len(self.history) > self.history_max_size:
            self.history.remove(self.history[0])
        pass
    pass

if __name__ == '__main__':
    pass
