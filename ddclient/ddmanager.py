from collections import OrderedDict

from namedlist import namedlist as named_list

try:
    from ddformatinfo import data_dictionary_format_info
    from .ddinterface import data_dictionary_interface
except SystemError:
    from ddformatinfo import data_dictionary_format_info
    from ddinterface import data_dictionary_interface

__data_dictionary_version_map = (
    ('0.11', (0, 0)),
)
data_dictionary_version_map = OrderedDict(__data_dictionary_version_map)
latest_data_dictionary_version = __data_dictionary_version_map[-1][0]


def set_sub_attr_value(obj, _range, row, item):
    if type(item) is not str:
        print('ERROR:', 'Attribute name must be string, but not', type(item))
        return
    if type(_range) is list:
        try:
            setattr(obj, item, row[_range[0]:_range[1]])
        except AttributeError:
            print('ERROR:', item, 'is not the right attribute name of', obj)
            return
        pass
    else:
        try:
            try:
                tmp_obj = getattr(obj, item)
            except AttributeError:
                print('ERROR:', item, 'is not the right attribute name of', obj)
                return
            fields = getattr(tmp_obj, '_fields')
            pass
        except AttributeError:
            print('ERROR:', 'Predefine attribute',
                  item, 'format and the header of the data dictionary file do not match')
            return
            pass
        for obj_attr in fields:
            if obj_attr in _range:
                tmp_range = _range[obj_attr]
                set_sub_attr_value(tmp_obj, tmp_range, row, item=obj_attr)
                pass
            else:
                print('WARNING:', 'Predefined sub attribute', obj_attr, 'is not found in the data dictionary')
                pass
        pass
    pass


def set_attr_value(obj, _range, row):
    for obj_attr in getattr(obj, '_fields'):
        if obj_attr in _range:
            tmp_range = _range[obj_attr]
            set_sub_attr_value(obj, tmp_range, row, item=obj_attr)
            pass
        else:
            print('WARNING:', 'Predefined attribute', obj_attr, 'is not found in the data dictionary')
            pass
    pass


