from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from simulator.uiform.SimulatorUI import Ui_SimulatorUI
from simulator.core.MqttMessagePackage import MqttMessagePackage as DataPackage
import cbor
import json
import sys
from simulator.core.DatagramManager import DatagramManager
from simulator.uiapplication.DatagramTreeViewModel import DatagramTreeViewModel
from simulator.uiapplication.DatagramTreeViewManager import DatagramTreeViewManager

########################################################################################################################
# Main windows class


class MainWin(QMainWindow):
    update_value_signal = pyqtSignal(DataPackage, name='UpdateValueSignal')

    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.ui = Ui_SimulatorUI()
        self.ui.setupUi(self)

        self.data_package = DataPackage()

        self.datagram_manager = DatagramManager()
        self.datagram_manager.import_csv('../datadictionarysource/default_data_dictionary.csv')
        self.datagram_manager.connect_data_server()
        self.datagram_manager.subscribe_all_topic_to_server()
        self.datagram_manager.user_data = self
        self.datagram_manager.update_data_callback = self.update_value_display_callback

        self.datagram_tree_view_model = DatagramTreeViewModel(self.datagram_manager)
        self.datagram_tree_view_manager = DatagramTreeViewManager(self.datagram_manager)
        self.datagram_tree_view_manager.build_list_view(self.datagram_tree_view_model.root_item)

        self.ui.treeViewDataDictionary.setModel(self.datagram_tree_view_model)
        self.ui.treeViewDataDictionary.resizeColumnToContents(0)
        self.ui.treeViewDataDictionary.selectionModel().selectionChanged.connect(
            self.update_datagram_property_display)

        self.update_value_signal.connect(self.update_value_display)

    def update_value_display(self, value_package):
        hash_id = value_package.hash_id
        dev_index = value_package.device_instance_index - 1

        row = self.datagram_tree_view_manager.get_list_view_row(hash_id, dev_index)
        if row is None:
            print('Can\'t find the row')
            return
        model = self.ui.treeViewDataDictionary.model()
        index = model.index(row, 1)
        model.dataChanged.emit(index, index)
        pass

    @staticmethod
    def update_value_display_callback(obj, value_package):
        obj.update_value_signal.emit(value_package)
        pass

    def update_datagram_property_display(self):
        index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        model = self.ui.treeViewDataDictionary.model()
        item = model.get_item(index)
        if not item.parent_item:
            return
        topic = item.data(0)
        hash_id = item.data(2)
        dev_index = item.id

        dg = item.datagram
        self.ui.treeWidgetDataInfo.topLevelItem(0).setText(1, dg.property.sub_system)
        self.ui.treeWidgetDataInfo.topLevelItem(1).setText(1, dg.property.data_path)
        self.ui.treeWidgetDataInfo.topLevelItem(2).setText(1, dg.property.name)
        self.ui.treeWidgetDataInfo.topLevelItem(3).setText(1, dg.property.description)
        self.ui.treeWidgetDataInfo.topLevelItem(4).setText(1, dg.property.type)
        self.ui.treeWidgetDataInfo.topLevelItem(5).setText(1, dg.property.format)
        self.ui.treeWidgetDataInfo.topLevelItem(6).setText(1, str(dg.property.max_size))
        self.ui.treeWidgetDataInfo.topLevelItem(7).setText(1, dg.property.default)
        self.ui.treeWidgetDataInfo.topLevelItem(8).setText(1, str(dg.property.min))
        self.ui.treeWidgetDataInfo.topLevelItem(9).setText(1, str(dg.property.max))
        str_list = []
        str_tmp = ""
        choice_list = dg.property.choice_list
        if choice_list != {}:
            for (k, d) in choice_list.items():
                str_list.append(k + "\t: " + str(d))
            str_list.sort()
            for s in str_list:
                str_tmp = str_tmp + s + '\n'
            str_tmp = str_tmp.rstrip('\n')
        self.ui.treeWidgetDataInfo.topLevelItem(10).setText(1, str_tmp)
        self.ui.treeWidgetDataInfo.topLevelItem(11).setText(1, dg.property.scale_unit)
        self.ui.treeWidgetDataInfo.topLevelItem(12).setText(1, str(dg.property.precision))
        self.ui.treeWidgetDataInfo.topLevelItem(13).setText(1, str(dg.property.is_alarm))
        self.ui.treeWidgetDataInfo.topLevelItem(14).setText(1, str(dg.property.is_evt_log))

        self.ui.treeWidgetDataInfo.topLevelItem(15).setText(1, str(dg.property.producer))
        self.ui.treeWidgetDataInfo.topLevelItem(16).setText(1, str(dg.property.consumer))

        self.ui.treeWidgetDataInfo.topLevelItem(17).setText(1, hex(dg.property.hash_id))
        self.data_package.device_instance_index = dev_index + 1
        self.data_package.hash_id = hash_id
        self.data_package.value = dg.get_value(dev_index)
        self.ui.treeWidgetDataInfo.resizeColumnToContents(1)

        self.ui.textEditValue.setText(self.data_package.to_json_str)
        self.statusBar().showMessage("Clicked: " + topic + " @ " + hex(hash_id))

    @pyqtSlot()
    def on_pushButtonPublish_clicked(self):
        sender = self.sender()
        result = "No topic"
        index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        model = self.ui.treeViewDataDictionary.model()
        item = model.get_item(index)
        if not item.parent_item:
            return
        topic = item.data(0)
        hash_id = item.data(2)
        dev_index = item.id

        try:
            tmp = json.loads(self.ui.textEditValue.toPlainText())
            try:
                self.data_package.payload_type = tmp['E_PAYLOAD_TYPE']
                self.data_package.payload_version = tmp['E_PAYLOAD_VERSION']
                self.data_package.hash_id = hash_id
                self.data_package.producer_mask = tmp['E_PRODUCER_MASK']
                self.data_package.action = tmp['E_ACTION']
                self.data_package.time_stamp_ms = tmp['E_TIMESTAMP_MS']
                self.data_package.time_stamp_second = tmp['E_TIMESTAMP_SECOND']
                self.data_package.device_instance_index = dev_index + 1
                self.data_package.value = tmp['E_VALUE']
                payload = cbor.dumps(self.data_package.value_package)
                self.datagram_manager.send_data_to_server(topic, payload)
            except KeyError as e:
                print('Data package error -> ' + '{}'.format(e))
        except json.decoder.JSONDecodeError:
            print('The input text and the json format mismatch')
            return
        self.statusBar().showMessage(sender.text() + ' was pressed: ' + result)
    pass
########################################################################################################################
sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWin()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("existing")
