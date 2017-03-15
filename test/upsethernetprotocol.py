import socketserver
try:
    from collections import OrderedDict as _OrderedDict
except SystemError:
    _OrderedDict = None
from queue import Queue, Empty
import threading
import socket


class UpsEthernetProtocolCRC16:
    __crc16_table = (
        0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
        0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
        0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
        0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
        0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
        0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
        0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
        0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
        0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
        0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
        0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
        0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
        0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
        0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
        0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
        0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
        0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
        0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
        0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
        0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
        0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
        0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
        0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
        0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
        0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
        0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
        0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
        0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
        0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
        0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
        0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
        0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
    )

    def __init__(self, init_value=0):
        self.__init_value = init_value

    def calculate_crc16_for_bytes(self, data_bytes, length=None):
        if isinstance(data_bytes, bytes) or isinstance(data_bytes, bytearray):
            last_crc16_value = self.__init_value
            _len = length if isinstance(length, int) else len(data_bytes)
            for i in range(_len):
                try:
                    last_crc16_value = self.__continue_calculate_for_byte(data_bytes[i], last_crc16_value)
                except IndexError:
                    break

            return last_crc16_value
            pass
        else:
            raise ValueError('Input value must be bytes or bytearray')
        pass

    def __continue_calculate_for_byte(self, value_byte, last_crc16_value):
        return ((last_crc16_value << 8) ^ self.__crc16_table[((last_crc16_value >> 8) ^ value_byte) & 0xff]) & 0xffff
        pass
    pass


