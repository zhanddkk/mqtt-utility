from simulator.core.DatagramData import DatagramData, CmdDatagramData, SettingDatagramData


class Datagram:
    def __init__(self, attribute):
        self._data_list = []
        self._attribute = attribute
        self._make_data_list()
        pass

    @property
    def data_list(self):
        return self._data_list

    @property
    def attribute(self):
        return self._attribute

    def _make_data_list(self):
        system = self._attribute.sub_system
        path = self._attribute.data_path
        name = self._attribute.name
        default = self._attribute.default

        system = system.strip(' ')
        if system != '':
            system = 'UPSSystem/' + system
        else:
            system = 'UPSSystem'
        path = path.strip(' ')
        if path != '':
            path = '/' + path
        name = name.strip(' ')
        if name != '':
            name = '/' + name

        start = path.find('[')
        end = path.find(']')

        if self.attribute.type == 'COMMAND':
            datagram_data_class = CmdDatagramData
        elif self.attribute.type == 'SETTING':
            datagram_data_class = SettingDatagramData
        else:
            datagram_data_class = DatagramData

        if (start == -1) or (end == -1) or (start >= end) or (start < 1) or (end < 1):
            self._data_list.append(datagram_data_class(0, (system + path + name).replace('\\', '/'), default))
        else:
            num = path[start + 1:end]

            if num.isdigit():
                device_number = int(num, base=10)
                front = path[:start]
                behind = path[end + 1:]
                for i in range(device_number):
                    tmp = system + front + str(i + 1) + behind + name
                    self._data_list.append(datagram_data_class(i, tmp.replace('\\', '/'), default))
            else:
                self._data_list.append(datagram_data_class(0, (system + path + name).replace('\\', '/'), default))
        pass

    pass