class DataDictionaryManager:
    def __init__(self):
        self.header = OrderedDict()
        version_class = type('Version',
                             (named_list('_Version', 'major, minor, doc'),),
                             {'__repr__': self.__ver_item_str,
                              '__str__': self.__ver_item_str})
        template_version = version_class(0, 0, 'Template Version')
        content_version = version_class(0, 0, 'Content Version')
        version_class = type('DataDictionaryVersion',
                             (named_list('_DataDictionaryVersion', 'template, content'),),
                             {'__repr__': self.__ver_str,
                              '__str__': self.__ver_str})
        self.__version = version_class(template_version, content_version)
        product_info_class = type('ProductInformation',
                                  (named_list('_ProductInformation', 'name'),),
                                  {'__repr__': self.__product_info_str,
                                   '__str__': self.__product_info_str})
        self.__product_info = product_info_class('NO DEFINE')
        self.format_info = None
        self.interface = None

    @staticmethod
    def __ver_item_str(_self):
        ver_str = '{doc:<30}: {major}.{minor}'.format(doc=_self.doc, major=_self.major, minor=_self.minor)
        return ver_str

    @staticmethod
    def __ver_str(_self):
        ver_str = ''.join('{0!r}\n'.format(item) for item in _self)
        return ver_str.rstrip('\n')

    @staticmethod
    def __product_info_str(_self):
        product_info_str = ''.join('{name:<30}: {value!s}\n'.format(name=fields_name,
                                                                    value=getattr(_self, fields_name))
                                   for fields_name in getattr(_self, '_fields'))
        return product_info_str

    @property
    def ver(self):
        return self.__version
        pass

    @property
    def product_info(self):
        return self.__product_info

    def get_version_info(self, reader):
        for index, row in enumerate(reader):
            try:
                if index >= len(self.__version):
                    continue
                version_text = row[1].strip(' ').upper().lstrip('V').split('.')
                self.__version[index].doc = row[0].strip(' ')
                self.__version[index].major = int(version_text[0])
                self.__version[index].minor = int(version_text[1])
            except IndexError:
                print('ERROR:', 'Can\'t get the version information')
                return False
            except TypeError:
                print('ERROR:', 'Can\'t get the version information')
                return False
                pass
            if reader.line_num >= 2:
                break
            pass
        print('----Version----')
        print(self.ver)
        version_key = '{major}.{minor}'.format(major=self.__version.template.major, minor=self.__version.template.minor)
        try:
            _version = data_dictionary_version_map[version_key]
            _format_info_ver = _version[0]
            _interface_ver = _version[1]

            self.format_info = data_dictionary_format_info[_format_info_ver]
            self.interface = data_dictionary_interface[_interface_ver]
            return True
        except KeyError:
            _latest_ver = latest_data_dictionary_version.split('.')
            _latest_major_ver = int(_latest_ver[0])
            _latest_minor_ver = int(_latest_ver[1])
            if (_latest_major_ver < self.__version.template.major) or\
                    ((_latest_major_ver == self.__version.template.major) and
                        (_latest_minor_ver < self.__version.template.minor)):
                print('WARNING:',  'The template version(' +
                      version_key + ') of the data dictionary is bigger then the supported(' +
                      latest_data_dictionary_version + ') by this application')
                _version = data_dictionary_version_map[latest_data_dictionary_version]
                _format_info_ver = _version[0]
                _interface_ver = _version[1]
                self.format_info = data_dictionary_format_info[_format_info_ver]
                self.interface = data_dictionary_interface[_interface_ver]
                return True
            print('ERROR:', 'The template version(' + version_key + ') of the data dictionary is not supported')
            return False
        except IndexError:
            print('ERROR:', 'The interface and format information version(' +
                  str(data_dictionary_version_map[version_key]) + ') of the data dictionary is not supported')
            return False
        pass

    def get_product_info(self, reader):
        for index, row in enumerate(reader):
            try:
                if index >= len(self.__product_info):
                    continue
                tmp_text = row[1]
                self.__product_info[index] = tmp_text.strip(' ')
            except IndexError:
                print('ERROR:', 'Can\'t get the product information')
                return False
                pass
            if reader.line_num >= 3:
                break
            pass
        print('----Product----')
        print(self.product_info)
        return True
        pass

    @staticmethod
    def get_range_dict(row, offset=0):
        range_dict = OrderedDict()
        index_list = []
        for index, cell in enumerate(row):
            tmp_cell_text = cell.strip(' ')
            tmp_cell_text = tmp_cell_text.strip('\t')

            if tmp_cell_text != '':
                # strip all space characters in header's key
                range_dict[tmp_cell_text] = [index + offset, None]
                index_list.append(index)

            if index + 1 == len(row):
                index_list.append(index + 1)

        index = 0
        for (key, data) in range_dict.items():
            index += 1
            range_dict[key][1] = index_list[index] + offset
        return range_dict

    def get_header_info(self, reader):
        for row in reader:
            if reader.line_num == 4:
                self.header = self.get_range_dict(row)
            elif reader.line_num == 5:
                for (key, data) in self.header.items():
                    if data[0] + 1 < data[1]:
                        tmp_sub_row = row[data[0]:data[1]]
                        sub_dict = self.get_range_dict(tmp_sub_row, data[0])
                        if sub_dict:
                            self.header[key] = sub_dict
                break
        if self.header:
            return True
        else:
            print('ERROR:', 'Can\'t get any header information from the data dictionary file')
            return False
        pass

    def make(self, args):
        for i in range(len(args)):
            args[i] = args[i].strip(' ')
        if self.format_info is None:
            return None
        else:
            info = self.format_info.value
            set_attr_value(info, self.header, args)
            return info
        pass
    pass


def demo_code():
    import csv
    from dditem import data_dictionary_item_text_format
    data_dictionary_manager = DataDictionaryManager()
    try:
        with open('default_data_dictionary.csv', newline='') as csv_file:
            reader = csv.reader(csv_file, dialect='excel')
            try:
                if data_dictionary_manager.get_version_info(reader):
                    data_dictionary_manager.get_product_info(reader)
                    data_dictionary_manager.get_header_info(reader)
                    for record in map(data_dictionary_manager.make, reader):
                        data_dictionary_item = data_dictionary_manager.interface.get_data_dictionary_item(record)
                        if data_dictionary_item is None:
                            print('ERROR:', 'Parse failed in line', reader.line_num)
                            continue
                        print(data_dictionary_item_text_format.format(**data_dictionary_item.__dict__))
                        print('OK:', 'Parse finished in line', reader.line_num)
                        print()
                        pass
            except csv.Error as exception:
                print('ERROR:', 'Parse failed in line', reader.line_num, exception)
    except FileNotFoundError as exception:
        print('ERROR:', exception)
    pass

if __name__ == '__main__':
    demo_code()
    pass
