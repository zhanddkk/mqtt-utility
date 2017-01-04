import threading
import ast as _ast
from namedlist import namedlist as named_list
try:
    from .dgpayload import DatagramPayload
except SystemError:
    from dgpayload import DatagramPayload
repeater_parameter_type = named_list('RepeaterParameter', 'counter,'
                                                          'tagger_count,'
                                                          'repeat_times_counter,'
                                                          'repeat_times_count,'
                                                          'user_input_str,'
                                                          'user_function')


def repeater_parameter(tagger_count, repeat_times_count, user_input_str):
    parameter = repeater_parameter_type(counter=0,
                                        tagger_count=tagger_count,
                                        repeat_times_counter=0,
                                        repeat_times_count=repeat_times_count,
                                        user_input_str=user_input_str,
                                        user_function=None)
    return parameter
    pass

user_function_header_str = '''\
def user_function(value, times):
'''

user_function_end_str = '''\
    return value
'''

default_user_input_str = '''\
value += 1
if value > 100:
    value = 0
print('value = ', value, 'times = ', times)'''


def get_user_function_source_code(user_input_str):
    if user_input_str.startswith('    '):
        user_input_str = user_input_str.strip('\n') + '\n'
        pass
    else:
        user_input_str = user_input_str.strip(' ').strip('\n')
        user_input_str = user_input_str.replace('\n', '\n    ')
        user_input_str = '    ' + user_input_str + '\n'
        pass
    return user_function_header_str + user_input_str + user_function_end_str
    pass


def get_user_function(user_input_str):
    source_code = get_user_function_source_code(user_input_str)
    # print(source_code)
    # convert to ast format
    module_node = _ast.parse(source_code, '<string>', 'exec')

    # compile the ast as binary byte code
    code = compile(module_node, '<string>', 'exec')

    # and eval it in the right context
    globals_ = {}
    locals_ = dict()
    eval(code, globals_, locals_)

    # return the mapping class
    return locals_['user_function']
    pass


