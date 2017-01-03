from .NamedList import named_list

data_dictionary_item_attribute_names = (
    'root_system',
    'sub_system',
    'data_path',
    'name',
    'description',
    'type',                     # General Status Command Setting Measure
    'system_tag',               # BasicType EnumType ArrayType StructureType StringType
    'basic_type',               # Bool Int8 UInt8 Int16 UInt16 Int32 UInt32 Float
    'max_size',                 # As the data dictionary
    'array_count',              # Array count
    'default',
    'min',
    'max',
    'selectable_point',         # List type, limit the value of the datagram been set as the content of the list
    'choice_list',              # The enum content
    'structure_format',         # The structure type datagram's data format
    'scale_unit',
    'precision',
    'is_alarm',                 # Bool Type
    'is_event_log',             # Bool Type
    'cmd_time_out',
    'producer',                 # List Type, list all the name of producers
    'consumer',                 # List Type, list all the name of consumers
    'no_setting_req_consumer',  # List Type, list all the consumers' name who does't have the setting request right
    'hash_id'                   # The datagram's hash id (get from data dictionary), 0xffffffff is invalid
)

data_dictionary_item_type = named_list('DataDictionaryItem', data_dictionary_item_attribute_names)

data_dictionary_item_text_format = '''\
root_system             = {root_system}
sub_system              = {sub_system}
data_path               = {data_path}
name                    = {name}
description             = {description}
type                    = {type}
system_tag              = {system_tag}
basic_type              = {basic_type}
max_size                = {max_size}
array_count             = {array_count}
default                 = {default}
min                     = {min}
max                     = {max}
selectable_point        = {selectable_point}
choice_list             = {choice_list}
structure_format        = {structure_format}
scale_unit              = {scale_unit}
precision               = {precision}
is_alarm                = {is_alarm}
is_event_log            = {is_event_log}
cmd_time_out            = {cmd_time_out}
producer                = {producer}
consumer                = {consumer}
no_setting_req_consumer = {no_setting_req_consumer}
hash_id                 = 0x{hash_id:>08X}'''
if __name__ == '__main__':
    data_dictionary_item = data_dictionary_item_type(*[i for i in range(25)])
    print(data_dictionary_item_text_format.format(**vars(data_dictionary_item)))
    pass


