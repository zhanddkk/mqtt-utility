import csv
import cbor
import ctypes
import threading
from namedlist import namedlist as named_list
try:
    from .ddmanager import DataDictionaryManager
    from .dgattribute import DatagramAttribute
    from .dg import Datagram
    from .dgpayload import DatagramPayload
    from .dgpayload import E_DATAGRAM_ACTION_PUBLISH as _E_DATAGRAM_ACTION_PUBLISH
    from .dgpayload import E_DATAGRAM_ACTION_RESPONSE as _E_DATAGRAM_ACTION_RESPONSE
    from .dgpayload import E_DATAGRAM_ACTION_REQUEST as _E_DATAGRAM_ACTION_REQUEST
    from .dgpayload import E_DATAGRAM_ACTION_ALLOW as _E_DATAGRAM_ACTION_ALLOW
    from .dgaccessclient import DatagramAccessClient
    from .bitmapparser import BitMapParser, command_bit_map
except SystemError:
    from ddmanager import DataDictionaryManager
    from dgattribute import DatagramAttribute
    from dg import Datagram
    from dgpayload import DatagramPayload
    from dgpayload import E_DATAGRAM_ACTION_PUBLISH as _E_DATAGRAM_ACTION_PUBLISH
    from dgpayload import E_DATAGRAM_ACTION_RESPONSE as _E_DATAGRAM_ACTION_RESPONSE
    from dgpayload import E_DATAGRAM_ACTION_REQUEST as _E_DATAGRAM_ACTION_REQUEST
    from dgpayload import E_DATAGRAM_ACTION_ALLOW as _E_DATAGRAM_ACTION_ALLOW
    from dgaccessclient import DatagramAccessClient
    from bitmapparser import BitMapParser, command_bit_map

message_format_class = named_list('MessageFormat', 'topic, qos, retain, is_valid, payload')


