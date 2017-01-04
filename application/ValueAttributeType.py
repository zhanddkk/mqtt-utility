from namedlist import namedlist as _type_creator
from ctypes import *
value_attribute_type = _type_creator('ValueAttribute', 'system_tag,'
                                                       'basic_type,'
                                                       'type_name,'
                                                       'array_count,'
                                                       'size,'
                                                       'special_data')
bit_attribute_type = _type_creator('BitAttribute', 'wide, names')

bool_attribute = value_attribute_type(system_tag='BasicType',
                                      basic_type='Bool',
                                      type_name='Bool',
                                      array_count=1,
                                      size=1,
                                      special_data=c_bool)

u_int8_attribute = value_attribute_type(system_tag='BasicType',
                                        basic_type='UInt8',
                                        type_name='UInt8',
                                        array_count=1,
                                        size=1,
                                        special_data=c_uint8
                                        )

u_int16_attribute = value_attribute_type(system_tag='BasicType',
                                         basic_type='UInt16',
                                         type_name='UInt16',
                                         array_count=1,
                                         size=2,
                                         special_data=c_uint16
                                         )

u_int32_attribute = value_attribute_type(system_tag='BasicType',
                                         basic_type='UInt32',
                                         type_name='UInt32',
                                         array_count=1,
                                         size=4,
                                         special_data=c_uint32
                                         )

int8_attribute = value_attribute_type(system_tag='BasicType',
                                      basic_type='Int8',
                                      type_name='Int8',
                                      array_count=1,
                                      size=1,
                                      special_data=c_int8)

int16_attribute = value_attribute_type(system_tag='BasicType',
                                       basic_type='Int16',
                                       type_name='Int16',
                                       array_count=1,
                                       size=2,
                                       special_data=c_int16)

int32_attribute = value_attribute_type(system_tag='BasicType',
                                       basic_type='Int32',
                                       type_name='Int32',
                                       array_count=1,
                                       size=4,
                                       special_data=c_int32)

float_attribute = value_attribute_type(system_tag='BasicType',
                                       basic_type='Float',
                                       type_name='Float',
                                       array_count=1,
                                       size=4,
                                       special_data=c_float)

string_attribute = value_attribute_type(system_tag='StringType',
                                        basic_type=None,
                                        type_name='String',
                                        array_count=1,
                                        size=None,
                                        special_data=None)

standard_value_attribute_dictionary = {
    'Bool': bool_attribute,
    'Int8': int8_attribute,
    'Int16': int16_attribute,
    'Int32': int32_attribute,
    'UInt8': u_int8_attribute,
    'UInt16': u_int16_attribute,
    'UInt32': u_int32_attribute,
    'Float': float_attribute,
    'String': string_attribute
}
