import threading
import time
from collections import OrderedDict
from ddclient.dgpayload import DatagramPayload
from ddclient.bitmapparser import BitMapParser, bit_attribute_type

heart_beat_bit_map = OrderedDict(
    (
        ('device_node_magic_number', bit_attribute_type(wide=16, names=None)),
        ('recycle_count', bit_attribute_type(wide=16, names=None)),
    )
)


class HeartBeat(threading.Thread):
    def __init__(self, datagram_manager, hash_id, time_interval_seconds, magic_number, start_count=0):
        super().__init__()
        self._hash_id = hash_id
        self._time_interval = time_interval_seconds
        self._running = True
        self._count = start_count
        self._magic_number = magic_number
        self._datagram_manager = datagram_manager
        self.__heart_beat_parser = BitMapParser(heart_beat_bit_map)

    def run(self):
        while self._running is True:
            self.publish_heart_beat_datagram()
            time.sleep(self._time_interval)

    def stop(self):
        self._running = False

    def publish_heart_beat_datagram(self):
        payload = DatagramPayload(hash_id=self._hash_id, value=self.__heart_beat_parser.encode(
            device_node_magic_number=self._magic_number, recycle_count=self._count))
        self._datagram_manager.send_package_by_payload(payload)
        self._count += 1

    @property
    def is_running(self):
        return self._running


