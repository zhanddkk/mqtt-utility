import random
# from DatagramId import *
from HeartBeat import HeartBeat
from ddclient.dgpayload import DatagramPayload, E_DATAGRAM_ACTION_RESPONSE
from ddclient.dgmanager import DatagramManager
from ddclient.unorderedmsgmatcher import UnorderedMessageMatcher
from ddclient.unverifyseqnumpkgcomparator import UnVerifySeqNumPackageComparator
from ddclient.testframework import TestFramework
from ddclient.bitmapparser import BitMapParser, command_response_bit_map, command_bit_map

E_DISCONNECTED = 0              # //Device node is disconnected
E_CONNECTED = 1                 # //Device node is connected
E_AUTHENTICATED = 2             # //Device node is authenticated
E_HW_VERSION_CHECK_FAILED = 3   # //Device nod does not pass the HW version check
E_FW_VERSION_CHECK_FAILED = 4   # //Device node does not pass the FW version check
E_AUTHENTICATION_FAILED = 5     # //Device node is not authenticated

cmd_ack_code_names = command_response_bit_map['ack_code'].names
cmd_code_names = command_bit_map['cmd_code'].names


class HardwareBasicNode:
    def __init__(self, dd_file_name, node_name, ip='localhost', port=1883):
        self.dgm = DatagramManager()
        # Set the broker's ip and port, and the name can be set as any string.
        self.dgm.init_datagram_access_client(name=node_name, ip=ip, port=port)
        # Import data dictionary file, the file path can be changed if needed.
        if not self.dgm.import_data_dictionary(file_name=dd_file_name):
            raise Exception('Import failed, please check the file path and the content of the file')
        # Connect to the broker
        if self.dgm.datagram_access_client.start():
            # Wait connecting success.
            while not self.dgm.datagram_access_client.is_running:
                pass
        else:
            raise Exception('Can\'t start the client')

        self.heart_beat = HeartBeat(self.dgm,
                                    self.node_parameter['heart_beat_hash_id'],
                                    self.node_parameter['heart_beat_interval'],
                                    random.randint(1, 100))
        self.test_framework = TestFramework()
        pass

    def run(self):
        self.dgm.register_msg_observer(self.test_framework)

        # step 1, acting as UC/HMI/.../, I boot up and start sending heart beat signals
        self.heart_beat.start()

        # step 2, slc will check the heart beat signal and then set communication status to connected.
        # I will check if the status is set, so prepare the matcher.
        connected_payload = DatagramPayload(hash_id=self.node_parameter['status_communication_hash_id'],
                                            value=E_CONNECTED)
        connected_payload.time_stamp_second = 0
        connected_payload.time_stamp_ms = 0

        matcher = UnorderedMessageMatcher()
        matcher.add_package(connected_payload.package)
        self.test_framework.first_matcher(matcher)

        # step 3, slc send the identity check command, I wil check this command is sent, so prepare the matcher.
        identity_check_command = DatagramPayload(hash_id=self.node_parameter['identity_check_hash_id'],
                                                 value=BitMapParser(command_bit_map).encode(
                                                     cmd_code=cmd_code_names['Rest'],
                                                     sequence=0,
                                                     producer=command_response_bit_map['producer'].names['SLC_UPS']))
        identity_check_command.time_stamp_second = 0
        identity_check_command.time_stamp_ms = 0

        matcher = UnorderedMessageMatcher()
        matcher.add_package(identity_check_command.package)
        matcher.set_comparator(UnVerifySeqNumPackageComparator())
        self.test_framework.then_matcher(matcher)

        # Check data
        if self.test_framework.wait_verify_result(5) is False:
            self.stop()
            raise Exception('Boot up failed')

        # step 4, I reply with received ack
        cmd_resp_payload = self.get_command_response_payload(self.node_parameter['identity_check_hash_id'],
                                                             cmd_ack_code_names['Received'])
        self.dgm.send_package_by_payload(cmd_resp_payload)

        # step 5. I reply hw/fw version./module number/serial number/....
        hw_version_payload = DatagramPayload(hash_id=self.node_parameter['hardware_version'],
                                             value="0.1.2.3")
        fw_version_payload = DatagramPayload(hash_id=self.node_parameter['firmware_version'],
                                             value="1.2.3.4")
        model_number_payload = DatagramPayload(hash_id=self.node_parameter['model_number'],
                                               value="1234")
        serial_number_payload = DatagramPayload(hash_id=self.node_parameter['serial_number'],
                                                value="12345656")
        dd_version_payload = DatagramPayload(hash_id=self.node_parameter['dd_version'],
                                             value="0.11.1.4")
        self.dgm.send_package_by_payload(hw_version_payload)
        self.dgm.send_package_by_payload(fw_version_payload)
        self.dgm.send_package_by_payload(model_number_payload)
        self.dgm.send_package_by_payload(serial_number_payload)
        self.dgm.send_package_by_payload(dd_version_payload)

        # step 6. I reply with command complete ack
        cmd_resp_payload = self.get_command_response_payload(self.node_parameter['identity_check_hash_id'],
                                                             cmd_ack_code_names['Completed'])
        self.dgm.send_package_by_payload(cmd_resp_payload)

        # For UC, setting update check
        try:
            cmd_payload = self.get_command_response_payload(hash_id=self.node_parameter['setting_update_check'],
                                                            ack_code=cmd_ack_code_names['Received'])
            self.dgm.send_package_by_payload(cmd_payload)

            cmd_payload = self.get_command_response_payload(hash_id=self.node_parameter['setting_update_check'],
                                                            ack_code=cmd_ack_code_names['Completed'])
            self.dgm.send_package_by_payload(cmd_payload)

            dd_version_payload = DatagramPayload(hash_id=self.node_parameter['setting_update_decision'],
                                                 value=2)
            self.dgm.send_package_by_payload(dd_version_payload)
        except KeyError:
            pass

        # step 7. slc set communication status to authenticated
        authenticated_payload = DatagramPayload(hash_id=self.node_parameter['status_communication_hash_id'],
                                                value=E_AUTHENTICATED)
        authenticated_payload.time_stamp_second = 0
        authenticated_payload.time_stamp_ms = 0

        matcher = UnorderedMessageMatcher()
        matcher.add_package(authenticated_payload.package)
        self.test_framework.first_matcher(matcher)

        if self.test_framework.wait_verify_result(20) is False:
            self.stop()
            raise Exception('Boot up failed')

        print('{Node Connected}\n')

        # while self.heart_beat.is_running:
        #     pass
        pass

    def stop(self):
        self.heart_beat.stop()
        disconnected_payload = DatagramPayload(hash_id=self.node_parameter['status_communication_hash_id'],
                                               value=E_DISCONNECTED)
        disconnected_payload.time_stamp_second = 0
        disconnected_payload.time_stamp_ms = 0

        matcher = UnorderedMessageMatcher()
        matcher.add_package(disconnected_payload.package)
        self.test_framework.then_matcher(matcher)
        ret = self.test_framework.wait_verify_result(10)
        self.dgm.un_register_msg_observer(self.test_framework.identification)
        if ret is False:
            raise Exception('Can not get the disconnected status')
        else:
            print('Node stopped')
        pass

    def get_command_response_payload(self, hash_id, ack_code):
        datagram = self.dgm.get_datagram(hash_id)

        _value = datagram.get_device_data_value(0)

        if not isinstance(_value, int):
            _value = 0

        cmd_bit_map = BitMapParser(command_response_bit_map)

        cmd_bit_map_value = cmd_bit_map.decode(_value)

        _value = cmd_bit_map.encode(ack_code=ack_code,
                                    sequence=cmd_bit_map_value.sequence,
                                    producer=cmd_bit_map_value.producer)

        return DatagramPayload(hash_id=hash_id,
                               value=_value,
                               action=E_DATAGRAM_ACTION_RESPONSE)

    @property
    def node_parameter(self):
        return {'heart_beat_interval': 1.0}
        pass

    pass
