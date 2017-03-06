import configparser
import os as _os
import json


class Configuration:
    def __init__(self):
        self.__config_file_name = 'config.ini'
        self.__config_ini = configparser.ConfigParser()
        self.__log_filter_hash_id_list = []
        self.__node_data = {}
        pass

    def __do_init(self):
        self.__node_data = json.loads(self.__config_ini['NODE_DEFINE']['data'])

    def create_config(self):
        self.__config_ini['IMPORT'] = {
            'data_dictionary_path': _os.path.join(_os.path.dirname(__file__), '..'),
            'data_dictionary_file_name': 'dd_source/default_data_dictionary.csv'
        }
        self.__config_ini['SETTING_DATA_FILE'] = {
            'dictionary_path': _os.path.join(_os.path.dirname(__file__), '..')
        }
        self.__config_ini['CONNECT_TO_BROKER'] = {
            'broker_address': 'localhost',
            'broker_net_port': '1883'
        }
        self.__config_ini['LOCAL_BROKER'] = {
            'net_port': '1883'
        }
        self.__config_ini['LOG_FILTER'] = {
            'hash_id_list': ''
        }
        _uc_node_data = {
            'name': 'UC',
            'device_index': 0,
            'communication_status_hash_id': '0x62E89354',
            'script': 'nodescript/UcNode.py',
            'args': '{dd},{ip},{port}'.format(
                dd='Default',
                ip='Default',
                port='Default')
        }
        _hmi_node_data = {
            'name': 'HMI',
            'device_index': 0,
            'communication_status_hash_id': '0x37CFE282',
            'script': 'nodescript/HmiNode.py',
            'args': '{dd},{ip},{port}'.format(
                dd='Default',
                ip='Default',
                port='Default')
        }
        self.__node_data = {
            'UC_0': _uc_node_data,
            'HMI_0': _hmi_node_data
        }
        self.__config_ini['NODE_DEFINE'] = {
            'data': json.dumps(self.__node_data, indent=4)
        }
        self.__config_ini['PYTHON'] = {
            'executable': 'python'
        }
        with open(self.__config_file_name, 'w') as configfile:
            self.__config_ini.write(configfile)
            configfile.close()
        pass

    def read_config(self, file_name='config.ini'):
        self.__config_file_name = file_name
        if not self.__config_ini.read(self.__config_file_name):
            self.create_config()
        else:
            self.__do_init()
        pass

    def save_config(self):
        with open(self.__config_file_name, 'w') as configfile:
            self.__config_ini.write(configfile)
            configfile.close()
        pass

    @property
    def data_dictionary_path(self):
        return self.__config_ini['IMPORT']['data_dictionary_path']

    @data_dictionary_path.setter
    def data_dictionary_path(self, path):
        self.__config_ini['IMPORT']['data_dictionary_path'] = path

    @property
    def data_dictionary_file_name(self):
        return self.__config_ini['IMPORT']['data_dictionary_file_name']

    @data_dictionary_file_name.setter
    def data_dictionary_file_name(self, file_name):
        self.__config_ini['IMPORT']['data_dictionary_file_name'] = file_name

    @property
    def connect_broker_ip(self):
        return self.__config_ini['CONNECT_TO_BROKER']['broker_address']

    @connect_broker_ip.setter
    def connect_broker_ip(self, ip):
        self.__config_ini['CONNECT_TO_BROKER']['broker_address'] = ip
        pass

    @property
    def connect_broker_ip_port(self):
        return int(self.__config_ini['CONNECT_TO_BROKER']['broker_net_port'])

    @connect_broker_ip_port.setter
    def connect_broker_ip_port(self, port):
        if port < 0 or port > 65535:
            print('ERROR:', 'Invalid port')
            return
        self.__config_ini['CONNECT_TO_BROKER']['broker_net_port'] = str(port)

    @property
    def log_filter_hash_id_list(self):
        _txt = self.__config_ini['LOG_FILTER']['hash_id_list'].split(',')
        try:
            return [int(value, base=16) for value in _txt]
        except ValueError:
            return []

    @log_filter_hash_id_list.setter
    def log_filter_hash_id_list(self, hash_id_list):
        self.__config_ini['LOG_FILTER']['hash_id_list'] = ','.join('0x{:>08X}'.format(value) for value in hash_id_list)

    @property
    def setting_data_file_path(self):
        return self.__config_ini['SETTING_DATA_FILE']['dictionary_path']
        pass

    @setting_data_file_path.setter
    def setting_data_file_path(self, path):
        self.__config_ini['SETTING_DATA_FILE']['dictionary_path'] = path

    @property
    def special_hash_ids(self):
        return self.__config_ini['SPECIAL_HASH_IDS']

    @property
    def node_data(self):
        self.__node_data = json.loads(self.__config_ini['NODE_DEFINE']['data'])
        return self.__node_data

    def add_node(self, name, hash_id, device_index, script, args):
        self.__node_data['{}_{}'.format(name, device_index)] = {
            'name': name,
            'device_index': device_index,
            'communication_status_hash_id': hash_id,
            'script': script,
            'args': args
        }
        self.__config_ini['NODE_DEFINE']['data'] = json.dumps(self.__node_data, indent=4)
        pass

    def get_node(self, name, device_index):
        _key = '{}_{}'.format(name, device_index)
        try:
            return self.__node_data[_key]
        except KeyError:
            return {}

    @property
    def python_exe(self):
        return self.__config_ini['PYTHON']['executable']
        pass

    @python_exe.setter
    def python_exe(self, path):
        self.__config_ini['PYTHON']['executable'] = path
    pass

if __name__ == '__main__':
    pass
