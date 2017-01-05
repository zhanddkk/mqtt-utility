import ast as _ast
try:
    from .dditem import data_dictionary_item_type
except SystemError:
    from dditem import data_dictionary_item_type

code_generator_header_text = '''
class DatagramAttributeMapping:
    # source_data type must be data_dictionary_item_type
    def __init__(self, source_data):
        self._source = source_data
'''

code_generator_property_text = '''
    @property
    def {name}(self):
        return self._source.{name}
'''


def attribute_mapping_class():
    source_code = code_generator_header_text
    for fields_name in getattr(data_dictionary_item_type, '_fields'):
        source_code += code_generator_property_text.format(name=fields_name)

    # convert to ast format
    module_node = _ast.parse(source_code, '<string>', 'exec')

    # compile the ast as binary byte code
    code = compile(module_node, '<string>', 'exec')

    # and eval it in the right context
    globals_ = {}
    locals_ = dict()
    eval(code, globals_, locals_)

    # return the mapping class
    return locals_['DatagramAttributeMapping']

attribute_mapping = attribute_mapping_class()


class DatagramAttribute(attribute_mapping):
    def __init__(self, source):
        super(DatagramAttribute, self).__init__(source)

if __name__ == '__main__':
    pass