class DatagramManager:
    def __init__(self, user_data=None):
        self.__datagram_dict = {}
        self.__datagram_indexes = []
        self.__datagram_access_client = None
        self.__data_dictionary_manager = DataDictionaryManager()
        self.__seq_num = 0
        self.__user_data = user_data
        self.__msg_observers = dict()
        self.__msg_observers_lock = threading.Lock()
        pass

    @property
    def sequence_number(self):
        return self.__seq_num

    @sequence_number.setter
    def sequence_number(self, value):
        try:
            self.__seq_num = ctypes.c_uint16(value).value
        except TypeError as exception:
            print('ERROR:', exception)

    @property
    def datagram_indexes(self):
        return self.__datagram_indexes

    @property
    def datagram_dictionary(self):
        return self.__datagram_dict

    @property
    def data_dictionary_version(self):
        return self.__data_dictionary_manager.ver

    @property
    def product_information(self):
        return self.__data_dictionary_manager.product_info

    @property
    def datagram_access_client(self):
        return self.__datagram_access_client

    def import_data_dictionary(self, file_name):
        datagram_dict = {}
        datagram_indexes = []
        data_dictionary_manager = self.__data_dictionary_manager
        try:
            with open(file_name, newline='') as csv_file:
                reader = csv.reader(csv_file, dialect='excel')
                try:
                    if data_dictionary_manager.get_version_info(reader) is False:
                        return False
                    if data_dictionary_manager.get_product_info(reader) is False:
                        return False
                    if data_dictionary_manager.get_header_info(reader) is False:
                        return False
                    for record in map(data_dictionary_manager.make, reader):
                        data_dictionary_item = data_dictionary_manager.interface.get_data_dictionary_item(record)
                        if data_dictionary_item is None:
                            print('ERROR:', 'Parse failed in line', reader.line_num)
                            continue
                        datagram = Datagram(DatagramAttribute(data_dictionary_item))
                        hash_id = data_dictionary_item.hash_id
                        datagram_dict[hash_id] = datagram
                        for instance in range(datagram.device_number):
                            datagram_indexes.append((hash_id, instance))
                    pass
                except csv.Error as exception:
                    print('ERROR:', 'Parse failed in line', reader.line_num, exception)
                    return False
        except FileNotFoundError as exception:
            print('ERROR:', exception)
            return False
        if datagram_indexes and datagram_dict:
            self.__datagram_indexes = datagram_indexes
            self.__datagram_dict = datagram_dict
        else:
            print('ERROR:', 'Import failed.')
            return False
        return True
        pass

    def get_datagram(self, hash_id):
        try:
            return self.__datagram_dict[hash_id]
        except KeyError:
            print('ERROR:', 'Can not find any datagram by hash id:', '0x{0:>08X}'.format(hash_id))
            return None

    def is_valid_datagram(self, hash_id, instance=0, action=_E_DATAGRAM_ACTION_PUBLISH):
        try:
            dg = self.__datagram_dict[hash_id]
            return dg.is_valid_device(instance, action)
        except KeyError:
            return False
        pass

    def init_datagram_access_client(self, name='', ip='localhost', port=1883):
        if self.__datagram_access_client is None:
            self.__datagram_access_client = DatagramAccessClient(name, self)
            self.__datagram_access_client.config(ip, port)
        else:
            print('WARNING:', 'The datagram access client already be initialized.')
        pass

    def delete_datagram_access_client(self):
        if self.__datagram_access_client is None:
            return
        if self.__datagram_access_client.is_running is True:
            self.__datagram_access_client.stop()
            self.__datagram_access_client = None
        pass

    def get_client(self):
        return self.__datagram_access_client

    def register_msg_observer(self, observer):
        self.__msg_observers_lock.acquire()
        self.__msg_observers[observer.identification] = observer
        self.__msg_observers_lock.release()
        pass

    def un_register_msg_observer(self, identification):
        self.__msg_observers_lock.acquire()
        try:
            self.__msg_observers.pop(identification)
        except KeyError:
            print('ERROR:', identification, 'is invalid identification')
            pass
        self.__msg_observers_lock.release()
        pass

    def record_message(self, msg):
        is_valid = False
        try:
            package = cbor.loads(msg.payload)
            is_valid = True
        except Exception as exception:
            print('ERROR:', 'The message received format is not cbor format,', exception)
            package = msg.payload

        if is_valid:
            payload = DatagramPayload()
            is_valid = payload.set_package(package)
            if is_valid:
                self.received_payload(msg.topic, payload)
            else:
                payload = package
        else:
            payload = package
        message = message_format_class(topic=msg.topic,
                                       qos=msg.qos,
                                       retain=msg.retain,
                                       is_valid=is_valid,
                                       payload=payload)
        if self.__user_data is not None:
            try:
                self.__user_data.record_message(message)
            except AttributeError:
                pass

        self.__msg_observers_lock.acquire()
        for observer in self.__msg_observers.values():
            if observer.on_msg_received(message):
                observer.do_msg_received(message)
        self.__msg_observers_lock.release()
        pass

    def received_payload(self, topic, payload):
        dg = self.get_datagram(getattr(payload, 'hash_id'))
        if dg is None:
            return
        dg.update_device_data_value_by_payload(topic, payload)
        if self.__user_data is not None:
            try:
                self.__user_data.received_payload(topic, payload)
                pass
            except AttributeError:
                pass
        pass

    def send_package_by_payload(self, payload, topic=None, qos=0, retain=None):
        if self.__datagram_access_client is None:
            print('ERROR:', 'No datagram server.')
            return False
        if topic is None:
            hash_id = payload.hash_id
            dg = self.get_datagram(hash_id)
            if dg is None:
                print('ERROR:', 'No topic')
                return False
            instance = payload.device_instance_index - 1
            dev_data = dg.get_device_data(instance)
            if dev_data is None:
                print('ERROR:', 'No topic')
                return False
            topic = dev_data.get_topic(payload.action)
            if topic is None:
                print('ERROR:', 'No topic')
                return False
        else:
            hash_id = payload.hash_id
            dg = self.get_datagram(hash_id)
            if dg is not None:
                instance = payload.device_instance_index - 1
                dev_data = dg.get_device_data(instance)
                if dev_data is not None:
                    topic_tmp = dev_data.get_topic(payload.action)
                    if topic_tmp is not None:
                        if topic != topic_tmp:
                            print('WARNING:', 'Input topic and defined topic in datagram do not match. Input =',
                                  topic + ',', 'Defined = ', topic_tmp)
        if retain is None:
            retain = True
            if dg.attribute.type == 'Command':
                if payload.action == _E_DATAGRAM_ACTION_PUBLISH or payload.action == _E_DATAGRAM_ACTION_RESPONSE:
                    retain = False
            elif dg.attribute.type == 'Setting':
                if payload.action == _E_DATAGRAM_ACTION_REQUEST or payload.action == _E_DATAGRAM_ACTION_RESPONSE:
                    retain = False
            else:
                pass
        if self.__datagram_access_client.publish(payload.get_package(), topic, qos, retain) is True:
            if dg is not None:
                if dg.set_device_data_value_by_payload(payload) is False:
                    print('WARNING:', 'The data is set failed.')
                if (dg.attribute.type == 'Command') and payload.action == _E_DATAGRAM_ACTION_PUBLISH:
                    try:
                        sequence = BitMapParser(command_bit_map).decode(payload.value).sequence
                        if sequence.value != self.__seq_num:
                            self.__seq_num = sequence.value
                    except TypeError:
                        print('WARNING:',
                              'The published value({value}) '
                              'type of the command datagram shall be UInt32'.format(value=payload.value))
                    self.__seq_num = self.__seq_num + 1 if self.__seq_num < 65535 else 0
            return True
            pass
        else:
            return False
            pass
        pass

    pass


def demo_code(file_name='default_data_dictionary.csv'):
    dgm = DatagramManager()
    if dgm.import_data_dictionary(file_name) is False:
        return False
    print('Import data dictionary OK')
    dgm.init_datagram_access_client('demo_code')
    dgm.datagram_access_client.start()
    while dgm.datagram_access_client.is_running is False:
        pass
    print('Server is running')
    try:
        from .repeater import repeater_parameter, Repeater, default_user_input_str
    except SystemError:
        from repeater import repeater_parameter, Repeater, default_user_input_str
    rpt = Repeater(dgm)
    resource = repeater_parameter(tagger_count=10,
                                  repeat_times_count=10,
                                  user_input_str=default_user_input_str)
    payload = DatagramPayload()
    payload.value = 10
    rpt.set_default_payload_package(payload.package)

    payload.hash_id = 0x6FEEF2A6
    rpt.append_repeater_item(payload.hash_id, 0, 0, resource)
    payload.hash_id = 0x2D0F0D2
    rpt.append_repeater_item(payload.hash_id, 0, 0, resource)

    print('OK')
    pass

if __name__ == "__main__":
    demo_code()
    pass
