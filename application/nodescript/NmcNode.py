import os as _os
import sqlite3
from DatagramId import *
from HardwareBasicNode import HardwareBasicNode
from ddclient.dgmsgobserver import DatagramMessageObserver
from ddclient.dgpayload import DatagramPayload
from queue import Queue
import threading
from namedlist import namedlist
import argparse
_here = _os.path.abspath(_os.path.dirname(__file__))

dd_file_name = '{}../../dd_source/default_data_dictionary.csv'.format(_here)


_event_db_structure_type = namedlist('EventDbStructureType', (
    "id",
    "slot_id",
    "event_number",
    "event_code",
    "main_group_id",
    "sub_group_id",
    "index_sub_group_id",
    "text_reference_id",
    "hash_id",
    "device_instance_type_id",
    "device_instance_id",
    "log_seconds",
    "log_milliseconds",
    "trigger_seconds",
    "trigger_milliseconds",
    "risky_log",
    "customer_log",
    "service_log",
    "nmc_log",
    "object_id",
    "severity",
    "bookmark_id",
    "data_value",
    "rd_information"))


class NmcEventLogProcessor(DatagramMessageObserver):

    __event_db_structure = _event_db_structure_type(
        id='INTEGER PRIMARY KEY AUTOINCREMENT',
        slot_id='INTEGER',
        event_number='INTEGER',
        event_code='INTEGER',
        main_group_id='INTEGER',
        sub_group_id='INTEGER',
        index_sub_group_id='INTEGER',
        text_reference_id='INTEGER',
        hash_id='INTEGER',
        device_instance_type_id='INTEGER',
        device_instance_id='INTEGER',
        log_seconds='INTEGER',
        log_milliseconds='INTEGER',
        trigger_seconds='INTEGER',
        trigger_milliseconds='INTEGER',
        risky_log='BOOLEAN',
        customer_log='BOOLEAN',
        service_log='BOOLEAN',
        nmc_log='BOOLEAN',
        object_id='INTEGER',
        severity='INTEGER',
        bookmark_id='INTEGER',
        data_value='INTEGER',
        rd_information='TEXT')

    __event_db_default_value = _event_db_structure_type(
        id=0,
        slot_id=0,
        event_number=0,
        event_code=0,
        main_group_id=0,
        sub_group_id=0,
        index_sub_group_id=0,
        text_reference_id=0,
        hash_id=0,
        device_instance_type_id=0,
        device_instance_id=0,
        log_seconds=0,
        log_milliseconds=0,
        trigger_seconds=0,
        trigger_milliseconds=0,
        risky_log=0,
        customer_log=0,
        service_log=0,
        nmc_log=0,
        object_id=0,
        severity=0,
        bookmark_id=0,
        data_value=0,
        rd_information='TEXT'
    )

    __event_structure_map = {
        "eventID": "event_code",
        "mainGroupID": "main_group_id",
        "subgroupID": "sub_group_id",
        "indexSubgroup": "index_sub_group_id",
        "hashID": "hash_id",
        "sourceDeviceType": "device_instance_type_id",
        "deviceInstance": "device_instance_id",
        "trgTmScd": "trigger_seconds",
        "trgTmMs": "trigger_milliseconds",
        "bRiskyLog": "risky_log",
        "bCustomerLog": "customer_log",
        "bServiceLog": "service_log",
        "bNMCLog": "nmc_log",
        "objectID": "object_id",
        "severity": "severity",
        "dataValue": "data_value",
        "logTmScd": "log_seconds",
        "logTmMs": "log_milliseconds",
        "RDInformation": "rd_information"
    }

    def __init__(self, datagram_manager, db_file_name, db_file_path):
        self.__id = 0x80000000
        self.__parse_types = {
            'BasicType': self.__parse_basic_type,
            'EnumType': self.__parse_enum_type,
            'StringType': self.__parse_string_type,
            'ArrayType': self.__parse_array_type,
            'StructureType': self.__parse_structure_type
        }
        self.__event_msg_queue = Queue()
        super(NmcEventLogProcessor, self).__init__(identification=self.__id, name='NmcEventLogProcess')
        self.__dgm = datagram_manager
        self.__dgm.register_msg_observer(self)

        self.__conn_db = None
        self.__db_file_name = db_file_name
        self.__db_file_path = db_file_path.rstrip('\\').rstrip('/')
        self.__db_cursor = None
        self.__db_current_id = None

        self.__write_db_thread = threading.Thread(target=self.write_db_task)
        self.__write_db_thread.start()

    def __init_db(self):
        self.__conn_db.execute('CREATE TABLE IF NOT EXISTS events ({})'.format(
            ','.join('{} {}'.format(item_name, getattr(self.__event_db_structure, item_name))
                     for item_name in getattr(self.__event_db_structure, '_fields'))))
        self.__conn_db.commit()

        data = self.__conn_db.execute('SELECT id FROM events ORDER BY id DESC LIMIT 0, 1')
        rows = data.fetchall()
        if rows:
            return rows[0][0] + 1
        else:
            return 0
        pass

    def release(self):
        self.__dgm.un_register_msg_observer(self.__id)
        self.__event_msg_queue.put(None)
        pass

    def on_msg_received(self, msg):
        if msg.is_valid:
            _payload = DatagramPayload()
            _payload.set_package(msg.payload)

            if E_SYS_GEN_EVENT_LOG_DATA_TO_NMC == _payload.hash_id:
                return True

            return False
            pass
        else:
            return False
        pass

    def do_msg_received(self, msg):
        self.__event_msg_queue.put(msg.payload.package)

    @staticmethod
    def __parse_string_type(value_type, value):
        if isinstance(value, str):
            if len(value) > value_type.array_count:
                print('WARNING:', 'value len {} is out of the max limit({})'.format(len(value), value_type.array_count))
                return True, value[:value_type.array_count]
            return True, value
        else:
            print('ERROR:', 'value = {} is not the string type'.format(value))
            return False, ''
        pass

    @staticmethod
    def __parse_basic_type(value_type, value):
        c_type = value_type.special_data
        if isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
            return True, c_type(value).value
        else:
            print('ERROR:', 'value = {} is not the basic type({})'.format(value, value_type.type_name))
            return False, c_type(0).value
        pass

    @staticmethod
    def __parse_enum_type(value_type, value):
        if isinstance(value, int):
            _enum_def = value_type.special_data
            for key, item in _enum_def.items():
                if item.value == value:
                    return True, (value, key)
            return True, (value, None)
        else:
            print('ERROR:', 'value = {} is not the enum type(UInt32)'.format(value))
            return True, (0, None)
        pass

    def __parse_array_type(self, value_type, value):
        _value = []
        for i in range(value_type.array_count):
            try:
                _sub_value = value[i]
            except IndexError:
                _sub_value = None
            except TypeError:
                _sub_value = None
            _value.append(self.parse_datagram_value(value_type.special_data, _sub_value))
            pass
        pass

    def __parse_structure_type(self, value_type, value):
        _output_structure_value = namedlist('OutputStructureValueClass', value_type.special_data.keys())(
            *((False, i) for i in value_type.special_data.keys())
        )
        i = 0
        for _sub_item_name, sub_item_value_type in value_type.special_data.items():
            try:
                _sub_value = value[i]
                i += 1
            except IndexError:
                _sub_value = None
            except TypeError:
                _sub_value = None

            setattr(_output_structure_value, _sub_item_name, self.parse_datagram_value(sub_item_value_type, _sub_value))
        return True, _output_structure_value
        pass

    def parse_datagram_value(self, value_type, value):
        try:
            return self.__parse_types[value_type.system_tag](value_type, value)
        except KeyError:
            return False, None
            pass
        pass

    def write_db_task(self):
        _file_name = self.__db_file_path + ('/' if self.__db_file_path else '') + self.__db_file_name
        self.__conn_db = sqlite3.connect(_file_name)
        self.__db_cursor = self.__conn_db.cursor()
        self.__db_current_id = self.__init_db()

        while True:
            msg = self.__event_msg_queue.get(timeout=None)
            if msg:
                _payload = DatagramPayload()
                _payload.set_package(msg)
                _hash_id = _payload.hash_id
                # _dev_index = _payload.device_instance_index
                dg = self.__dgm.get_datagram(_hash_id)

                _value = self.parse_datagram_value(dg.attribute.value_type, _payload.value)
                if _value[0] is False:
                    continue

                event_db_value = _event_db_structure_type(**self.__event_db_default_value.__dict__)
                event_db_value.id = self.__db_current_id
                event_db_value.event_number = self.__db_current_id

                _dg_val = _value[1]
                if isinstance(_dg_val, list):
                    for sub_value in _dg_val:
                        event_db_value.id = self.__db_current_id
                        event_db_value.event_number = self.__db_current_id
                        try:
                            for field_name in getattr(sub_value, '_fields'):
                                try:
                                    _key_name_in_db = self.__event_structure_map[field_name]
                                    setattr(event_db_value,
                                            _key_name_in_db,
                                            getattr(sub_value, field_name[1]))
                                except KeyError:
                                    pass

                            _names = ','.join(name for name in getattr(event_db_value, '_fields'))
                            _values = ','.join('?' for i in range(len(event_db_value)))

                            self.__conn_db.execute('INSERT INTO events ({}) values ({})'.format(_names, _values),
                                                   event_db_value)
                            self.__db_current_id += 1
                            pass
                        except AttributeError:
                            pass
                        pass

                else:
                    event_db_value.id = self.__db_current_id
                    event_db_value.event_number = self.__db_current_id
                    try:
                        for field_name in getattr(_value[1], '_fields'):
                            try:
                                _key_name_in_db = self.__event_structure_map[field_name]
                                setattr(event_db_value,
                                        _key_name_in_db,
                                        getattr(_value[1], field_name)[1])
                            except KeyError:
                                pass
                        _names = ','.join(name for name in getattr(event_db_value, '_fields'))
                        _values = ','.join('?' for i in range(len(event_db_value)))

                        self.__conn_db.execute('INSERT INTO events ({}) values ({})'.format(_names, _values),
                                               event_db_value)
                        self.__db_current_id += 1
                        pass
                    except AttributeError:
                        pass
                    pass
                self.__conn_db.commit()
                pass
            else:
                break
        self.__conn_db.close()
        pass

    pass