class UpsEthernetProtocolFrame:
    _fields = ("protocol_id",
               "length",
               "source",
               "priority",
               "message_type",
               "message_id",
               "rolling_counter",
               "data_length_count",
               "data",
               "check_sum")

    def __init__(self):
        self.__protocol_id = 0x00
        self.__length = 0x14
        self.__source = 0x00
        self.__priority = 0x00
        self.__message_type = 0b0
        self.__message_id = 0x12345678
        self.__rolling_counter = 0
        self.__data_length_count = 0
        self.__data = bytearray(8)
        self.__check_sum = 0
        pass

    @property
    def bytes(self):
        ret_bytes = bytearray(self.__length)
        ret_bytes[0] = self.__protocol_id
        ret_bytes[1] = self.__length
        if self.__length == 2:
            return ret_bytes
        ret_bytes[2] = self.__source
        ret_bytes[3] = self.__priority << 6 | self.__message_type
        _tmp = self.__message_id
        for i in range(4):
            ret_bytes[7 - i] = _tmp & 0xff
            _tmp >>= 8

        ret_bytes[8] = self.__rolling_counter
        ret_bytes[9] = self.__data_length_count

        for i in range(self.__length - 12):
            ret_bytes[i + 10] = self.__data[i]
            pass

        ret_bytes[self.__length - 2] = (self.__check_sum & 0xff00) >> 8
        ret_bytes[self.__length - 1] = self.__check_sum & 0xff
        return bytes(ret_bytes)
        pass

    @bytes.setter
    def bytes(self, value):
        if isinstance(value, bytearray) or isinstance(value, bytes):
            _len = len(value)
            if _len < 2:
                raise ValueError('The minimal bytes length must be 2, input value={}(len={})'.format(value, _len))
            elif (_len > 2) and (_len < 20):
                raise ValueError('The bytes length range is (2 or 20 ~ 62), input value={}(len={})'.format(value, _len))
            self.__length = _len

            self.__protocol_id = value[0]
            _len = value[1]

            if self.__length != value[1]:
                print('WARNING:', 'Frame length({}) and the length({}) get by parser are mismatch'.format(self.__length,
                                                                                                          _len))
                if (_len == 2) or ((_len > 19) and (_len < 63)):
                    if self.__length > _len:
                        print('WARNING:', 'Some data({}) of the input bytes will be discarded'.format(value[_len:]))
                        self.__length = _len
                    else:
                        print('WARNING:', 'The length in the frame be set as {}(bytes length)'.format(self.__length))
                    pass
                else:
                    raise ValueError(
                        'The length({}) get by parser is invalid, it must be in the range 20 ~ 62 or =2'.format(value))
            if self.__length == 2:
                return
            self.__source = value[2]
            self.__priority = (value[3] >> 6) & 0b11
            self.__message_type = value[3] & 0b111111
            self.__message_id = value[4] << 24 | value[5] << 16 | value[6] << 8 | value[7]
            self.__rolling_counter = value[8]
            self.__data_length_count = value[9]

            if self.__data_length_count > 50:
                raise ValueError(
                    'The data length must be in the range 0 ~ 50, input length={}'.format(self.__data_length_count))
            if self.__data_length_count < 8:
                if self.__length > 20:
                    print('WARNING:',
                          'Data length count({}) and frame length({}) are mismatch,'
                          ' so set data length count as {}'.format(self.__data_length_count,
                                                                   self.__length,
                                                                   self.__length - 12))
                    self.__data_length_count = self.__length - 12
                    self.__data = bytearray(self.__data_length_count)
                else:
                    self.__data = bytearray(8)
            else:
                self.__data = bytearray(self.__data_length_count)

            for i in range(self.__data_length_count):
                self.__data[i] = value[10 + i]

            self.__check_sum = value[self.__length - 2] << 8 | value[self.__length - 1]
            pass
        else:
            raise ValueError('Bytes must be bytearray or bytes type, input value={}({})'.format(value, type(value)))
            pass
        pass

    @property
    def protocol_id(self):
        return self.__protocol_id

    @protocol_id.setter
    def protocol_id(self, value):
        if isinstance(value, int):
            if value == 0:
                self.__length = 2
            elif (value > 255) or (value < 0):
                raise ValueError('Protocol ID is limited from 0 to 255, input value={}'.format(value))
            self.__protocol_id = value
        else:
            raise ValueError('Protocol ID must be int type, input value={}({})'.format(value, type(value)))
        pass

    @property
    def length(self):
        return self.__length

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        if isinstance(value, int):
            if (value > 255) or (value < 0):
                raise ValueError('Source is limited from 0 to 255, input value={}'.format(value))
            self.__source = value
        else:
            raise ValueError('Source must be int type, input value={}({})'.format(value, type(value)))
        pass

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        if isinstance(value, int):
            if (value > 0b11) or (value < 0):
                raise ValueError('Priority is limited from 0 to {}, input value={}'.format(0b11, value))
            self.__priority = value
        else:
            raise ValueError('Priority must be int type, input value={}({})'.format(value, type(value)))
        pass

    @property
    def message_type(self):
        return self.__message_type

    @message_type.setter
    def message_type(self, value):
        if isinstance(value, int):
            if (value > 0b111111) or (value < 0):
                raise ValueError('Message type is limited from 0 to {}, input value={}'.format(0b111111, value))
            self.__message_type = value
        else:
            raise ValueError('Message type must be int type, input value={}({})'.format(value, type(value)))
        pass

    @property
    def message_id(self):
        return self.__message_id

    @message_id.setter
    def message_id(self, value):
        if isinstance(value, int):
            if (value > 0xffffffff) or (value < 0):
                raise ValueError('Message ID is limited from 0 to {}, input value={}'.format(0xffffffff, value))
            self.__message_id = value
        else:
            raise ValueError('Message ID must be int type, input value={}({})'.format(value, type(value)))
        pass

    @property
    def rolling_counter(self):
        return self.__rolling_counter
        pass

    @rolling_counter.setter
    def rolling_counter(self, value):
        if isinstance(value, int):
            if (value > 0xff) or (value < 0):
                raise ValueError('Rolling counter is limited from 0 to {}, input value={}'.format(0xff, value))
            self.__rolling_counter = value
        else:
            raise ValueError('Rolling counter must be int type, input value={}({})'.format(value, type(value)))
        pass

    @property
    def data_length_count(self):
        return self.__data_length_count

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        if isinstance(value, bytearray) or isinstance(value, bytes):
            _len = len(value)
            if _len > 50:
                _len = 50
                value = value[:50]
            self.__data_length_count = _len
            if self.__data_length_count > 8:
                self.__data = bytearray(self.__data_length_count)
                self.__length = self.__data_length_count + 12
                pass
            else:
                self.__length = 20
                self.__data = bytearray(8)
            for i in range(self.__data_length_count):
                self.__data[i] = value[i]
            pass
        else:
            raise ValueError('Data must be bytearray or bytes type, input value={}({})'.format(value, type(value)))
            pass
        pass

    def set_data(self, data_bytes, length=None):
        if isinstance(data_bytes, bytearray) or isinstance(data_bytes, bytes):
            _len = len(data_bytes)
            if _len > 50:
                _len = 50
                data_bytes = data_bytes[:50]

            if isinstance(length, int):
                if (length >= 0) and (length < 50):
                    _len = length
                else:
                    raise ValueError(
                        'The data length must be in the range 0 ~ 50, input length={}'.format(_len))

            self.__data_length_count = _len
            if self.__data_length_count > 8:
                self.__data = bytearray(self.__data_length_count)
                self.__length = self.__data_length_count + 12
                pass
            else:
                self.__length = 20
                self.__data = bytearray(8)
            for i in range(self.__data_length_count):
                try:
                    self.__data[i] = data_bytes[i]
                except IndexError:
                    break
            pass
        else:
            raise ValueError('Data must be bytearray or bytes type, input value={}({})'.format(bytes, type(bytes)))
            pass
        pass

    @property
    def check_sum(self):
        return self.__check_sum
        pass

    @check_sum.setter
    def check_sum(self, value):
        if isinstance(value, int):
            if (value > 0xffff) or (value < 0):
                raise ValueError('Check sum is limited from 0 to {}, input value={}'.format(0xffff, value))
            self.__check_sum = value
        else:
            raise ValueError('Check sum must be int type, input value={}({})'.format(value, type(value)))
        pass

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__,
                                 ', '.join('{0}={1!r}'.format(name, getattr(self, name)) for name in self._fields))
        pass

    def __dict__(self):
        # In 2.6, return a dict.
        # Otherwise, return an OrderedDict
        t = _OrderedDict if _OrderedDict is not None else dict
        return t(zip(self._fields, self))
        pass

    def __iter__(self):
        return (getattr(self, field_name) for field_name in self._fields)

    def __getitem__(self, item):
        if isinstance(item, str):
            try:
                return getattr(self, item)
            except AttributeError:
                raise KeyError('{} is invalid key'.format(item))
        elif isinstance(item, int):
            try:
                return getattr(self, self._fields[item])
            except IndexError:
                raise IndexError('{} is out of the index range({})'.format(item, len(self._fields)))
        else:
            raise KeyError('{}'.format(item))
        pass
    pass


