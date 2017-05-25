import xml.etree.ElementTree as _XmlEt
from ddclient.dgpayload import E_DATAGRAM_ACTION_PUBLISH


class MessageFilterConfig:
    __header_text = '''\
<?xml version="1.0" encoding="UTF-8" ?>
<filter version=\"{version}\" name=\"{name}\" description=\"{description}\">
    <items>
'''

    __end_text = '''\
    </items>
</filter>
'''
    __item_text = '''\
        <item hashId=\"0x{hash_id:>08X}\" deviceIndex=\"{device_index}\"><!--{topic}--></item>\n'''

    def __init__(self, datagram_manager, config_data,
                 version='0.0.1',
                 name='default config',
                 description='This is a default filter config file'):
        self.__dgm = datagram_manager
        self.__config_data = config_data
        self.__version = version
        self.__name = name
        self.__description = description
        pass

    def export_file(self, output_file):
        """
        Export xml file
        :param output_file: file path(include name)
        :return: 
        """
        with open(output_file, mode='w', encoding='utf-8') as output_f:
            output_f.write(self.__header_text.format(version=self.__version,
                                                     name=self.__name,
                                                     description=self.__description))
            # Items' contents
            for _hash_id, _dev_indexes in self.__config_data.items():
                if _dev_indexes:
                    # Get topic from datagram manager
                    _dg = None
                    if self.__dgm:
                        _dg = self.__dgm.get_datagram(hash_id=_hash_id)
                    for _dev_index in _dev_indexes:
                        _topic = 'Topic is not set'
                        if _dg:
                            _dev_data = _dg.get_device_data(_dev_index)
                            if _dev_data:
                                _topic = _dev_data.get_topic(E_DATAGRAM_ACTION_PUBLISH)
                        # print item string to file
                        output_f.write(self.__item_text.format(hash_id=_hash_id,
                                                               device_index=_dev_index + 1,
                                                               topic=_topic))
                pass
            output_f.write(self.__end_text)
            pass
        pass

    def import_file(self, input_file):
        """
        data structure:
        {
            hash id: [device index list],
            ...
        }
        This structure is easy for search
        :param input_file: 
        :return: bool - True(succeed)
        """
        _ret = True
        _tree = _XmlEt.parse(input_file)
        _root = _tree.getroot()
        self.__version = _root.get('version')
        self.__name = _root.get('name')
        self.__description = _root.get('description')
        _items = _root.find('items')
        if _items:
            self.__config_data = {}
            for _item in _items.iter(tag='item'):
                try:
                    _hash_id = int(_item.get('hashId'), base=16)
                    _dev_index = int(_item.get('deviceIndex'), base=10) - 1
                    self.add_item(_hash_id, _dev_index)
                except TypeError:
                    _ret = False
                    break
                    pass
                pass
        else:
            _ret = False
        return _ret
        pass

    def add_item(self, hash_id, device_index):
        if hash_id in self.__config_data:
            _device_indexes = self.__config_data[hash_id]
            if device_index in _device_indexes:
                pass
            else:
                _device_indexes.append(device_index)
                pass
        else:
            self.__config_data[hash_id] = [device_index]
            pass
        pass

    def remove_item(self, hash_id, device_index):
        if hash_id in self.__config_data:
            _device_indexes = self.__config_data[hash_id]
            try:
                _device_indexes.remove(device_index)
                if not _device_indexes:
                    self.__config_data.pop(hash_id)
                    pass
            except ValueError:
                pass
        pass

    def is_item_exist(self, hash_id, device_index):
        try:
            return device_index in self.__config_data[hash_id]
        except KeyError:
            return False
        pass

    @property
    def config_data(self):
        return self.__config_data

    @property
    def version(self):
        return self.__version

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description
    pass


if __name__ == '__main__':
    _config_data = {
        0x00000001: [0, 1, 2],
        0x00000004: [0],
        0x00000007: [0, 1],
    }

    a = MessageFilterConfig(datagram_manager=None, config_data=_config_data)
    a.export_file('test.xml')
    b = MessageFilterConfig(datagram_manager=None, config_data=_config_data)
    b.import_file('test.xml')
    pass