class NmcNode(HardwareBasicNode):

    def __init__(self, file_name=dd_file_name, ip='localhost', port=1883, db_file_name='event_log.db', db_file_path=''):
        super(NmcNode, self).__init__(file_name, 'NmcNode', ip, port)
        self.event_log_process = NmcEventLogProcessor(self.dgm, db_file_name, db_file_path)
        pass

    @property
    def node_parameter(self):
        return {
            'heart_beat_hash_id': E_NMC_IDTY_GEN_HEARTBEAT,
            'status_communication_hash_id': E_NMC_STATUS_COMMUNICATION,
            'identity_check_hash_id': E_NMC_IDTY_CMD_IDENTITY_REQUEST,
            'hardware_version': E_NMC_IDTY_GEN_HWVERSION,
            'firmware_version': E_NMC_IDTY_GEN_FWVERSION,
            'model_number': E_NMC_IDTY_GEN_MODEL_NUMBER,
            'serial_number': E_NMC_IDTY_GEN_SERIAL_NUMBER,
            'dd_version': E_NMC_IDTY_GEN_DDVERSION,
            'heart_beat_interval': 0.1
        }
        pass

    pass


def main():
    import sys

    arg_parser = argparse.ArgumentParser(description='Nmc node simulator script')
    arg_parser.add_argument('-D',
                            '--dd',
                            default=dd_file_name,
                            help='datagram data file')
    arg_parser.add_argument('-H',
                            '--host',
                            default='localhost',
                            help='mqtt host to connect to. Defaults to localhost.')
    arg_parser.add_argument('-P',
                            '--port',
                            default='1883',
                            help='network port to connect to. Defaults to 1883.')
    arg_parser.add_argument('--db-filename',
                            default='event_log.db',
                            help='database file name. Defaults is event_log.db.')
    arg_parser.add_argument('--db-path',
                            default='',
                            help='database path. Defaults is current path.')
    arg_parser.add_argument('--boot-sequence',
                            default='on',
                            help='if need to run the boot sequence(on/off), Defaults to on')
    args = arg_parser.parse_args()

    file_name = args.dd
    ip = args.host

    try:
        port = int(args.port, base=10)
    except TypeError:
        port = 1883
    except ValueError:
        port = 1883

    is_need_boot_seq = True if args.boot_sequence == 'on' else False

    db_file_name = args.db_filename
    db_file_path = args.db_path

    node = NmcNode(file_name, ip, port, db_file_name, db_file_path)

    if is_need_boot_seq:
        node.run()

    while True:
        line = sys.stdin.readline()
        if line == 'stop\n':
            if is_need_boot_seq:
                node.stop()
            node.event_log_process.release()
            break
        if (not node.heart_beat.is_running) and is_need_boot_seq:
            break
    pass

if __name__ == '__main__':
    main()
    pass
