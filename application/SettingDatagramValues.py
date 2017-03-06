import json
import threading
from collections import OrderedDict
from AppVersion import __doc__ as __app_version__
from StdoutDlg import ProcessStdoutDlg, StdoutDlg
from QSimpleThread import QSimpleThread
from PyQt5.QtCore import QProcess, QObject
from ddclient.dgpayload import E_DATAGRAM_ACTION_REQUEST, E_DATAGRAM_ACTION_PUBLISH


class SettingDatagramValues(QObject):
    def __init__(self, datagram_manager, configuration, parent=None):
        super(SettingDatagramValues, self).__init__(parent)
        self.__parent = parent
        self.__dgm = datagram_manager
        self.version = '0.0.1'
        self.node_status = OrderedDict()
        self.comment = 'Created by simulator({})'.format(__app_version__)
        self.__config = configuration
        self.node_data = configuration.node_data
        self.process_data = {}
        self.__dump_ret = False
        self.__finished_event = threading.Event()
        self.__ready_count = 0
        pass

    def __run_node(self, node_id, node):
        _process = QProcess()
        _process_stdout_dlg = ProcessStdoutDlg(self.__parent, _process, node_id)
        _process_stdout_dlg.process_stdout_message.message_signal.connect(self.__on_process_message)
        self.process_data[node_id] = _process_stdout_dlg
        _args = node['args'].split(',')
        try:
            if _args[0] == 'Default':
                _args[0] = '{}/{}'.format(self.__config.data_dictionary_path, self.__config.data_dictionary_file_name)
            if _args[1] == 'Default':
                _args[1] = self.__config.connect_broker_ip
            if _args[2] == 'Default':
                _args[2] = str(self.__config.connect_broker_ip_port)
        except IndexError:
            pass
        _args.insert(0, node['script'])
        _process.start(self.__config.python_exe, _args)
        _process_stdout_dlg.show()
        pass

    def __on_process_message(self, msg):
        if msg == 'Node Connected':
            self.__ready_count += 1
            if self.__ready_count == len(self.process_data):
                self.__finished_event.set()
        pass

    def __check_node_status(self):
        for _key, node in self.node_data.items():
            # 'name': name,
            # 'device_index': device_index,
            # 'communication_status_hash_id': hash_id,
            # 'script': script,
            # 'args': args
            try:
                dg = self.__dgm.get_datagram(int(node['communication_status_hash_id'], base=16))
                if dg is not None:
                    dev_index = node['device_index']
                    _value = dg.get_device_data_value(dev_index)
                    _name = None
                    if dg.attribute.choice_list is not None:
                        for _key2, _data2 in dg.attribute.choice_list.content.items():
                            if _data2.value == _value:
                                _name = _key2
                    self.node_status[_key] = {'value': _value,
                                              'name': _name}
                    if _value != 2:
                        self.__run_node(_key, node)
                        pass
                    pass
                else:
                    self.node_status[_key] = {'value': None, 'name': 'Not find this datagram'}
            except KeyError:
                self.node_status[_key] = {'value': None, 'name': 'Not define'}
            pass

        pass

    def __wait_task(self, stdout_dlg):
        second = 0
        while not self.__finished_event.is_set():
            stdout_dlg.puts('Wait time {}s.\n'.format(second))
            self.__finished_event.wait(1)
            second += 1
            pass
        stdout_dlg.close_signal.emit()
        pass

    def dump(self, file_name):
        self.__check_node_status()
        _node_simulators = []
        if self.process_data:
            _stdout_dlg = StdoutDlg(self.__parent)
            _stdout_dlg.puts('Wait nodes\' status being AUTHENTICATED...\n')
            _dump_thread = QSimpleThread(target=self.__wait_task, args=(_stdout_dlg,))
            _dump_thread.start()
            _stdout_dlg.exec()
            if not self.__finished_event.is_set():
                self.__finished_event.set()
            for node in self.node_data.values():
                _node_simulators.append(node['name'])

        try:
            _data = []
            for hash_id, dg in self.__dgm.datagram_dictionary.items():
                if dg.attribute.type == 'Setting':
                    for dev_index in range(dg.device_number):
                        _data_item = OrderedDict()
                        _data_item['HashId'] = '0x{:>08X}'.format(hash_id)
                        _data_item['device_index'] = dev_index
                        _producer = dg.attribute.producer[0]
                        if _producer in _node_simulators:
                            _action = E_DATAGRAM_ACTION_REQUEST
                        else:
                            _action = E_DATAGRAM_ACTION_PUBLISH
                        _value = dg.get_device_data_value(dev_index, _action)
                        _name = None
                        if dg.attribute.choice_list is not None:
                            for _key2, _data2 in dg.attribute.choice_list.content.items():
                                if _data2.value == _value:
                                    _name = _key2

                        _data_item['value'] = _value
                        _data_item['comment'] = _name
                        _data_item['action'] = _action
                        _data.append(_data_item)
                        pass
                pass
            _obj = OrderedDict(
                (
                    ('Version', self.version),
                    ('NodeStatus', self.node_status),
                    ('Data', _data)
                )
            )
            with open(file_name, 'w') as fp:
                json.dump(_obj, fp, indent=4)
            return True
        except Exception as exception:
            print('ERROR:', type(exception).__name__, exception)
            return False
            pass
        pass

    def load(self, file_name):
        pass

    pass
