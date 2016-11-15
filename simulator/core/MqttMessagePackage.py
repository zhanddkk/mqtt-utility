

class MqttMessagePackage:
    E_PAYLOAD_TYPE = 0
    E_PAYLOAD_VERSION = 1
    E_HASH_ID = 2
    E_PRODUCER_MASK = 3
    E_ACTION = 4
    E_TIMESTAMP_SECOND = 5
    E_TIMESTAMP_MS = 6
    E_DEVICE_INSTANCE_INDEX = 7
    E_DATA_OBJECT_REFERENCE_TYPE = 8
    E_DATA_OBJECT_REFERENCE_VALUE = 9
    E_VALUE = 10

    value_package_name = [
        "E_PAYLOAD_TYPE",
        "E_PAYLOAD_VERSION",
        "E_HASH_ID",
        "E_PRODUCER_MASK",
        "E_ACTION",
        "E_TIMESTAMP_MS",
        "E_TIMESTAMP_SECOND",
        "E_DEVICE_INSTANCE_INDEX",
        "E_VALUE"
    ]

    value_display_index = {
        "E_PAYLOAD_TYPE": E_PAYLOAD_TYPE,
        "E_PAYLOAD_VERSION": E_PAYLOAD_VERSION,
        "E_HASH_ID": E_HASH_ID,
        "E_PRODUCER_MASK": E_PRODUCER_MASK,
        "E_ACTION": E_ACTION,
        "E_TIMESTAMP_MS": E_TIMESTAMP_MS,
        "E_TIMESTAMP_SECOND": E_TIMESTAMP_SECOND,
        "E_DEVICE_INSTANCE_INDEX": E_DEVICE_INSTANCE_INDEX,
        "E_VALUE": E_VALUE
    }

    # For match cbor format
    value_package = {
        E_PAYLOAD_TYPE: 0,
        E_PAYLOAD_VERSION: 0,
        E_HASH_ID: 0,
        E_PRODUCER_MASK: 0,
        E_ACTION: 0,
        E_TIMESTAMP_MS: 0xffff,
        E_TIMESTAMP_SECOND: 0xffffffff,
        E_DEVICE_INSTANCE_INDEX: 1,
        E_VALUE: None
    }

    def __init__(self, value_package=None):
        if value_package:
            self.value_package = value_package
        pass

    @property
    def payload_type(self):
        return self.value_package[self.E_PAYLOAD_TYPE]

    @payload_type.setter
    def payload_type(self, val):
        self.value_package[self.E_PAYLOAD_TYPE] = val

    @property
    def payload_version(self):
        return self.value_package[self.E_PAYLOAD_VERSION]

    @payload_version.setter
    def payload_version(self, val):
        self.value_package[self.E_PAYLOAD_VERSION] = val

    @property
    def hash_id(self):
        return self.value_package[self.E_HASH_ID]

    @hash_id.setter
    def hash_id(self, val):
        self.value_package[self.E_HASH_ID] = val

    @property
    def producer_mask(self):
        return self.value_package[self.E_PRODUCER_MASK]

    @producer_mask.setter
    def producer_mask(self, val):
        self.value_package[self.E_PRODUCER_MASK] = val

    @property
    def action(self):
        return self.value_package[self.E_ACTION]

    @action.setter
    def action(self, val):
        self.value_package[self.E_ACTION] = val

    @property
    def time_stamp_ms(self):
        return self.value_package[self.E_TIMESTAMP_MS]

    @time_stamp_ms.setter
    def time_stamp_ms(self, val):
        self.value_package[self.E_TIMESTAMP_MS] = val

    @property
    def time_stamp_second(self):
        return self.value_package[self.E_TIMESTAMP_SECOND]

    @time_stamp_second.setter
    def time_stamp_second(self, val):
        self.value_package[self.E_TIMESTAMP_SECOND] = val

    @property
    def device_instance_index(self):
        return self.value_package[self.E_DEVICE_INSTANCE_INDEX]

    @device_instance_index.setter
    def device_instance_index(self, val):
        self.value_package[self.E_DEVICE_INSTANCE_INDEX] = val

    @property
    def value(self):
        return self.value_package[self.E_VALUE]

    @value.setter
    def value(self, val):
        self.value_package[self.E_VALUE] = val

    @property
    def to_json_str(self):
        json_str = ""
        for name in self.value_package_name:
            json_str += '{:<25}'.format('\"' + name + '\"') + ': ' \
                        + self.value_to_str(self.value_package[self.value_display_index[name]]) + ',\n'
        return '{\n' + json_str.rstrip(',\n') + '\n}'
        pass
    pass

    @staticmethod
    def value_to_str(value):
        value_str = str(value)
        if value_str == 'None':
            value_str = 'null'
        elif value_str == 'True':
            value_str = 'true'
        elif value_str == 'False':
            value_str = 'false'
        return value_str
        pass


def json_object_pairs_hook(list_data):
    import collections
    # print(list_data)
    return collections.OrderedDict(list_data)
    pass

if __name__ == "__main__":
    # pkg = MqttMessagePackage()
    # print(pkg.to_json_str)
    import json
    json_str = '{"a":12, "b":13, "f":25, "c":44}'
    data = json.loads(json_str, object_pairs_hook=json_object_pairs_hook)
    print(data['b'])
    print(data)

    a = '4294967295'
    b = int(a)
    print(type(b))
    print(b)
    pass
