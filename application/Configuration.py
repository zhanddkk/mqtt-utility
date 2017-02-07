import configparser
import os as _os


class Configuration:
    def __init__(self):
        self.__config_file_name = 'config.ini'
        self.__config_ini = configparser.ConfigParser()
        self.__log_filter_hash_id_list = []
        pass

    def create_config(self):
        self.__config_ini['IMPORT'] = {
            'data_dictionary_path': _os.path.join(_os.path.dirname(__file__), '../')
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
        with open(self.__config_file_name, 'w') as configfile:
            self.__config_ini.write(configfile)
            configfile.close()
        pass

    def read_config(self, file_name='config.ini'):
        self.__config_file_name = file_name
        if not self.__config_ini.read(self.__config_file_name):
            self.create_config()
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
    pass

if __name__ == '__main__':
    pass
