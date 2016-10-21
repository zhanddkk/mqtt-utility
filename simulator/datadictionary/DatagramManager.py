import csv
import sys
import json
from simulator.datadictionary.DataProperty import DataProperty
from simulator.datadictionary.Datagram import Datagram

class DatagramManager:
    def __init__(self):
        self.property_index = {}
        self.property_name = []
        self.datagram_list = []
        pass
    # file_name='../datadictionarysource/default_data_dictionary.csv'

    def import_datagram(self, file_name='../datadictionarysource/default_data_dictionary.csv'):
        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            try:
                i = 0
                for row in reader:
                    # print(row)
                    # print(json.loads(row[0]))

                    if i < 2:
                        self.property_name.append(row)
                    else:
                        dg = Datagram(row, self.property_index)
                        self.datagram_list.append(dg)
                        # print(row)
                    if i == 0:
                        for j in range(len(row)):
                            if row[j] and (row[j] != ''):
                                self.property_index[row[j]] = j
                    i += 1
                    pass
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(file_name, reader.line_num, e))
        f.close()

        list_string = "{0;D AC\t}{1; ADCff} {2 ;FBGh}"
        choice_list = {}
        list_string = list_string.expandtabs(0)
        list_string = list_string.replace(' ', '')
        list_string = list_string.replace('{', '')
        list_string = list_string.rstrip('}')
        item = list_string.split('}')

        for cell in item:
            tmp = cell.split(';')
            choice_list[tmp[0]] = tmp[1]
        print(choice_list)

        a = "12.6"
        print(eval(a) + 5)
        pass

    def test(self):
        pass
