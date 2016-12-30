from NamedList import named_list


class DataDictionaryFormatInfoV0V10:
    __attribute_name_list = [
        'RootSystem',
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

    __attribute_class = named_list('DatagramAttributeText', __attribute_name_list)
    __producer_class = named_list('ProducerNameText', __producer_name_list)
    __consumer_class = named_list('ConsumerNameText', __consumer_name_list)

    @property
    def value(self):
        producer = self.__producer_class(['No'], ['No'], ['No'], ['No'], ['No'])
        consumer = self.__consumer_class(['No'], ['No'], ['No'], ['No'], ['No'])
        attribute_text = self.__attribute_class(
            [''], [''], [''], [''], ['NO_DEFINE'], ['GENERAL'], ['32BUS'], ['1'], [''], [''], [''], [''],
            ['Sec'], [''], ['No'], ['Yes'], [''], producer, consumer,
            ['0xFFFFFFFF']
        )
        return attribute_text
        pass
    pass

data_dictionary_format_info = {
    '0.10': DataDictionaryFormatInfoV0V10(),
}
