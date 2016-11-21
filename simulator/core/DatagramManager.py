import csv
from collections import namedtuple

# local file
from simulator.core.Datagram import Datagram
from simulator.core.DatagramAttribute import DatagramAttribute, head_name_list


class DatagramManager:
    def __init__(self):
        self.__data_dict = {}  # Datagram dictionary {hash_id: datagram}
        self.__indexes = []  # item = [hash_id, instance]
        self.value_update_user_data = None
        self.value_update_callback = None
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
        d.value = package_msg.value
        if self.value_update_callback is not None:
            self.value_update_callback(self.value_update_user_data, package_msg)
        pass

    def on_publish(self):
        pass

    def import_csv(self, file_name):
        datagram_property = namedtuple('DatagramRecord', head_name_list)
        try:
            with open(file_name, newline='') as csv_file:
                try:
                    next(csv_file)
                    next(csv_file)
                    reader = csv.reader(csv_file, dialect='excel')
                    for record in map(datagram_property._make, reader):
                        attribute_data = DatagramAttribute(record)
                        hash_id = attribute_data.hash_id
                        datagram = Datagram(attribute_data)
                        self.__data_dict[hash_id] = datagram
                        for data in datagram.data_list:
                            self.__indexes.append([hash_id, data.instance])
                            pass
                    return True
                except csv.Error as e:
                    print('ERROR:', e)
                    return False
        except FileNotFoundError as e:
            print('ERROR:', e)
            return False
        pass

    def get_datagram(self, hash_id):
        try:
            return self.__data_dict[hash_id]
        except KeyError:
            return None
    pass


if __name__ == "__main__":
    dgm = DatagramManager()
    dgm.import_csv('../datadictionarysource/default_data_dictionary.CSV')
    print('ok')
    pass
