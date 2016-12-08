import csv
# local file
from simulator.core.Datagram import Datagram
from simulator.core.DataDictionaryInfo import data_dictionary, DataDictionaryInfo
from simulator.core import PayloadPackage


class DatagramManager:
    def __init__(self):
        self.__data_dict = {}  # Datagram dictionary {hash_id: datagram}
        self.__indexes = []  # item = [hash_id, instance, action]
        self.seq_num = 0
        self.value_update_user_data = None
        self.value_update_callback = None
        self.data_dictionary = DataDictionaryInfo()
        pass

    @property
    def index_list(self):
        return self.__indexes

    @property
    def datagram_dict(self):
        return self.__data_dict

    @property
    def len(self):
        return len(self.__indexes)

    def clear(self):
        self.__data_dict.clear()
        self.__indexes.clear()
        self.seq_num = 0
        self.data_dictionary = DataDictionaryInfo()

    def on_message(self, topic, package_msg):
        hash_id = package_msg.hash_id
        instance = package_msg.device_instance_index - 1
        try:
            dg = self.__data_dict[hash_id]
        except KeyError:
            print('WARNING:', 'Can\'t find any datagram which hash ID is', hex(hash_id))
            return
        try:
            d = dg.data_list[instance]
        except IndexError:
            print('ERROR:', 'Can\'t find the data which the device instance is', instance, 'at the datagram')
            return
        d.set_value(package_msg.value, package_msg.action)
        if self.value_update_callback is not None:
            self.value_update_callback(self.value_update_user_data, package_msg)
        pass

    def on_publish(self):
        pass

    def import_csv(self, file_name):
        try:
            with open(file_name, newline='') as csv_file:
                reader = csv.reader(csv_file, dialect='excel')
                try:
                    self.data_dictionary.get_version_info(reader)
                    self.data_dictionary.get_header_info(reader)
                    if self.data_dictionary.ver in data_dictionary:
                        data_dictionary_class = data_dictionary[self.data_dictionary.ver]['data_dictionary_info_class']
                        data_attribute_class = data_dictionary[self.data_dictionary.ver]['datagram_attribute_class']
                        tmp_data_dictionary = data_dictionary_class()
                        tmp_data_dictionary.header = self.data_dictionary.header
                        tmp_data_dictionary.info = self.data_dictionary.info
                        self.data_dictionary = tmp_data_dictionary
                        for record in map(self.data_dictionary.make, reader):
                            attribute = data_attribute_class(record)
                            hash_id = attribute.hash_id
                            datagram = Datagram(attribute)
                            self.__data_dict[hash_id] = datagram
                            for data in datagram.data_list:
                                self.__indexes.append([hash_id,
                                                       data.instance,
                                                       PayloadPackage.E_DATAGRAM_ACTION_PUBLISH])
                                if attribute.type == 'COMMAND':
                                    self.__indexes.append([hash_id,
                                                           data.instance,
                                                           PayloadPackage.E_DATAGRAM_ACTION_RESPONSE])
                                    self.__indexes.append([hash_id,
                                                           data.instance,
                                                           PayloadPackage.E_DATAGRAM_ACTION_ALLOW])
                                    pass
                                elif attribute.type == 'SETTING':
                                    self.__indexes.append([hash_id,
                                                           data.instance,
                                                           PayloadPackage.E_DATAGRAM_ACTION_REQUEST])
                                    self.__indexes.append([hash_id,
                                                           data.instance,
                                                           PayloadPackage.E_DATAGRAM_ACTION_RESPONSE])
                                    self.__indexes.append([hash_id,
                                                           data.instance,
                                                           PayloadPackage.E_DATAGRAM_ACTION_ALLOW])
                                    pass
                            pass
                        return True
                    else:
                        print('ERROR:', 'this simulator not support the dictionary that the version is',
                              self.data_dictionary.ver)
                        return False
                except csv.Error as exception:
                    print('ERROR:', 'in line', reader.line_num, exception)
                    return False
        except FileNotFoundError as exception:
            print('ERROR:', exception)
            return False
        pass
        pass

    def get_datagram(self, hash_id):
        try:
            return self.__data_dict[hash_id]
        except KeyError:
            return None
    pass


if __name__ == "__main__":
    dgm = DatagramManager()
    dgm.import_csv('..\\datadictionarysource\\Full_Interface.CSV')
    print('ok')
    pass