class Repeater:
    def __init__(self, datagram_manager, user_data=None):
        self.__datagram_manager = datagram_manager
        self.__user_data = user_data
        self.__access_data_lock = threading.Lock()
        self.__finished_event = threading.Event()
        self.__payload = DatagramPayload()
        self.__payload.value = 0
        self.__interval = 0.1
        self.__server_is_running = False
        self.__repeater_item_list = []
        self.__resource_dict = {}
        self.__thread = None
        pass

    @property
    def repeater_items(self):
        return list(self.__repeater_item_list)

    @property
    def is_running(self):
        return self.__server_is_running

    def set_default_payload_package(self, package):
        self.__access_data_lock.acquire()
        ret = self.__payload.set_package(package)
        self.__access_data_lock.release()
        return ret
        pass

    def append_repeater_item(self, hash_id, instance, action, resource):
        if self.__datagram_manager.is_valid_datagram(hash_id, instance, action) is False:
            print('ERROR:', '[hash id: 0x{hash_id:>08X} instance: {instance} action: {action}]'
                            ' is not define in data dictionary'.format(hash_id=hash_id,
                                                                       instance=instance,
                                                                       action=action))
            return False
        resource = repeater_parameter_type(**(vars(resource)))
        try:
            resource.user_function = get_user_function(resource.user_input_str)
        except Exception as exception:
            print('ERROR:', 'Parse user function failed,', exception)
            return False
        index = [hash_id, instance, action]
        if index in self.__repeater_item_list:
            print('ERROR:',
                  '[hash id: 0x{hash_id:>08X} instance: {instance} action: {action}]'
                  ' already exists in repeater list'.format(hash_id=hash_id, instance=instance, action=action))
            return False
        self.__access_data_lock.acquire()
        self.__repeater_item_list.append(index)
        if hash_id in self.__resource_dict:
            tmp_dict = self.__resource_dict[hash_id]
            if instance in tmp_dict:
                tmp_dict = tmp_dict[instance]
                tmp_dict[action] = resource
            else:
                tmp_dict[instance] = {action: resource}
        else:
            self.__resource_dict[hash_id] = {instance: {action: resource}}
        # print(self.__repeater_item_list)
        # print(self.__resource_dict)
        self.__access_data_lock.release()
        if self.__server_is_running:
            pass
        else:
            self.start_server()
        pass
        return True

    def delete_repeater_item(self, hash_id, instance, action):
        index = [hash_id, instance, action]
        if index not in self.__repeater_item_list:
            print('ERROR:',
                  '[hash id: 0x{hash_id:>08X} instance: {instance} action: {action}]'
                  ' not exists in repeater list'.format(hash_id=hash_id, instance=instance, action=action))
            return False
        self.__access_data_lock.acquire()
        self.__repeater_item_list.remove(index)
        self.__resource_dict[hash_id][instance].pop(action)
        if self.__resource_dict[hash_id][instance]:
            pass
        else:
            self.__resource_dict[hash_id].pop(instance)
            if self.__resource_dict[hash_id]:
                pass
            else:
                self.__resource_dict.pop(hash_id)
        # print(self.__repeater_item_list)
        # print(self.__resource_dict)
        self.__access_data_lock.release()
        if self.__repeater_item_list:
            pass
        else:
            self.__finished_event.set()
        pass
        return True

    def clear_repeater_item(self):
        self.__access_data_lock.acquire()
        self.__repeater_item_list.clear()
        self.__resource_dict.clear()
        self.__access_data_lock.release()
        self.__finished_event.set()
        pass

    def get_repeater_item_resource(self, hash_id, instance, action):
        self.__access_data_lock.acquire()
        if hash_id in self.__resource_dict:
            tmp_dict = self.__resource_dict[hash_id]
            if instance in tmp_dict:
                tmp_dict = tmp_dict[instance]
                try:
                    resource = tmp_dict[action]
                except KeyError:
                    resource = None
            else:
                resource = None
        else:
            resource = None
        self.__access_data_lock.release()
        return resource
        pass

    def start_server(self, interval=0.1):
        if (self.__server_is_running is True) or (self.__thread is not None):
            print('ERROR:', 'The repeater server is running')
            return
        if interval < 0.1:
            print('WARNING:', 'Interval value should bigger then 0.1, so set it as 0.1 automatically')
            interval = 0.1
        self.__interval = interval
        # self.start()
        self.__thread = threading.Thread(target=self.run)
        self.__thread.start()
        pass

    def run(self):
        finished_item = []
        self.__server_is_running = True
        while not self.__finished_event.is_set():
            self.__access_data_lock.acquire()
            for index in self.__repeater_item_list:
                hash_id = index[0]
                instance = index[1]
                action = index[2]
                resource = self.__resource_dict[hash_id][instance][action]
                if resource.counter >= resource.tagger_count:
                    self.__payload.hash_id = hash_id
                    self.__payload.device_instance_index = instance + 1
                    self.__payload.action = action
                    resource.repeat_times_counter += 1

                    # Get value and publish message
                    try:
                        dg = self.__datagram_manager.get_datagram(hash_id)
                        val = dg.get_device_data_value(instance, action)
                        self.__payload.value = resource.user_function(val,
                                                                      resource.repeat_times_counter)
                    except Exception as exception:
                        print('ERROR:',
                              'Excuse user function failed, {exception},'
                              ' so set payload value as {value}, automatically'.format(exception=exception,
                                                                                       value=self.__payload.value))
                    if self.__datagram_manager is not None:
                        self.__datagram_manager.send_package_by_payload(self.__payload)
                    # Check if it needs exit
                    if (resource.repeat_times_count > 0) and\
                            (resource.repeat_times_counter >= resource.repeat_times_count):
                        # Remove finished item
                        finished_item.append([hash_id, instance, action])
                        pass
                    if self.__user_data is not None:
                        try:
                            __resource = repeater_parameter_type(**(vars(resource)))
                            self.__user_data.repeater_recored(hash_id, instance, action, __resource)
                        except AttributeError:
                            pass
                    resource.counter = 0
                    # print(index, 'Source:', resource)
                else:
                    resource.counter += 1
            if finished_item:
                # Need remove finished items
                for item in finished_item:
                    hash_id = item[0]
                    instance = item[1]
                    action = item[2]
                    self.__repeater_item_list.remove(item)
                    self.__resource_dict[hash_id][instance].pop(action)
                    if self.__resource_dict[hash_id][instance]:
                        pass
                    else:
                        self.__resource_dict[hash_id].pop(instance)
                        if self.__resource_dict[hash_id]:
                            pass
                        else:
                            self.__resource_dict.pop(hash_id)
                    if self.__user_data is not None:
                        try:
                            self.__user_data.repeater_finished(hash_id, instance, action)
                        except AttributeError:
                            pass
                if self.__repeater_item_list:
                    pass
                else:
                    self.__finished_event.set()
                finished_item.clear()
                pass
            self.__access_data_lock.release()
            self.__finished_event.wait(self.__interval)
            pass
        self.__server_is_running = False
        self.__thread = None
        self.__finished_event.clear()
        print('Repeater server is stopped')
        pass

    def stop_server(self):
        if self.__server_is_running:
            self.__finished_event.set()
        pass
    pass


def demo_code():
    rpt = Repeater(None)
    rpt.start_server(0.1)
    resource = repeater_parameter(tagger_count=10,
                                  repeat_times_count=10,
                                  user_input_str=default_user_input_str)
    print(vars(resource))
    rpt.append_repeater_item(0x11, 0, 0, resource)

    print('OK')
    pass

if __name__ == '__main__':
    demo_code()
    pass
