from simulator.core.Datagram import Datagram
from simulator.core.DatagramProperty import DatagramProperty
import csv
import cbor
from collections import namedtuple
import paho.mqtt.client as DataClient
from simulator.core.MqttMessagePackage import MqttMessagePackage
import threading


class DatagramManager:
    datagram_property_names = 'SubSystem,'      \
                              'DataPath,'       \
                              'Name,'           \
                              'Description,'    \
                              'Type,'           \
                              'Format,'         \
                              'MaxSize,'        \
                              'Default,'        \
                              'Min,'            \
                              'Max,'            \
                              'ChoiceList,'     \
                              'ScaleUnit,'      \
                              'Precision,'      \
                              'IsAlarm,'        \
                              'IsEvtLog,'       \
                              'CmdTimeOut,'     \
                              'Producer_UC,'        \
                              'Producer_SLC_UPS,'   \
                              'Producer_SLC_NMC,'   \
                              'Producer_HMI,'       \
                              'Producer_Tuner,'     \
                              'Consumer_UC,'        \
                              'Consumer_SLC_UPS,'   \
                              'Consumer_SLC_NMC,'   \
                              'Consumer_HMI,'       \
                              'Consumer_Tuner,'     \
                              'HashID'

    def __init__(self):
        self.name = 'DatagramManager'   # DatagramManager name
        self.broker = 'localhost'       # MQTT broker
        self.port = 1883                # MQTT broker port
        self.client = None
        self.is_connect = False
        self.update_data_callback = None
        self.user_data = None

        self.__data_dict = {}     # Data dictionary {id: datagram}
        self.__indexes = []       # item = [id, device_index, topic]
        self.this_operation_index = None

    @property
    def index_list(self):
        return self.__indexes

    @property
    def datagram_dict(self):
        return self.__data_dict

    @property
    def len(self):
        return len(self.__indexes)

    def clear_all_data(self):
        self.__data_dict.clear()
        self.__indexes.clear()

    def import_csv(self, file_name=''):
        datagram_property = namedtuple('DatagramRecord', self.datagram_property_names)
        try:
            with open(file_name, newline='') as csv_file:
                try:
                    next(csv_file)
                    next(csv_file)
                    reader = csv.reader(csv_file, dialect='excel')
                    for record in map(datagram_property._make, reader):
                        property_data = DatagramProperty(record)
                        hash_id = property_data.hash_id
                        datagram = Datagram(property_data)
                        try:
                            self.__data_dict[hash_id] = datagram
                            for index, topic in enumerate(datagram.topics):
                                self.__indexes.append([hash_id, index, topic])
                        except KeyError:
                            pass
                    return True
                except csv.Error as e:
                    print(e)
                    return False
        except FileNotFoundError as e:
            print(e)
            return False
        pass

    def get_datagram_by_id(self, hash_id=0):
        try:
            return self.__data_dict[hash_id]
        except KeyError:
            return None
    ####################################################################################################################
    # Mosquitto operation

    def connect_data_server(self):
        import os
        self.client = DataClient.Client(self.name + str(os.getppid()) + str(threading.get_ident()), userdata=self)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except ConnectionRefusedError as e:
            print(e)
            self.is_connect = False
        except TimeoutError as e:
            print(e)
            self.is_connect = False
            pass

    pass

    def disconnect_data_server(self):
        self.client.disconnect()
        self.client.loop_stop(force=False)
        self.client = None
        self.is_connect = False
        pass

    def send_data_to_server(self, hash_id, dev_index, data_package):
        if self.is_connect:
            payload = cbor.dumps(data_package.value_package)
            dg = self.get_datagram_by_id(hash_id)
            topic = dg.get_topic(dev_index)
            self.client.publish(topic, payload)
            dg.set_buf(data_package.value, dev_index)
            self.this_operation_index = [hash_id, dev_index]
            # dg.save_history(dev_index, 1)
            return True
        else:
            print('The datagram manager has not connect to the server')
            return False
        pass

    def subscribe_all_topic_to_server(self):
        if self.is_connect:
            for ids in self.index_list:
                try:
                    topic = ids[2]
                except IndexError:
                    return
                self.client.subscribe(topic, 0)
            return True
        else:
            print('The datagram manager has not connect to the server')
            return False
        pass

    def un_subscribe_all_topic_to_server(self):
        if self.is_connect:
            for ids in self.index_list:
                try:
                    topic = ids[2]
                except IndexError:
                    return
                self.client.unsubscribe(topic)
            return True
        else:
            print('The datagram manager has not connect to the server')
            return False
        pass
    ####################################################################################################################
    # Mosquitto callback function

    @staticmethod
    def on_connect(client, obj, flag, rc):
        print("OnConnect, flag = " + str(flag) + " rc = " + str(rc))
        obj.is_connect = True

    @staticmethod
    def on_publish(client, obj, mid):
        print("OnPublish, mid = " + str(mid))
        index = obj.this_operation_index
        if index:
            try:
                # hash_id = index[0]
                # dev_index = index[1]
                dg = obj.get_datagram_by_id(index[0])
                dg.save_history(index[1], 1)
            except IndexError:
                print('Index error')
                pass
            pass

    @staticmethod
    def on_subscribe(client, obj, mid, granted_qos):
        print("Subscribed: mid = " + str(mid) + " qos = " + str(granted_qos))

    @staticmethod
    def on_log(client, obj, level, string):
        print("Log: level = " + str(level) + ' ' + string)

    @staticmethod
    def on_message(client, obj, msg):
        print("Message: topic = [" + msg.topic + "] qos = " + str(msg.qos) + " message = [" + str(msg.payload) + "]")
        try:
            payload = cbor.loads(msg.payload)
            package = MqttMessagePackage(payload)
            hash_id = package.hash_id
            device_index = package.device_instance_index - 1
            dg = obj.get_datagram_by_id(hash_id)
            dg.set_value(package.value, device_index)
            dg.save_history(device_index, 0)
        except TypeError:
            print('Message format error')
            return
            pass

        if obj.update_data_callback:
            obj.update_data_callback(obj.user_data, package)

    @staticmethod
    def on_disconnect(client, obj, rc):
        print("Disconnect: rc = " + str(rc))
        obj.client = None
        obj.is_connect = False
        pass

if __name__ == "__main__":
    manager = DatagramManager()
    manager.import_csv('../datadictionarysource/default_data_dictionary.csv')
    manager.connect_data_server()
    print('OK')
    manager.disconnect_data_server()
    print('OK')
    test = b'\xa9\x00\x00\x01\x00\x02\x1a`\x16\x06\xd9\x03\x00\x04\x00\x05\x00\x06\x00\x07\x01\n\xf6'
    a = cbor.loads(test)
    print('OK')
