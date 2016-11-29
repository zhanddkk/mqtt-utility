import configparser


class Configuration:
    def __init__(self):
        self.config_file_name = 'config.ini'
        self.config_ini = configparser.ConfigParser()
        pass

    def create_config(self):
        self.config_ini['MQTT_CONNECT'] = {
            'broker_address': 'localhost',
            'broker_net_port': '1883'
        }
        self.config_ini['MQTT_BROKER'] = {
            'net_port': '1883'
        }
        with open(self.config_file_name, 'w') as configfile:
            self.config_ini.write(configfile)
            configfile.close()
        pass

    def read_config(self, file_name='config.ini'):
        self.config_file_name = file_name
        if not self.config_ini.read(self.config_file_name):
            self.create_config()
        pass

    def save_config(self):
        with open(self.config_file_name, 'w') as configfile:
            self.config_ini.write(configfile)
            configfile.close()
        pass

    @property
    def mqtt_connect_addr(self):
        return self.config_ini['MQTT_CONNECT']['broker_address']

    @mqtt_connect_addr.setter
    def mqtt_connect_addr(self, addr):
        self.config_ini['MQTT_CONNECT']['broker_address'] = addr
        pass

    @property
    def mqtt_connect_port(self):
        return int(self.config_ini['MQTT_CONNECT']['broker_net_port'])

    @mqtt_connect_port.setter
    def mqtt_connect_port(self, port):
        if port < 0 or port > 65535:
            print('ERROR:', 'Invalid port')
            return
        self.config_ini['MQTT_CONNECT']['broker_net_port'] = str(port)

    pass

if __name__ == '__main__':
    pass
