from .NamedList import named_list
from .DatagramDeviceDataHistory import DatagramDeviceDataHistory
datagram_device_data_action_class = named_list('DatagramDeviceDataAction', 'publish, response, request, allow')
action_item_class = named_list('ActionItem', 'topic, value, history')


class DatagramDeviceData:
    def __init__(self, instance, topic, default_value=None):
        self.__instance = instance
        self.__action =\
            datagram_device_data_action_class(publish=action_item_class(topic=topic,
                                                                        value=default_value,
                                                                        history=DatagramDeviceDataHistory()),
                                              response=action_item_class(topic='Response/' + topic,
                                                                         value=0,
                                                                         history=DatagramDeviceDataHistory()),
                                              request=action_item_class(topic='Request/' + topic,
                                                                        value=default_value,
                                                                        history=DatagramDeviceDataHistory()),
                                              allow=action_item_class(topic='AllowedRequest/' + topic,
                                                                      value=None,
                                                                      history=DatagramDeviceDataHistory()))
        # self.__history = None
        pass

    @property
    def instance(self):
        return self.__instance

    def update_value_by_payload(self, topic, payload):
        try:
            action = self.__action[payload.action]
            if topic != action.topic:
                print('WARNING:', 'Payload topic and action topic do not match. Action topic =',
                      action.topic + ',', 'payload topic = ', topic)
            action.value = payload.value
            # Save history as received
            action.history.append_data(1, payload.value)
        except IndexError:
            print('ERROR:', 'Action value in payload is out of the range.')
        except TypeError as exception:
            print('ERROR:', exception)
        pass

    def set_value_by_payload(self, payload):
        try:
            action = self.__action[payload.action]
            action.value = payload.value
            # Save history as published
            action.history.append_data(0, payload.value)
        except IndexError:
            print('ERROR:', 'Action value in payload is out of the range.')
        except TypeError as exception:
            print('ERROR:', exception)
        pass

    def get_value(self, action):
        try:
            return self.__action[action].value
        except IndexError:
            print('ERROR:', 'Action value is out of the range.')
            return None
        except TypeError as exception:
            print('ERROR:', exception)
            return None

    def get_topic(self, action):
        try:
            return self.__action[action].topic
        except IndexError:
            print('ERROR:', 'Action value is out of the range.')
            return None
        except TypeError as exception:
            print('ERROR:', exception)
            return None

    def get_history_data(self, action):
        try:
            return self.__action[action].history.data
        except IndexError:
            print('ERROR:', 'Action value is out of the range.')
            return None
        except TypeError as exception:
            print('ERROR:', exception)
            return None

    pass
