import os as _os
from DatagramId import *
from HardwareBasicNode import HardwareBasicNode

_here = _os.path.abspath(_os.path.dirname(__file__))

dd_file_name = '{}../../dd_source/default_data_dictionary.csv'.format(_here)


class UcNode(HardwareBasicNode):

    def __init__(self, file_name=dd_file_name, ip='localhost', port=1883):
        super(UcNode, self).__init__(file_name, 'HmiNode', ip, port)
        pass

    @property
    def node_parameter(self):
        return {
            'heart_beat_hash_id': E_UC_IDTY_GEN_HEARTBEAT,
            'status_communication_hash_id': E_UC_STATUS_COMMONICATION,
            'identity_check_hash_id': E_UC_IDTY_CMD_IDENTITY_REQUEST,
            'hardware_version': E_UC_IDTY_GEN_HWVERSION,
            'firmware_version': E_UC_IDTY_GEN_FWVERSION,
            'model_number': E_UC_IDTY_GEN_MODEL_NUMBER,
            'serial_number': E_UC_IDTY_GEN_SERIAL_NUMBER,
            'dd_version': E_UC_IDTY_GEN_DDVERSION,
            'setting_update_decision': E_UC_STATUS_UCSETTING_UPDATE_DECISION,
            'setting_update_check': E_UC_CMD_UCSETTING_UPDATE_CHECK,
            'heart_beat_interval': 0.1
        }
        pass

    pass


def main():
    import sys
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = dd_file_name

    try:
        ip = sys.argv[2]
    except IndexError:
        ip = 'localhost'

    try:
        port = int(sys.argv[3], base=10)
    except IndexError:
        port = 1883
    except ValueError:
        port = 1883

    print('Args:', file_name, ip, port)

    node = UcNode(file_name, ip, port)
    node.run()

    while node.heart_beat.is_running:
        line = sys.stdin.readline()
        if line == 'stop\n':
            node.stop()
            break
    pass

if __name__ == '__main__':
    main()
    pass
