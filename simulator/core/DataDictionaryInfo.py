from collections import OrderedDict
from simulator.core.NameClass import NameClass
from simulator.core.DatagramAttribute import DatagramAttributeVer0601


def set_sub_attr_value(obj, range, row, item=None):
    if type(range) is list:
        if item is not None:
            setattr(obj, item, row[range[0]:range[1]])
            pass
        pass
    else:
        obj = getattr(obj, item)
        for obj_attr in obj.fields:
            if obj_attr in range:
                tmp_range = range[obj_attr]
                set_sub_attr_value(obj, tmp_range, row, item=obj_attr)
                pass
        pass
    pass


def set_attr_value(obj, range, row):
    for obj_attr in obj.fields:
        if obj_attr in range:
            tmp_range = range[obj_attr]
            set_sub_attr_value(obj, tmp_range, row, item=obj_attr)
            pass
    pass


class DataDictionaryInfo:
    def __init__(self):
        self.header = OrderedDict()
        self.info = OrderedDict()

    @property
    def ver(self):
        ver_text = ''
        try:
            ver_text = self.info['Master Template Version'] + self.info['Data Dictionary Version']
        except KeyError:
            pass
        return ver_text.replace('_', '')
        pass

    def get_version_info(self, reader):
        for row in reader:
            try:
                self.info[row[0]] = row[1]
            except KeyError:
                pass
            if reader.line_num >= 3:
                break

        print('Data Dictionary Version: ', self.ver)
        pass

    @staticmethod
    def get_range_dict(row, offset=0):
        range_dict = OrderedDict()
        index_list = []
        for index, cell in enumerate(row):
            tmp_cell_text = cell.strip(' ')
            tmp_cell_text = tmp_cell_text.strip('\t')

            if tmp_cell_text != '':
                range_dict[cell] = [index + offset, None]
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
                        self.header[key] = self.get_range_dict(tmp_sub_row, data[0])
                break
        pass
    pass


class DataDictionaryInfoVer0601(DataDictionaryInfo):
    __attribute_name_list = [
        'SubSystem',
        'DataPath',
        'Name',
        'Description',
        'Type',
        'Format',
        'MaxSize',
        'Default',
        'Min',
        'Max',
        'ChoiceList',
        'ScaleUnit',
        'Precision',
        'IsAlarm',
        'IsEvtLog',
        'CmdTimeOut',
        'Producer',
        'Consumer',
        'HashID'
    ]

    __producer_name_list = ['UC', 'SLC_UPS', 'SLC_NMC', 'HMI', 'Tuner']
    __consumer_name_list = ['UC', 'SLC_UPS', 'SLC_NMC', 'HMI', 'Tuner']

    __attribute_class = NameClass('DatagramAttributeText', __attribute_name_list).new_class
    __producer_class = NameClass('ProducerNameText', __producer_name_list).new_class
    __consumer_class = NameClass('ConsumerNameText', __consumer_name_list).new_class

    def make(self, *args):
        producer = self.__producer_class('No', 'No', 'No', 'No', 'No')
        consumer = self.__consumer_class('No', 'No', 'No', 'No', 'No')
        attribute_text = self.__attribute_class(
            '', '', '', 'name', 'GENERAL', '32BUS', '1', '', '', '', '',
            'Sec', '', 'No', 'Yes', '', producer, consumer,
            '0xFFFFFFFF'
        )
        set_attr_value(attribute_text, self.header, args[0])
        return attribute_text
    pass

data_dictionary = {
    '0601': {
        'data_dictionary_info_class': DataDictionaryInfoVer0601,
        'datagram_attribute_class': DatagramAttributeVer0601,
    }
}

if __name__ == '__main__':
    pass
