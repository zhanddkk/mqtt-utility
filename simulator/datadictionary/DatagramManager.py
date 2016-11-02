import csv
import sys
from simulator.datadictionary.Datagram import Datagram
import paho.mqtt.publish as publish
from PyQt5.QtCore import pyqtSignal, QObject


class DatagramManager:
    def __init__(self):
        self.property_index = {}
        self.property_name = []
        self.datagram_dict = {}
        self.index_list = []
        self.data_broker = ""
        self.client_name = ""
        pass

    def import_datagram(self, file_name=''):
        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            try:
                i = 0
                for row in reader:
                    if i < 2:
                        self.property_name.append(row)
                    else:
                        dg = Datagram(row, self.property_index)
                        self.datagram_dict[dg.id] = dg
                        for dev_index in range(dg.device_num):
                            self.index_list.append([dg.id, dev_index])
                    if i == 0:
                        for j in range(len(row)):
                            if row[j] and (row[j] != ''):
                                self.property_index[row[j]] = j
                    if i == 1:
                        self.property_index["PropertyNameList"] = self.property_name
                    i += 1
                    pass
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(file_name, reader.line_num, e))
        f.close()
        pass

    def get_datagram(self, hash_id=0):
        return self.datagram_dict[hash_id]
        pass

    def send_value(self, hash_id, dev_index, value):
        dg = self.datagram_dict[hash_id]
        publish.single(dg.get_topic(dev_index), value, hostname=self.data_broker)
        pass

    def get_row(self, hash_id, dev_index):
        is_find = False
        index = 0
        for i in range(len(self.index_list)):
            if (self.index_list[i][0] == hash_id) and (self.index_list[i][1] == dev_index):
                index += i
                is_find = True
                break
        if is_find:
            return index
        else:
            return None
        pass


class DatagramTreeItem(object):
    def __init__(self, dg, parent=None):
        self.parent_item = parent
        self.item_dg = dg
        self.instance = 0
        self.child_items = []
        pass

    def child(self, row):
        return self.child_items[row]

    def child_count(self):
        return len(self.child_items)

    def child_number(self):
        if self.parent_item:
            return self.parent_item.child_item.index(self)
        return 0

    def column_count(self):
        pass
    pass