class BasicFrameFilter:
    def __init__(self):
        pass

    def compare(self, input_frame):
        return True
        pass

    pass


class MessageIdFrameFilter(BasicFrameFilter):
    def __init__(self, message_id):
        self.__message_id = message_id
        super(MessageIdFrameFilter, self).__init__()
        pass

    def compare(self, input_frame):
        return input_frame.message_id == self.__message_id
        pass

    pass


class UdpMessageHandler(socketserver.BaseRequestHandler):
    message_queue = None
    frame_filter = BasicFrameFilter()
    lock_set_frame_filter = threading.Lock()

    def handle(self):
        data = self.request[0]
        try:
            frame = UpsEthernetProtocolFrame()
            frame.bytes = data
            self.lock_set_frame_filter.acquire()
            if isinstance(self.message_queue, Queue) and self.frame_filter.compare(frame):
                self.message_queue.put(frame)
            self.lock_set_frame_filter.release()
            print('Received:', frame)
        except ValueError:
            print('Received:', 'Invalid frame({})'.format(', '.join('{:02X}'.format(byte) for byte in data)))

        pass
    pass


class ThreadedUdpServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class UpsEthernetProtocol:

    def __init__(self, remote='localhost', remote_port=8080, local_port=8081):
        self.__remote = remote
        self.__remote_port = remote_port
        self.__local_port = local_port
        self.__local = socket.gethostname()
        self.__frame_queue = Queue()
        UdpMessageHandler.message_queue = self.__frame_queue
        self.__udp_server = ThreadedUdpServer((self.__local, self.__local_port), UdpMessageHandler)
        self.__udp_server_thread = None
        self.__udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__crc16_calculator = UpsEthernetProtocolCRC16()
        self.__rolling_counter = 0
        pass

    def start_server(self):
        self.__udp_server_thread = threading.Thread(target=self.__udp_server.serve_forever)
        self.__udp_server_thread.daemon = True
        self.__rolling_counter = 0
        self.__udp_server_thread.start()
        pass

    def stop_server(self):
        self.__udp_server.shutdown()
        self.__udp_server.server_close()
        pass

    @staticmethod
    def set_frame_filter(frame_filter):
        if isinstance(frame_filter, BasicFrameFilter):
            UdpMessageHandler.lock_set_frame_filter.acquire()
            UdpMessageHandler.frame_filter = frame_filter
            UdpMessageHandler.lock_set_frame_filter.release()
            pass
        else:
            raise ValueError('{} is invalid frame filter'.format(frame_filter))
        pass

    def read_frame(self, timeout=None):
        try:
            _frame = self.__frame_queue.get(timeout=timeout)
            if _frame.message_type & 0b000100 != 0:
                _crc16 = self.__crc16_calculator.calculate_crc16_for_bytes(_frame.bytes, _frame.length - 2)
                if _crc16 != _frame.check_sum:
                    print('ERROR:', 'CRC 16 check failed (in frame={:04X}, calculate={:04X})'.format(_frame.check_sum,
                                                                                                     _crc16))
                    return None
            return _frame
        except Empty:
            return None
        pass

    def send_frame_bytes(self, frame_bytes):
        self.__udp_socket.sendto(frame_bytes, (self.__remote, self.__remote_port))
        pass

    def send_frame(self, frame, rolling_counter=None):
        if not isinstance(frame, UpsEthernetProtocolFrame):
            raise ValueError('{} is invalid frame'.format(frame))
        self.__rolling_counter =\
            rolling_counter & 0xff if isinstance(rolling_counter, int) else self.__rolling_counter + 1
        frame.rolling_counter = self.__rolling_counter
        if frame.message_type & 0b000100 != 0:
            frame.check_sum = self.__crc16_calculator.calculate_crc16_for_bytes(frame.bytes, frame.length - 2)
        self.send_frame_bytes(frame.bytes)
        print('Send:', frame)
        return frame
        pass
    pass


