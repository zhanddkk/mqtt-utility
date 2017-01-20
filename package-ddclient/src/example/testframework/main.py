import unittest
import os as _os
from ddclient.dgpayload import DatagramPayload
from ddclient.dgmanager import DatagramManager
from ddclient.unorderedmsgmatcher import UnorderedMessageMatcher
from ddclient.orderedmsgmatcher import OrderedMessageMatcher
from ddclient.testframework import TestFramework

_here = _os.path.abspath(_os.path.dirname(__file__))


class TestDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._dgm = DatagramManager()
        # Set the broker's ip and port, and the name can be set as any string.
        cls._dgm.init_datagram_access_client(name='TestDemo', ip='localhost', port=1883)
        # Import data dictionary file, the file path can be changed if needed.
        file_path = '{}/doc/dd.csv'.format(_here)
        if not cls._dgm.import_data_dictionary(file_name=file_path):
            raise Exception('Import failed, please check the file path and the content of the file')
        # Connect to the broker
        if cls._dgm.datagram_access_client.start():
            # Wait connecting success.
            while not cls._dgm.datagram_access_client.is_running:
                pass
        else:
            raise Exception('Can\'t start the client')

    @classmethod
    def tearDownClass(cls):
        # Disconnect to the broker
        getattr(cls, '_dgm').delete_datagram_access_client()

    def __init_payload(self):
        self._payload.is_object_reference_package = False
        self._payload.payload_type = 0
        self._payload.payload_version = 0
        self._payload.hash_id = 0xffffffff
        self._payload.producer_mask = 1
        self._payload.action = 0
        self._payload.time_stamp_second = 0xffffffff
        self._payload.time_stamp_ms = 0xffff
        self._payload.device_instance_index = 1
        self._payload.value = None
        pass

    def setUp(self):
        self._payload = DatagramPayload()
        self.__init_payload()
        self.__test_framework = TestFramework()
        # Register the message observer, then the message can be received by test frame
        self._dgm.register_msg_observer(self.__test_framework)

    def tearDown(self):
        # Un register the message observer to free the resource for next test case
        self._dgm.un_register_msg_observer(self.__test_framework.identification)

    def test_one_un_ordered_matcher(self):
        _payload = DatagramPayload()
        _payload.set_package(self._payload.package)

        matcher = UnorderedMessageMatcher()
        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x01
        matcher.add_package(_payload.package)

        # All of payload attributes can be set as your need to receive from the broker
        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x02
        matcher.add_package(_payload.package)

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x03
        matcher.add_package(_payload.package)

        self.__test_framework.first_matcher(matcher)
        # Trigger message
        self._payload.hash_id = 0x49a34eb9

        # The ordered is not matched with the matcher defined
        self._payload.value = 0x02
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x03
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x01
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        # wait the result
        ret = self.__test_framework.wait_verify_result(10)
        self.assertTrue(ret)
        pass

    def test_un_verify_seq_num(self):
        _payload = DatagramPayload()
        _payload.set_package(self._payload.package)

        matcher = OrderedMessageMatcher()

        from ddclient.unverifyseqnumpkgcomparator import UnVerifySeqNumPackageComparator
        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x12000537
        matcher.first_package(_payload.package)  # Add first
        matcher.set_comparator(UnVerifySeqNumPackageComparator())

        self.__test_framework.first_matcher(matcher)

        # Trigger message
        self._payload.hash_id = 0x49a34eb9

        # The value is 0x12ffee37, so the seq number is 0xffee
        self._payload.value = 0x12ffee37
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        # wait the result
        ret = self.__test_framework.wait_verify_result(10)
        self.assertTrue(ret)

        matcher = UnorderedMessageMatcher()

        _payload.hash_id = 0x49a34eb9
        # The value is 0x2e55aafe, so the seq number is 55aa
        _payload.value = 0x2e55aafe
        matcher.add_package(_payload.package)  # Add first
        matcher.set_comparator(UnVerifySeqNumPackageComparator())

        self.__test_framework.first_matcher(matcher)

        # Trigger message
        self._payload.hash_id = 0x49a34eb9

        # The value is 0x2eaa55fe, so the seq number is aa55
        self._payload.value = 0x2eaa55fe
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        # wait the result
        ret = self.__test_framework.wait_verify_result(10)
        self.assertTrue(ret)

        pass

    def test_one_ordered_matcher(self):
        _payload = DatagramPayload()
        _payload.set_package(self._payload.package)

        matcher = OrderedMessageMatcher()
        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x01
        matcher.first_package(_payload.package)   # Add first

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x02
        matcher.then_package(_payload.package)    # Then append

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x03
        matcher.then_package(_payload.package)   # Then append

        self.__test_framework.first_matcher(matcher)
        # Trigger message
        self._payload.hash_id = 0x49a34eb9

        # The ordered is not matched with the matcher defined
        self._payload.value = 0x01
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x02
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x03
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        # wait the result
        ret = self.__test_framework.wait_verify_result(10)
        self.assertTrue(ret)
        pass

    def test_mixed_matcher(self):
        _payload = DatagramPayload()
        _payload.set_package(self._payload.package)
        # --------------------------------------------------------------------------------------------------------------
        # Unordered matcher
        matcher = UnorderedMessageMatcher()
        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x01
        matcher.add_package(_payload.package)  # Add first

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x02
        matcher.add_package(_payload.package)  # Add second

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x03
        matcher.add_package(_payload.package)  # Add third

        self.__test_framework.first_matcher(matcher)  # Add first

        # Ordered matcher
        matcher = OrderedMessageMatcher()
        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x04
        matcher.first_package(_payload.package)  # Add first

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x05
        matcher.then_package(_payload.package)  # Then append

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x06
        matcher.then_package(_payload.package)  # Then append

        self.__test_framework.then_matcher(matcher)   # Append

        # Unordered matcher
        matcher = UnorderedMessageMatcher()
        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x07
        matcher.add_package(_payload.package)  # Add first

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x08
        matcher.add_package(_payload.package)  # Add second

        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x09
        matcher.add_package(_payload.package)  # Add third

        self.__test_framework.then_matcher(matcher)  # Append
        # --------------------------------------------------------------------------------------------------------------

        # Trigger message
        self._payload.hash_id = 0x49a34eb9

        # The ordered is not matched with the matcher defined
        self._payload.value = 0x01
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x03
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x02
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        # Send data as the ordered matcher
        self._payload.value = 0x04
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x05
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x06
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x09
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x07
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        self._payload.value = 0x08
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        # wait the result
        ret = self.__test_framework.wait_verify_result(10)
        self.assertTrue(ret)
        pass

    def test_publish_and_get_dg(self):
        # UPSSystem, ,Command,InverterToStaticBypassCommand,Command for transferring the output from inverter
        # operation to Static Bypass operation,COMMAND,32BUS,1,0, , , ,NA, ,No,Yes,1000,
        # No,No,No,Yes,Yes,Yes,No,No,No,No,0x61C3015B

        # We test the datagram which hash id is 0x61C3015B
        # Device index is 1
        # Action is 0 (publish)
        hash_id = 0x61C3015B
        dg = self._dgm.get_datagram(hash_id)
        self.assertIsNotNone(dg)
        attribute = dg.attribute

        # Get some attributes and verify them
        self.assertEqual(attribute.type, 'Command')
        self.assertEqual(attribute.system_tag, 'BasicType')
        self.assertEqual(attribute.basic_type, 'UInt32')
        self.assertEqual(attribute.hash_id, 0x61C3015B)
        self.assertEqual(attribute.producer, ['HMI', 'Tuner'])

        # Prepare payload
        self._payload.hash_id = hash_id
        from ddclient.dgpayload import E_DATAGRAM_ACTION_PUBLISH, D_NODE_MASK_HMI, D_NODE_MASK_TUNER
        self._payload.producer_mask = D_NODE_MASK_HMI | D_NODE_MASK_TUNER
        self._payload.action = E_DATAGRAM_ACTION_PUBLISH
        self._payload.device_instance_index = 1
        self._payload.value = 0x02000001

        # Publish payload
        ret = self._dgm.send_package_by_payload(self._payload)
        # Verify published result
        self.assertTrue(ret)

        # Verify current value of the datagram
        _value = dg.get_device_data_value(instance=self._payload.device_instance_index - 1,
                                          action=self._payload.action)
        self.assertEqual(_value, self._payload.value)
        pass

    def test_cmd_seq(self):
        _payload = DatagramPayload()
        _payload.set_package(self._payload.package)

        matcher = OrderedMessageMatcher()

        from ddclient.unverifyseqnumpkgcomparator import UnVerifySeqNumPackageComparator
        _payload.hash_id = 0x49a34eb9

        from ddclient.bitmapparser import BitMapParser, command_bit_map
        bit_map = BitMapParser(command_bit_map)
        # Set the published command value of expectation
        _value = bit_map.encode(cmd_code=command_bit_map['cmd_code'].names['Rest'],  # 0
                                producer=command_bit_map['producer'].names['SLC_UPS']  # 1
                                )  # 0x01000000
        self.assertEqual(_value, 0x01000000)

        _payload.value = _value
        matcher.first_package(_payload.package)  # Add first
        matcher.set_comparator(UnVerifySeqNumPackageComparator())

        self.__test_framework.first_matcher(matcher)

        # Trigger message
        self._payload.hash_id = 0x49a34eb9

        # Set the command value to publish
        _value = bit_map.encode(cmd_code=command_bit_map['cmd_code'].names['Rest'],  # 0
                                sequence=5,
                                producer=command_bit_map['producer'].names['SLC_UPS']  # 1
                                )  # 0x01000500
        self.assertEqual(_value, 0x01000500)

        self._payload.value = _value
        ret = self._dgm.send_package_by_payload(self._payload)
        self.assertTrue(ret)

        # wait the result
        ret = self.__test_framework.wait_verify_result(10)
        self.assertTrue(ret)

        _dg = self._dgm.get_datagram(self._payload.hash_id)
        self.assertIsNotNone(_dg)

        # Get the current value of the datagram
        _value = _dg.get_device_data_value(instance=self._payload.device_instance_index - 1,
                                           action=self._payload.action)
        self.assertEqual(_value, 0x01000500)

        # Get the sequence number of the command datagram
        seq_num = BitMapParser(command_bit_map).decode(_value).sequence.value

        # Verify the sequence number
        self.assertEqual(seq_num, 5)

        pass

if __name__ == '__main__':
    unittest.main()
    pass
