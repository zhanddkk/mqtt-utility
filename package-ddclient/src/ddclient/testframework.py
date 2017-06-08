import time
from queue import Queue, Empty
try:
    from .dgmsgobserver import DatagramMessageObserver
    from .msgmatcher import MessageMatcher
except SystemError:
    from dgmsgobserver import DatagramMessageObserver
    from msgmatcher import MessageMatcher


class TestFramework(DatagramMessageObserver):

    def __init__(self):
        super(TestFramework, self).__init__(identification=0, name='TestFramework')
        self.__msg_matcher_list = list()
        self.__queue = Queue()
        pass

    def first_matcher(self, matcher):
        if not isinstance(matcher, MessageMatcher):
            raise TypeError("Matcher should be subclass of MessageMatcher")
        self.__msg_matcher_list = [matcher]

    def then_matcher(self, matcher):
        if not isinstance(matcher, MessageMatcher):
            raise TypeError("Matcher should be subclass of MessageMatcher")
        self.__msg_matcher_list.append(matcher)

    def wait_verify_result(self, timeout=1):
        _matcher_index = 0
        _is_waiting = True
        _ret = False
        if timeout and timeout > 0:
            _timeout = timeout
            _used_time = 0.0
            while _is_waiting:
                _matcher = self.__msg_matcher_list[_matcher_index]

                _start_time = time.time()
                _timeout = _timeout - _used_time
                if _timeout < 0:
                    _is_waiting = False
                    try:
                        package = self.__queue.get_nowait()
                    except Empty:
                        print('TIMEOUT:', 'When wait the matcher', _matcher_index)
                        break
                        pass
                else:
                    try:
                        package = self.__queue.get(timeout=_timeout)
                    except Empty:
                        print('TIMEOUT:', 'When wait the matcher', _matcher_index)
                        break
                        pass

                _used_time = time.time() - _start_time

                _matcher.verify(package)
                if _matcher.is_passed:
                    _matcher_index += 1
                    if _matcher_index == len(self.__msg_matcher_list):
                        _ret = True
                        break
        return _ret

    def clear_message(self):
        _q = self.__queue.queue
        with self.__queue.mutex:
            _q.clear()
        pass

    def do_msg_received(self, msg):
        self.__queue.put(msg.payload.package)
        pass
    pass
