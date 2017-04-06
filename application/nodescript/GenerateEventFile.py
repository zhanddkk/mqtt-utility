import os as _os
import argparse
from queue import Queue, Empty
from ddclient.dgmsgobserver import DatagramMessageObserver
from ddclient.dgmanager import DatagramManager
from ddclient.dgpayload import DatagramPayload, E_DATAGRAM_ACTION_RESPONSE, E_DATAGRAM_ACTION_PUBLISH
from ddclient.bitmapparser import BitMapParser, command_response_bit_map, command_bit_map
_here = _os.path.abspath(_os.path.dirname(__file__))

dd_file_name = '{}../../dd_source/default_data_dictionary.csv'.format(_here)


GENERATE_EVENT_FILE_CMD_HASH_ID = 0x31F3362A
FETCH_EVENT_FILE_CMD_HASH_ID = 0x5776E8DB
EVENT_LOG_QUERY_STATEMENT_HASH_ID = 0x4F7A85E2

INVALID_STATUS = None
GET_GENERATE_EVENT_FILE_CMD = 0
SEND_GENERATE_EVENT_FILE_CMD_RECEIVED_ACK = 1
GET_EVENT_LOG_QUERY_STATEMENT = 2
SEND_GENERATE_EVENT_FILE_CMD_COMPLETED_ACK = 3
GET_FETCH_EVENT_FILE_CMD = 4
GET_FETCH_EVENT_FILE_CMD_COMPLETED_ACK = 5

cmd_ack_code_names = command_response_bit_map['ack_code'].names
cmd_code_names = command_bit_map['cmd_code'].names


