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
        cls._dgm.init_datagram_access_client(name='Test', ip='localhost', port=1883)
        cls._dgm.import_data_dictionary(
            file_name='{}/../../../../doc/datadictionarysource/default_data_dictionary.csv'.format(_here))
        if cls._dgm.datagram_access_client.start():
            while not cls._dgm.datagram_access_client.is_running:
                pass
        else:
            raise Exception

    @classmethod
    def tearDownClass(cls):
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
        self._dgm.register_msg_observer(self.__test_framework)

    def tearDown(self):
        self._dgm.un_register_msg_observer(self.__test_framework.identification)

    def test_one_un_ordered_matcher(self):
        _payload = DatagramPayload()
        _payload.set_package(self._payload.package)

        matcher = UnorderedMessageMatcher()
        _payload.hash_id = 0x49a34eb9
        _payload.value = 0x01
        matcher.add_package(_payload.package)

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

if __name__ == '__main__':
    unittest.main()
    pass
