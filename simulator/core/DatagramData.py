import datetime
from collections import OrderedDict
from simulator.core.DataHistory import DataHistory
from simulator.core.RepeaterParameter import RepeaterParameter
from simulator.core import PayloadPackage


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

    def set_value(self, val, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        h = DataHistory()
        h.opt = 1
        h.time = datetime.datetime.now()
        h.value = val
        self._value = val
        self.history.append(h)
        if len(self.history) > self.history_max_size:
            self.history.remove(self.history[0])

    def get_history(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        return self.history
        pass

    def get_value(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        return self._value

    def get_topic(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        return self._topic

    def send_value(self, val, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        h = DataHistory()
        h.opt = 0
        h.time = datetime.datetime.now()
        h.value = val
        self.history.append(h)
        if len(self.history) > self.history_max_size:
            self.history.remove(self.history[0])
        pass
    pass


class CmdDatagramData:
    __history_max_size = 10

    def __init__(self, instance, topic, default_value=None):
        self.instance = instance
        self.__topic = topic
        self.__value = {
            PayloadPackage.E_DATAGRAM_ACTION_PUBLISH: default_value,
            PayloadPackage.E_DATAGRAM_ACTION_RESPONSE: 0,
            PayloadPackage.E_DATAGRAM_ACTION_ALLOW: 1
        }
        self.repeater_info = RepeaterParameter()
        self.__history = {
            # PayloadPackage.E_DATAGRAM_ACTION_PUBLISH: OrderedDict(),
            # PayloadPackage.E_DATAGRAM_ACTION_RESPONSE: OrderedDict(),
            PayloadPackage.E_DATAGRAM_ACTION_PUBLISH: [],
            PayloadPackage.E_DATAGRAM_ACTION_RESPONSE: [],
            PayloadPackage.E_DATAGRAM_ACTION_ALLOW: []
        }

    @property
    def history_max_size(self):
        return self.__history_max_size

    @history_max_size.setter
    def history_max_size(self, val):
        if val < 1:
            val = 1
            print('ERROR:', 'history_max_size should be grater then zero', 'but input value = ', val)
            print('So, the history_max_size be set to 1')
        self.__history_max_size = val

    @property
    def topic(self):
        return self.__topic

    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, val):
        self.set_value(val)

    @property
    def history(self):
        return self.get_history()
        pass

    def get_topic(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        if action == PayloadPackage.E_DATAGRAM_ACTION_PUBLISH:
            return self.__topic
            pass
        elif action == PayloadPackage.E_DATAGRAM_ACTION_RESPONSE:
            return 'Response/' + self.__topic
            pass
        elif action == PayloadPackage.E_DATAGRAM_ACTION_ALLOW:
            return 'AllowedRequest/' + self.__topic
            pass
        else:
            print('ERROR:', 'Action code is error', action)
            return None
        pass

    def get_history(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        if action in self.__history:
            return self.__history[action]
        else:
            print('ERROR:', 'Action code is error', action)
            return None
        pass

    def get_value(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        if action in self.__value:
            return self.__value[action]
        else:
            print('ERROR:', 'Action code is error', action)
            return None
        pass

    def set_value(self, val, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        if action in self.__value:
            h = DataHistory()
            h.opt = 1
            h.time = datetime.datetime.now()
            h.value = val
            self.__value[action] = val
            self.__history[action].append(h)
            if len(self.__history[action]) > self.history_max_size:
                self.__history[action].remove(self.__history[action][0])
            '''
            if action == PayloadPackage.E_DATAGRAM_ACTION_ALLOW:
                self.history[action].append(h)
                if len(self.history[action]) > self.history_max_size:
                    self.history[action].remove(self.history[action][0])
            else:
                if type(val) is int:
                    self.history[action][val >> 8] = h
                    if len(self.history[action]) > self.history_max_size:
                        self.history[action].popitem(last=0)
                        pass
                pass
            '''
        else:
            print('ERROR:', 'Action code is error', action)
        pass

    def send_value(self, val, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        h = DataHistory()
        h.opt = 0
        h.time = datetime.datetime.now()
        h.value = val
        if action in self.__history:
            self.__history[action].append(h)
            if len(self.__history[action]) > self.history_max_size:
                self.__history[action].remove(self.__history[action][0])
        else:
            print('ERROR:', 'Action code is error', action)
        pass


class SettingDatagramData:
    __history_max_size = 10

    def __init__(self, instance, topic, default_value=None):
        self.instance = instance
        self.__topic = topic
        self.__value = {
            PayloadPackage.E_DATAGRAM_ACTION_PUBLISH: default_value,
            PayloadPackage.E_DATAGRAM_ACTION_REQUEST: default_value,
            PayloadPackage.E_DATAGRAM_ACTION_RESPONSE: 0,
            PayloadPackage.E_DATAGRAM_ACTION_ALLOW: 1
        }
        self.repeater_info = RepeaterParameter()
        self.__history = {
            PayloadPackage.E_DATAGRAM_ACTION_PUBLISH: [],
            PayloadPackage.E_DATAGRAM_ACTION_REQUEST: [],
            PayloadPackage.E_DATAGRAM_ACTION_RESPONSE: [],
            PayloadPackage.E_DATAGRAM_ACTION_ALLOW: []
        }

    @property
    def history_max_size(self):
        return self.__history_max_size

    @history_max_size.setter
    def history_max_size(self, val):
        if val < 1:
            val = 1
            print('ERROR:', 'history_max_size should be grater then zero', 'but input value = ', val)
            print('So, the history_max_size be set to 1')
        self.__history_max_size = val

    @property
    def topic(self):
        return self.__topic

    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, val):
        self.set_value(val)

    @property
    def history(self):
        return self.get_history()
        pass

    def get_topic(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        if action == PayloadPackage.E_DATAGRAM_ACTION_PUBLISH:
            return self.__topic
            pass
        elif action == PayloadPackage.E_DATAGRAM_ACTION_REQUEST:
            return 'Request/' + self.__topic
            pass
        elif action == PayloadPackage.E_DATAGRAM_ACTION_RESPONSE:
            return 'Response/' + self.__topic
            pass
        elif action == PayloadPackage.E_DATAGRAM_ACTION_ALLOW:
            return 'AllowedRequest/' + self.__topic
            pass
        else:
            print('ERROR:', 'Action code is error', action)
            return None
        pass

    def get_history(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        if action in self.__history:
            return self.__history[action]
        else:
            print('ERROR:', 'Action code is error', action)
            return None
        pass

    def get_value(self, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        if action in self.__value:
            return self.__value[action]
        else:
            print('ERROR:', 'Action code is error', action)
            return None
        pass

    def set_value(self, val, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        if action in self.__value:
            h = DataHistory()
            h.opt = 1
            h.time = datetime.datetime.now()
            h.value = val
            self.__value[action] = val
            self.__history[action].append(h)
            if len(self.__history[action]) > self.history_max_size:
                self.__history[action].remove(self.__history[action][0])
        else:
            print('ERROR:', 'Action code is error', action)
        pass

    def send_value(self, val, action=PayloadPackage.E_DATAGRAM_ACTION_PUBLISH):
        h = DataHistory()
        h.opt = 0
        h.time = datetime.datetime.now()
        h.value = val
        if action in self.__history:
            self.__history[action].append(h)
            if len(self.__history[action]) > self.history_max_size:
                self.__history[action].remove(self.__history[action][0])
        else:
            print('ERROR:', 'Action code is error', action)
        pass

if __name__ == '__main__':
    dictionary = {'b': 10, 'a': 44, 'o': 66, 'd': 32}
    a = sorted(dictionary.items(), key=lambda d: d[0])
    print(a)
    a.test = 5
    print(a)
    pass
