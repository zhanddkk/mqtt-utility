try:
    from .dgdevdata import DatagramDeviceData
    from .dgpayload import (E_DATAGRAM_ACTION_PUBLISH, E_DATAGRAM_ACTION_RESPONSE, E_DATAGRAM_ACTION_REQUEST,
                            E_DATAGRAM_ACTION_ALLOW)
    from .valuetype import ValueType, standard_value_attribute_dictionary
    from .bitmapparser import command_bit_map, command_response_bit_map, setting_response_bit_map, BitMapParser
except SystemError:
    from dgdevdata import DatagramDeviceData
    from dgpayload import (E_DATAGRAM_ACTION_PUBLISH, E_DATAGRAM_ACTION_RESPONSE, E_DATAGRAM_ACTION_REQUEST,
                           E_DATAGRAM_ACTION_ALLOW)
    from valuetype import ValueType, standard_value_attribute_dictionary
    from bitmapparser import command_bit_map, command_response_bit_map, setting_response_bit_map, BitMapParser


class Datagram:
    __command_value_attribute = ValueType(
        system_tag='BitmapType',
        basic_type='UInt32',
        size=4,
        special_data=command_bit_map
    )  # Bitmap

    __command_response_value_attribute = ValueType(
        system_tag='BitmapType',
        basic_type='UInt32',
        size=4,
        special_data=command_response_bit_map
    )  # Bitmap

    __setting_response_value_attribute = ValueType(
        system_tag='BitmapType',
        basic_type='UInt32',
        size=4,
        special_data=setting_response_bit_map
    )

    __one_allow_value_attribute = standard_value_attribute_dictionary['Bool']

    def __init__(self, attribute):
        self.__attribute = attribute
        self.__device_data_list = []
        self.__make_data_list()
        pass

    @property
    def attribute(self):
        return self.__attribute

    @property
    def device_number(self):
        return len(self.__device_data_list)

    @property
    def device_data_list(self):
        return self.__device_data_list

    def get_device_data(self, instance):
        try:
            return self.__device_data_list[instance]
        except IndexError:
            print('ERROR:', 'Can not find any data by instance:', instance)
            return None
        except TypeError:
            print('ERROR:', 'Can not find any data by instance:', instance)
            return None

    def is_valid_action(self, action=E_DATAGRAM_ACTION_PUBLISH):
        _ret = True
        if action == E_DATAGRAM_ACTION_REQUEST:
            if self.__attribute.type != 'Setting':
                _ret = False
        elif (action == E_DATAGRAM_ACTION_RESPONSE) or \
                (action == E_DATAGRAM_ACTION_ALLOW):
            if (self.__attribute.type != 'Command') and (self.__attribute.type != 'Setting'):
                _ret = False
            pass
        elif action == E_DATAGRAM_ACTION_PUBLISH:
            pass
        else:
            # Invalid action value
            _ret = False
            pass
        return _ret
        pass

    def get_value_type(self, action=E_DATAGRAM_ACTION_PUBLISH):
        _value_type = None
        if self.is_valid_action(action):
            if self.__attribute.type == 'Command':
                if action == E_DATAGRAM_ACTION_PUBLISH:
                    _value_type = self.__command_value_attribute
                    pass
                elif action == E_DATAGRAM_ACTION_RESPONSE:
                    _value_type = self.__command_response_value_attribute
                    pass
                elif action == E_DATAGRAM_ACTION_ALLOW:
                    _value_type = self.__one_allow_value_attribute
                else:
                    pass
                pass
            elif self.__attribute.type == 'Setting':
                if (action == E_DATAGRAM_ACTION_PUBLISH) or action == E_DATAGRAM_ACTION_REQUEST:
                    _value_type = self.attribute.value_type
                    pass
                elif action == E_DATAGRAM_ACTION_RESPONSE:
                    _value_type = self.__setting_response_value_attribute
                    pass
                elif action == E_DATAGRAM_ACTION_ALLOW:
                    # Maybe
                    _value_type = self.__one_allow_value_attribute
                else:
                    pass
                pass
            else:
                _value_type = self.attribute.value_type
                pass
            pass
        else:
            pass
        return _value_type
        pass

    def is_valid_device(self, instance, action=E_DATAGRAM_ACTION_PUBLISH):
        dg = self.get_device_data(instance)
        if dg is None:
            _ret = False
        else:
            _ret = self.is_valid_action(action)
        return _ret
        pass

    def get_device_data_value(self, instance, action=E_DATAGRAM_ACTION_PUBLISH):
        dg = self.get_device_data(instance)
        if dg is None:
            return None
        if action == E_DATAGRAM_ACTION_REQUEST:
            if self.__attribute.type != 'Setting':
                print('ERROR:', 'Action value ', action, 'and datagram type do not match.')
                return None
        elif (action == E_DATAGRAM_ACTION_RESPONSE) or\
                (action == E_DATAGRAM_ACTION_ALLOW):
            if (self.__attribute.type != 'Command') and (self.__attribute.type != 'Setting'):
                print('ERROR:', 'Action value ', action, 'and datagram type do not match.')
                return None
            pass
        elif action == E_DATAGRAM_ACTION_PUBLISH:
            pass
        else:
            # Invalid action value
            pass
        dev_data = self.get_device_data(instance)
        if dev_data is None:
            return None
        return dev_data.get_value(action)
        pass

    def get_device_data_history(self, instance, action=E_DATAGRAM_ACTION_PUBLISH):
        dg = self.get_device_data(instance)
        if dg is None:
            return None
        if action == E_DATAGRAM_ACTION_REQUEST:
            if self.__attribute.type != 'Setting':
                print('ERROR:', 'Action value ', action, 'and datagram type do not match.')
                return None
        elif (action == E_DATAGRAM_ACTION_RESPONSE) or \
                (action == E_DATAGRAM_ACTION_ALLOW):
            if (self.__attribute.type != 'Command') and (self.__attribute.type != 'Setting'):
                print('ERROR:', 'Action value ', action, 'and datagram type do not match.')
                return None
            pass
        elif action == E_DATAGRAM_ACTION_PUBLISH:
            pass
        else:
            # Invalid action value
            pass
        dev_data = self.get_device_data(instance)
        if dev_data is None:
            return None
        return dev_data.get_history_data(action)
        pass

    def update_device_data_value_by_payload(self, topic, payload):
        action = payload.action
        if action == E_DATAGRAM_ACTION_REQUEST:
            if self.__attribute.type != 'Setting':
                print('ERROR:', 'Action value ', action, 'and datagram type do not match.')
                return False
        elif (action == E_DATAGRAM_ACTION_RESPONSE) or\
                (action == E_DATAGRAM_ACTION_ALLOW):
            if (self.__attribute.type != 'Command') and (self.__attribute.type != 'Setting'):
                print('ERROR:', 'Action value ', action, 'and datagram type do not match.')
                return False
            pass
        elif action == E_DATAGRAM_ACTION_PUBLISH:
            pass
        else:
            # Invalid action value
            pass
        instance = payload.device_instance_index - 1
        dev_data = self.get_device_data(instance)
        if dev_data is None:
            return False
        dev_data.update_value_by_payload(topic, payload)
        return True
        pass

    def set_device_data_value_by_payload(self, payload):
        action = payload.action
        if action == E_DATAGRAM_ACTION_REQUEST:
            if self.__attribute.type != 'Setting':
                print('ERROR:', 'Action value ', action, 'and datagram type do not match.')
                return False
        elif (action == E_DATAGRAM_ACTION_RESPONSE) or \
                (action == E_DATAGRAM_ACTION_ALLOW):
            if (self.__attribute.type != 'Command') and (self.__attribute.type != 'Setting'):
                print('ERROR:', 'Action value ', action, 'and datagram type do not match.')
                return False
            pass
        elif action == E_DATAGRAM_ACTION_PUBLISH:
            pass
        else:
            # Invalid action value
            pass
        instance = payload.device_instance_index - 1
        dev_data = self.get_device_data(instance)
        if dev_data is None:
            return False
        dev_data.set_value_by_payload(payload)
        return True
        pass

    def __make_data_list(self):
        root = self.__attribute.root_system
        system = self.__attribute.sub_system
        path = self.__attribute.data_path
        name = self.__attribute.name
        default = self.__attribute.default

        if root == '':
            pass
        else:
            root += '/'
            pass
        if system == '':
            pass
        else:
            system += '/'
        system = root + system
        path = path.strip('/').replace('\\', '/')
        if path == '':
            pass
        else:
            path += '/'
        if name == '':
            name = 'NO_DEFINE'

        start = path.find('[')
        end = path.find(']')

        if (start == -1) or (end == -1) or (start >= end) or (start < 1) or (end < 1):
            self.__device_data_list.append(DatagramDeviceData(0,
                                                              system + path + name,
                                                              default))
        else:
            num = path[start + 1:end]

            if num.isdigit():
                device_number = int(num, base=10)
                front = path[:start]
                behind = path[end + 1:]
                for i in range(device_number):
                    tmp = system + front + str(i + 1) + behind + name
                    self.__device_data_list.append(DatagramDeviceData(i,
                                                                      tmp,
                                                                      default))
            else:
                self.__device_data_list.append(DatagramDeviceData(0,
                                                                  system + path + name,
                                                                  default))
        pass
    pass
