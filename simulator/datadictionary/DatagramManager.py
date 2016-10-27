import csv
import sys
from simulator.datadictionary.Datagram import Datagram


class DatagramManager:
    def __init__(self):
        self.property_index = {}
        self.property_name = []
        self.datagram_dict = {}
        self.index_list = []
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


