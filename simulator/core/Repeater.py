import threading
from simulator.core.PayloadPackage import PayloadPackage


class Repeater(threading.Thread):
    _index_list = []    # item = [hash_id, instance],

    def __init__(self, datagram_server, interval, def_package=PayloadPackage()):
        super(Repeater, self).__init__()
        self.datagram_server = datagram_server
        self.interval = interval
        self.lock = threading.Lock()
        self.finished = threading.Event()
        self._def_package = def_package
        self.user_function = None
        self.finish_repeat_callback = None
        self.finish_repeat_data = None
        pass

    def append_data(self, item, def_package=None):
        self.lock.acquire()
        try:
            index = self._index_list.index(item)
            print('WARNING:', item, 'is existed at', index)
            pass
        except ValueError:
            try:
                dg = self.datagram_server.datagram_manager.get_datagram(item[0])
                if dg is None:
                    print('ERROR:', item, 'is error, can\'t find the datagram')
                    return
                d = dg.data_list[item[1]]
                if d.repeater_info.tagger_count < 1:
                    print('ERROR:', 'repeat tagger count should be greater then 1')
                    return
                d.repeater_info.is_running = True
                d.repeater_info.counter = 0
                d.repeater_info.repeat_times = 0
            except IndexError:
                print('ERROR:', item, 'is error, can\'t find the data in the datagram')
                return
            self._index_list.append(item)
            pass
        if def_package is not None:
            self._def_package = def_package
        self.lock.release()
        pass

    def remove_data(self, item):
        self.lock.acquire()
        try:
            self._index_list.remove(item)
            try:
                dg = self.datagram_server.datagram_manager.get_datagram(item[0])
                if dg is None:
                    print('ERROR:', item, 'is error, can\'t find the datagram')
                    return
                d = dg.data_list[item[1]]
                d.repeater_info.is_running = False
                d.repeater_info.counter = 0
                d.repeater_info.repeat_times = 0
            except IndexError:
                print('ERROR:', item, 'is error, can\'t find the data in the datagram')
                return
            pass
        except ValueError:
            print('ERROR:', item, 'is not existed')
            pass
        self.lock.release()
        pass

    def stop(self):
        self.finished.set()
        pass

    def run(self):
        while not self.finished.is_set():
            tmp = self._index_list
            for item in tmp:
                try:
                    dg = self.datagram_server.datagram_manager.get_datagram(item[0])
                    d = dg.data_list[item[1]]
                    repeater_info = d.repeater_info
                    if repeater_info.counter >= repeater_info.tagger_count:
                        self._def_package.hash_id = item[0]
                        self._def_package.device_instance_index = item[1] + 1
                        repeater_info.repeat_times += 1

                        try:
                            exec(repeater_info.user_function_str + '\nself.user_function = user_function')

                            self._def_package.value = self.user_function(d.value, repeater_info.repeat_times)
                        except Exception as exception:
                            print('ERROR:',
                                  'when parse user function of item',
                                  item,
                                  'and run it, exception :',
                                  exception)

                        self.datagram_server.publish(self._def_package)

                        if (repeater_info.exit_times > 0) and (repeater_info.repeat_times >= repeater_info.exit_times):
                            repeater_info.is_running = False
                            repeater_info.repeat_times = 0
                            self._index_list.remove(item)

                        repeater_info.counter = 0
                    else:
                        repeater_info.counter += 1
                    pass
                except IndexError:
                    print('ERROR:', 'Item format or value is error', item)
                    self.stop()
                    pass
                except TypeError:
                    print('ERROR:', 'Item type is error', item)
                    self.stop()
                    pass
                pass
            self.finished.wait(self.interval)
        pass


if __name__ == "__main__":
    pass