# ======================================================================================================================
# Demo code
# ----------------------------------------------------------------------------------------------------------------------


def __demo_task(host, port, cmd_line_queue, cmd_line_processed):
    _ups_ethernet_protocol = UpsEthernetProtocol(host, port)
    _ups_ethernet_protocol.set_frame_filter(MessageIdFrameFilter(message_id=0x00000001))
    _ups_ethernet_protocol.start_server()

    while True:
        _frame = _ups_ethernet_protocol.read_frame(5)
        if _frame:
            print('I have received a valid frame({})'.format(_frame))
        else:
            print('I have received a invalid frame or not have received any frame with timeout')

        try:
            cmd_line = cmd_line_queue.get(timeout=0.1)
            if isinstance(cmd_line, str):
                if cmd_line.rstrip().upper() == 'STOP':
                    _ups_ethernet_protocol.stop_server()
                    cmd_line_processed.set()
                    return
                elif cmd_line.rstrip().upper() == 'SEND':
                    _frame = UpsEthernetProtocolFrame()
                    _frame.protocol_id = 0x0f
                    _frame.source = 0x3f
                    _frame.priority = 0b1
                    _frame.message_type = 0b111
                    _frame.message_id = 0x00000002
                    # _frame.data = b'1234567'
                    _frame.set_data(b'ABC_DEF_HIJ_KLM', 20)
                    _ups_ethernet_protocol.send_frame(_frame)
                    pass
                else:
                    cmd_line_args = cmd_line.split(' ')
                    if len(cmd_line_args) >= 2:
                        if cmd_line_args[0].strip().upper() == 'FID':
                            _id = int(cmd_line_args[1].strip())
                            _ups_ethernet_protocol.set_frame_filter(MessageIdFrameFilter(_id))
                    pass

            cmd_line_processed.set()
        except Empty:
            pass
    pass


def demo(host, port):
    import sys
    _cmd_line_queue = Queue()
    _cmd_line_processed = threading.Event()
    _demo_sub_thread = threading.Thread(target=__demo_task,
                                        args=(host, port, _cmd_line_queue, _cmd_line_processed))
    _demo_sub_thread.start()
    while True:
        line = sys.stdin.readline()
        _cmd_line_processed.clear()
        _cmd_line_queue.put(line)
        while not _cmd_line_processed.isSet():
            pass
        if not _demo_sub_thread.isAlive():
            break
    pass

if __name__ == '__main__':
    demo('192.168.56.1', 50667)
    pass
