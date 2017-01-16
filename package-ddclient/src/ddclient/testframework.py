import time
from queue import Queue, Empty
try:
    from .dgmsgobserver import DatagramMessageObserver
except SystemError:
    from dgmsgobserver import DatagramMessageObserver


class TestFramework(DatagramMessageObserver):

    def __init__(self):
        super(TestFramework, self).__init__(identification=0, name='TestFramework')
        self.__msg_matcher_list = list()
        self.__queue = Queue()
        pass

    def first_matcher(self, matcher):
        self.__msg_matcher_list = [matcher]
        pass

    def then_matcher(self, matcher):
        self.__msg_matcher_list.append(matcher)
        pass

    def wait_verify_result(self, timeout=1):
        _matcher_index = 0
        if timeout and timeout > 0:
            _timeout = timeout
            _used_time = 0.0
            while True:
                _matcher = self.__msg_matcher_list[_matcher_index]

                _start_time = time.time()
                _timeout = _timeout - _used_time
                if _timeout < 0:
                    _timeout = None

                try:
                    package = self.__queue.get(timeout=_timeout)
                except Empty:
                    print('TIMEOUT:', 'When wait the matcher', _matcher_index)
                    return False
                    pass

                _used_time = time.time() - _start_time

                _matcher.verify(package)
                if _matcher.is_passed:
                    _matcher_index += 1
                    if _matcher_index == len(self.__msg_matcher_list):
                        return True
                        pass
        else:
            return False
            pass
        pass

    def do_msg_received(self, msg):
        self.__queue.put(msg.payload.package)
        pass
    pass
