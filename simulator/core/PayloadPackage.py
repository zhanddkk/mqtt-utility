# ----Payload Type----
# 0: Datagram dynamic value(default)
# 1: Datagram property value

# ----Payload Version----
# It is a 16 bits number indicate the version of the specified payload type

# ----Hash ID----
# The unique 32bit hash ID is generated from the unique name string

# ----Producer Mask----
# This field is an unsigned 32bit value
D_NODE_MASK_UC = 1          # (1<<0)
D_NODE_MASK_SLC_UPS = 2     # (1<<1)
D_NODE_MASK_SLC_NMC = 4     # (1<<2)
D_NODE_MASK_HMI = 8         # (1<<3)
D_NODE_MASK_TUNER = 16      # (1<<4)

# ----Action----
E_DATAGRAM_ACTION_PUBLISH = 0
E_DATAGRAM_ACTION_REQUEST = 1
E_DATAGRAM_ACTION_RESPONSE = 2
E_DATAGRAM_ACTION_ALLOW = 3
# ----Time Stamp----
# The timestamp is used to indicate the accurate time of the datagram value update
# typedef struct
# {
#     uint32_t ui32Secounds;
#    uint16_t ui16MilliSeconds;
# } TDatagramTimeStamp;
# The timestamp is optional, if the producer node doesn’t supply it,
# it need to set it to an invalid format (ui32Secounds = 0xFFFFFFFF, and ui16MilliSeconds = 0xFFFF).

# ----Device Instance Index----
# The unsigned 16bit index

# ----Package Index----
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
# ----Package Item Info----
payload_package_item_info = {
    E_PAYLOAD_TYPE: ['UInt16', {0: 'Dynamic', 1: 'Property'}],
    E_PAYLOAD_VERSION: ['UInt16', None],
    E_HASH_ID: ['UInt32', None],
    E_PRODUCER_MASK: ['UInt32', {D_NODE_MASK_UC: 'UC',
                                 D_NODE_MASK_SLC_UPS: 'SLC_UPS',
                                 D_NODE_MASK_SLC_NMC: 'SLC_NMC',
                                 D_NODE_MASK_HMI: 'HMI',
                                 D_NODE_MASK_TUNER: 'TUNER'}],
    E_ACTION: ['UInt16', {0: 'Publish', 1: 'Request', 2: 'Response', 3: 'Allow'}],
    E_TIMESTAMP_SECOND: ['UInt32', None],
    E_TIMESTAMP_MS: ['UInt16', None],
    E_DEVICE_INSTANCE_INDEX: ['UInt16', None],
    E_DATA_OBJECT_REFERENCE_TYPE: ['UInt16', None],
    E_DATA_OBJECT_REFERENCE_VALUE: ['UInt16', None],
}