class GenerateEventFile(DatagramMessageObserver):
    def __init__(self, ip='localhost', port=1883, _dd_file_name=dd_file_name):
        self.__id = 0x80000001
        super(GenerateEventFile, self).__init__(identification=self.__id, name='GenerateEventFileModule')
        self.dgm = DatagramManager()
        # Set the broker's ip and port, and the name can be set as any string.
        self.dgm.init_datagram_access_client(name='GenerateEventFile', ip=ip, port=port)
        # Import data dictionary file, the file path can be changed if needed.
        if not self.dgm.import_data_dictionary(file_name=_dd_file_name):
            raise Exception('Import failed, please check the file path and the content of the file')
        # Connect to the broker
        if self.dgm.datagram_access_client.start():
            # Wait connecting success.
            while not self.dgm.datagram_access_client.is_running:
                pass
        else:
            raise Exception('Can\'t start the client')

        self.__status = (
            (GENERATE_EVENT_FILE_CMD_HASH_ID, self.__get_generate_event_file_cmd,
             'Status {}: Wait tuner sending a specified command datagram'
             ' (GenerateEventFileCommand) to SLC_UPS for generating event file'),
            (GENERATE_EVENT_FILE_CMD_HASH_ID, self.__send_generate_event_file_cmd_received_ack,
             'Status {}: EventLog module send a received command ACK after it receives this command'),
            (EVENT_LOG_QUERY_STATEMENT_HASH_ID, self.__get_event_log_query_statement,
             'Status {}: Tuner send a general SQL query datagram (EventLogQueryStatement) to SLC_UPS'),
            (GENERATE_EVENT_FILE_CMD_HASH_ID, self.__send_generate_event_file_cmd_completed_ack,
             'Status {}: EventLog send a command completed ACK to Tuner after corresponding file is generated'),
            (FETCH_EVENT_FILE_CMD_HASH_ID, self.__get_fetch_event_file_cmd,
             'Status {}: Wait tuner sending a transfer file finish command(FetchEventFileCommand) to EventLog module'),
            (FETCH_EVENT_FILE_CMD_HASH_ID, self.__send_fetch_event_file_cmd_completed_ack,
             'Status {}: EventLog module sends a complete transfer file finish ACK')
        )
        self.__status_index = GET_GENERATE_EVENT_FILE_CMD
        self.__cmd_payload = None
        self.__event_msg_queue = Queue()
        self.__is_exit = False

        self.dgm.register_msg_observer(self)

    def __get_generate_event_file_cmd(self, payload):
        ret = True
        _value = payload.value
        if isinstance(_value, int) and (payload.action == E_DATAGRAM_ACTION_PUBLISH):
            self.__cmd_payload = payload
            self.__status_index = SEND_GENERATE_EVENT_FILE_CMD_RECEIVED_ACK
            # No need to get the datagram at next status
            ret = False
        return ret
        pass

    def __send_generate_event_file_cmd_received_ack(self, payload):
        _receive_ack_payload = self.get_command_response_payload(hash_id=payload.hash_id,
                                                                 ack_code=cmd_ack_code_names['Received'],
                                                                 cmd_value=self.__cmd_payload.value)
        self.dgm.send_package_by_payload(_receive_ack_payload)
        self.__status_index = GET_EVENT_LOG_QUERY_STATEMENT
        return True
        pass

    def __get_event_log_query_statement(self, payload):
        print('>>Received :\n{}'.format(payload))
        print('>>Query event data base')
        print('>>Create file: {}'.format('tmp.txt'))
        self.__status_index = SEND_GENERATE_EVENT_FILE_CMD_COMPLETED_ACK
        # No need to get the datagram at next status
        return False
        pass

    def __send_generate_event_file_cmd_completed_ack(self, payload):
        _complete_ack_payload = self.get_command_response_payload(hash_id=self.__cmd_payload.hash_id,
                                                                  ack_code=cmd_ack_code_names['Completed'],
                                                                  cmd_value=self.__cmd_payload.value)
        self.dgm.send_package_by_payload(_complete_ack_payload)
        self.__status_index = GET_FETCH_EVENT_FILE_CMD
        return True
        pass

    def __get_fetch_event_file_cmd(self, payload):
        ret = True
        _value = payload.value
        if isinstance(_value, int) and (payload.action == E_DATAGRAM_ACTION_PUBLISH):
            self.__cmd_payload = payload
            print('>>The event file is removed.')
            self.__status_index = GET_FETCH_EVENT_FILE_CMD_COMPLETED_ACK
            # No need to get the datagram at next status
            ret = False
        return ret
        pass

    def __send_fetch_event_file_cmd_completed_ack(self, payload):
        _complete_ack_payload = self.get_command_response_payload(hash_id=payload.hash_id,
                                                                  ack_code=cmd_ack_code_names['Completed'],
                                                                  cmd_value=self.__cmd_payload.value)
        self.dgm.send_package_by_payload(_complete_ack_payload)
        print('----------------Finished----------------')
        self.__status_index = GET_GENERATE_EVENT_FILE_CMD
        return True
        pass

    def get_command_response_payload(self, hash_id, ack_code, cmd_value=None):
        if not isinstance(cmd_value, int):
            datagram = self.dgm.get_datagram(hash_id)

            _value = datagram.get_device_data_value(0)

            if not isinstance(_value, int):
                _value = 0
        else:
            _value = cmd_value

        cmd_bit_map = BitMapParser(command_response_bit_map)

        cmd_bit_map_value = cmd_bit_map.decode(_value)

        _value = cmd_bit_map.encode(ack_code=ack_code,
                                    sequence=cmd_bit_map_value.sequence.value,
                                    producer=cmd_bit_map_value.producer.value)

        return DatagramPayload(hash_id=hash_id,
                               value=_value,
                               action=E_DATAGRAM_ACTION_RESPONSE)

    def run(self):
        self.__is_exit = False
        _is_need_get = True
        _payload = None
        _last_status = INVALID_STATUS
        while not self.__is_exit:
            try:
                if _last_status != self.__status_index:
                    print(self.__status[self.__status_index][2].format(self.__status_index))
                    _last_status = self.__status_index
                if _is_need_get:
                    try:
                        _package = self.__event_msg_queue.get(timeout=0.1)
                        _payload = DatagramPayload()
                        _payload.set_package(_package)
                        pass
                    except Empty:
                        continue
                        pass
                    pass
                else:
                    pass
                _is_need_get = self.__status[self.__status_index][1](_payload)
            except IndexError:
                raise ValueError('Invalid status {}'.format(self.__status_index))
                pass
            pass
        pass

    def stop(self):
        self.__is_exit = True
        pass

    def do_msg_received(self, msg):
        _payload = msg.payload
        try:
            if _payload.hash_id == self.__status[self.__status_index][0]:
                self.__event_msg_queue.put(_payload.package)
                pass
        except IndexError:
            pass
        pass
    pass


def main():
    # import sys

    arg_parser = argparse.ArgumentParser(description='Nmc node simulator script')
    arg_parser.add_argument('-D', '--dd', help='datagram data file')
    arg_parser.add_argument('-H', '--host', help='mqtt host to connect to. Defaults to localhost.')
    arg_parser.add_argument('-P', '--port', help='network port to connect to. Defaults to 1883.')

    args = arg_parser.parse_args()

    file_name = args.dd if args.dd else dd_file_name
    ip = args.host if args.host else 'localhost'

    try:
        port = int(args.port, base=10)
    except TypeError:
        port = 1883
    except ValueError:
        port = 1883

    _generate_event_file = GenerateEventFile(ip=ip, port=port, _dd_file_name=file_name)
    _generate_event_file.run()
    pass

if __name__ == '__main__':
    main()
    pass
