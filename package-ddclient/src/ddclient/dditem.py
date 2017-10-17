from namedlist import namedlist as named_list

data_dictionary_item_attribute_names = (
    'root_system',
    'sub_system',
    'data_path',
    'name',
    'description',
    'type',                     # General Status Command Setting Measure
    'value_type',
    'default',
    'min',
    'max',
    'selectable_point',         # List type, limit the value of the datagram been set as the content of the list
    'scale_unit',
    'precision',
    'is_alarm',                 # Bool Type
    'is_event_log',             # Bool Type
    'is_none_volatile',         # Bool Type
    'is_retain',                # Bool Type
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
value_type              = {value_type}
default                 = {default}
min                     = {min}
max                     = {max}
selectable_point        = {selectable_point}
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


