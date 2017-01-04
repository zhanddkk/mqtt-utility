from namedlist import namedlist as named_list
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
E_DATAGRAM_ACTION_RESPONSE = 1
E_DATAGRAM_ACTION_REQUEST = 2
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

payload_package_info_item_class = named_list('PayloadPackageInfoItem', 'type, choice_list')
payload_package_info = {
    E_PAYLOAD_TYPE: payload_package_info_item_class(type='UInt16',
                                                    choice_list={0: 'Dynamic',
                                                                 1: 'Property'}),
    E_PAYLOAD_VERSION: payload_package_info_item_class(type='UInt16',
                                                       choice_list=None),
    E_HASH_ID: payload_package_info_item_class(type='UInt32',
                                               choice_list=None),
    E_PRODUCER_MASK: payload_package_info_item_class(type='UInt32',
                                                     choice_list={D_NODE_MASK_UC: 'UC',
                                                                  D_NODE_MASK_SLC_UPS: 'SLC_UPS',
                                                                  D_NODE_MASK_SLC_NMC: 'SLC_NMC',
                                                                  D_NODE_MASK_HMI: 'HMI',
                                                                  D_NODE_MASK_TUNER: 'TUNER'}),
    E_ACTION: payload_package_info_item_class(type='UInt16',
                                              choice_list={E_DATAGRAM_ACTION_PUBLISH: 'Publish',
                                                           E_DATAGRAM_ACTION_RESPONSE: 'Response',
                                                           E_DATAGRAM_ACTION_REQUEST: 'Request',
                                                           E_DATAGRAM_ACTION_ALLOW: 'Allow'}),
    E_TIMESTAMP_SECOND: payload_package_info_item_class(type='UInt32',
                                                        choice_list=None),
    E_TIMESTAMP_MS: payload_package_info_item_class(type='UInt16',
                                                    choice_list=None),
    E_DEVICE_INSTANCE_INDEX: payload_package_info_item_class(type='UInt16',
                                                             choice_list=None),
    E_DATA_OBJECT_REFERENCE_TYPE: payload_package_info_item_class(type='UInt16',
                                                                  choice_list=None),
    E_DATA_OBJECT_REFERENCE_VALUE: payload_package_info_item_class(type='UInt16',
                                                                   choice_list=None)
}

datagram_payload_data_class = named_list('DatagramPayloadData',
                                         'payload_type,'
                                         ' payload_version,'
                                         ' hash_id,'
                                         ' producer_mask,'
                                         ' action,'
                                         ' time_stamp_second,'
                                         ' time_stamp_ms,'
                                         ' device_instance_index,'   # Start from 1, not 0
                                         ' data_object_reference_type,'
                                         ' data_object_reference_value,'
                                         ' value')


class DatagramPayload(datagram_payload_data_class):

    def __init__(self, hash_id=0, device_instance_index=1):
        self.is_object_reference_package = False
        super(DatagramPayload, self).__init__(payload_type=0,
                                              payload_version=0,
                                              hash_id=hash_id,
                                              producer_mask=1,
                                              action=0,
                                              time_stamp_second=0xffffffff,
                                              time_stamp_ms=0xffff,
                                              device_instance_index=device_instance_index,
                                              data_object_reference_type=0,
                                              data_object_reference_value=0,
                                              value=None)
        pass

    def __str__(self):
        if self.is_object_reference_package:
            return \
                "E_PAYLOAD_TYPE                :" + str(self.payload_type) + '\n' + \
                "E_PAYLOAD_VERSION             :" + str(self.payload_version) + '\n' + \
                "E_HASH_ID                     :" + '0x{:0>8X}'.format(self.hash_id) + '\n' + \
                "E_PRODUCER_MASK               :" + '0x{:0>8X}'.format(self.producer_mask) + '\n' + \
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
                "E_HASH_ID                     :" + '0x{:0>8X}'.format(self.hash_id) + '\n' + \
                "E_PRODUCER_MASK               :" + '0x{:0>8X}'.format(self.producer_mask) + '\n' + \
                "E_ACTION                      :" + str(self.action) + '\n' + \
                "E_TIMESTAMP_SECOND            :" + str(self.time_stamp_second) + '\n' + \
                "E_TIMESTAMP_MS                :" + str(self.time_stamp_ms) + '\n' + \
                "E_DEVICE_INSTANCE_INDEX       :" + str(self.device_instance_index) + '\n' + \
                "E_VALUE                       :" + str(self.value)
            pass

    def __repr__(self):
        return self.__str__()

    @property
    def package(self):
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

    def set_package(self, package):
        try:
            setattr(self, 'payload_type', package[E_PAYLOAD_TYPE])
            setattr(self, 'payload_version', package[E_PAYLOAD_VERSION])
            setattr(self, 'hash_id', package[E_HASH_ID])
            setattr(self, 'producer_mask', package[E_PRODUCER_MASK])
            setattr(self, 'action', package[E_ACTION])
            setattr(self, 'time_stamp_second', package[E_TIMESTAMP_SECOND])
            setattr(self, 'time_stamp_ms', package[E_TIMESTAMP_MS])
            setattr(self, 'device_instance_index', package[E_DEVICE_INSTANCE_INDEX])
            if (E_DATA_OBJECT_REFERENCE_TYPE in package) or (E_DATA_OBJECT_REFERENCE_VALUE in package):
                setattr(self, 'data_object_reference_type', package[E_DATA_OBJECT_REFERENCE_TYPE])
                setattr(self, 'data_object_reference_value', package[E_DATA_OBJECT_REFERENCE_VALUE])
                self.is_object_reference_package = True
            else:
                self.is_object_reference_package = False
            setattr(self, 'value', package[E_VALUE])
            return True
            pass
        except Exception as exception:
            print('ERROR', 'the input package format is error, exception :', exception)
            return False
            pass
        pass

    def get_package(self):
        return self.package

    pass

if __name__ == '__main__':
    pass