class PayloadPackage:
    is_object_reference_package = False
    payload_type = 0
    payload_version = 0
    hash_id = 0
    producer_mask = 1
    action = 0
    time_stamp_second = 0xffffffff
    time_stamp_ms = 0xffff
    device_instance_index = 1       # Start from 1, not 0
    data_object_reference_type = 0
    data_object_reference_value = 0
    value = None

    def loads(self, package):
        try:
            self.payload_type = package[E_PAYLOAD_TYPE]
            self.payload_version = package[E_PAYLOAD_VERSION]
            self.hash_id = package[E_HASH_ID]
            self.producer_mask = package[E_PRODUCER_MASK]
            self.action = package[E_ACTION]
            self.time_stamp_second = package[E_TIMESTAMP_SECOND]
            self.time_stamp_ms = package[E_TIMESTAMP_MS]
            self.device_instance_index = package[E_DEVICE_INSTANCE_INDEX]
            if (E_DATA_OBJECT_REFERENCE_TYPE in package) or (E_DATA_OBJECT_REFERENCE_VALUE in package):
                self.data_object_reference_type = package[E_DATA_OBJECT_REFERENCE_TYPE]
                self.data_object_reference_value = package[E_DATA_OBJECT_REFERENCE_VALUE]
                self.is_object_reference_package = True
            else:
                self.is_object_reference_package = False
            self.value = package[E_VALUE]
            return True
            pass
        except Exception as exception:
            print('ERROR', 'the input package format is error, exception :', exception)
            return False
            pass
        pass

    def dumps(self):
        if self.is_object_reference_package:
            return {
                E_PAYLOAD_TYPE: self.payload_type,
                E_PAYLOAD_VERSION: self.payload_version,
                E_HASH_ID: self.hash_id,
                E_PRODUCER_MASK: self.producer_mask,
                E_ACTION: self.action,
                E_TIMESTAMP_SECOND: self.time_stamp_second,
                E_TIMESTAMP_MS: self.time_stamp_ms,
                E_DEVICE_INSTANCE_INDEX: self.device_instance_index,
                E_DATA_OBJECT_REFERENCE_TYPE: self.data_object_reference_type,
                E_DATA_OBJECT_REFERENCE_VALUE: self.data_object_reference_value,
                E_VALUE: self.value
            }
        else:
            return {
                E_PAYLOAD_TYPE: self.payload_type,
                E_PAYLOAD_VERSION: self.payload_version,
                E_HASH_ID: self.hash_id,
                E_PRODUCER_MASK: self.producer_mask,
                E_ACTION: self.action,
                E_TIMESTAMP_SECOND: self.time_stamp_second,
                E_TIMESTAMP_MS: self.time_stamp_ms,
                E_DEVICE_INSTANCE_INDEX: self.device_instance_index,
                E_VALUE: self.value
            }
        pass

    def to_string(self):
        if self.is_object_reference_package:
            return \
                "E_PAYLOAD_TYPE                :" + str(self.payload_type) + '\n' + \
                "E_PAYLOAD_VERSION             :" + str(self.payload_version) + '\n' + \
                "E_HASH_ID                     :" + '0x' + '{:0>8}'.format(hex(self.hash_id)[2:].upper()) + '\n' + \
                "E_PRODUCER_MASK               :" + '0x' + '{:0>8}'.format(hex(self.producer_mask)[2:].upper()) + '\n'\
                + \
                "E_ACTION                      :" + str(self.action) + '\n' + \
                "E_TIMESTAMP_SECOND            :" + str(self.time_stamp_second) + '\n' + \
                "E_TIMESTAMP_MS                :" + str(self.time_stamp_ms) + '\n' + \
                "E_DEVICE_INSTANCE_INDEX       :" + str(self.device_instance_index) + '\n' + \
                "E_DATA_OBJECT_REFERENCE_TYPE  :" + str(self.data_object_reference_type) + '\n' + \
                "E_DATA_OBJECT_REFERENCE_VALUE :" + str(self.data_object_reference_value) + '\n' + \
                "E_VALUE                       :" + str(self.value)
            pass
        else:
            return \
                "E_PAYLOAD_TYPE                :" + str(self.payload_type) + '\n' + \
                "E_PAYLOAD_VERSION             :" + str(self.payload_version) + '\n' + \
                "E_HASH_ID                     :" + '0x' + '{:0>8}'.format(hex(self.hash_id)[2:].upper()) + '\n' + \
                "E_PRODUCER_MASK               :" + '0x' + '{:0>8}'.format(hex(self.producer_mask)[2:].upper()) + '\n'\
                + \
                "E_ACTION                      :" + str(self.action) + '\n' + \
                "E_TIMESTAMP_SECOND            :" + str(self.time_stamp_second) + '\n' + \
                "E_TIMESTAMP_MS                :" + str(self.time_stamp_ms) + '\n' + \
                "E_DEVICE_INSTANCE_INDEX       :" + str(self.device_instance_index) + '\n' + \
                "E_VALUE                       :" + str(self.value)
            pass

    pass


if __name__ == '__main__':
    pass

