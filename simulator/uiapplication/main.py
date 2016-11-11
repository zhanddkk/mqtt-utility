# from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QFileDialog
# import cbor
# import json
import sys
import os
(file_path_base, filename) = os.path.split(os.path.realpath(__file__))
file_path = os.path.join(file_path_base, '..\\..\\')
sys.path.append(file_path)
########################################################################################################################
# Main windows class


class MainWin(QMainWindow):
    from simulator.core.MqttMessagePackage import MqttMessagePackage as DataPackage
    update_value_signal = pyqtSignal(DataPackage, name='UpdateValueSignal')

    def __init__(self, parent=None):
        from simulator.core.MqttMessagePackage import MqttMessagePackage as DataPackage
        from simulator.uiform.SimulatorUI import Ui_SimulatorUI
        from simulator.core.DatagramManager import DatagramManager
        from simulator.uiapplication.DatagramTreeViewModel import DatagramTreeViewModel
        from simulator.uiapplication.DatagramTreeViewManager import DatagramTreeViewManager
        super(MainWin, self).__init__(parent)
        self.ui = Ui_SimulatorUI()
        self.ui.setupUi(self)

        self.data_package = DataPackage()

        self.datagram_manager = DatagramManager()
        # self.datagram_manager.broker = '192.168.1.102'
        self.datagram_manager.connect_data_server()
        self.datagram_manager.user_data = self
        self.datagram_manager.update_data_callback = self.update_value_display_callback

        self.datagram_tree_view_model = DatagramTreeViewModel(self.datagram_manager)
        self.datagram_tree_view_manager = DatagramTreeViewManager(self.datagram_manager)

        self.update_value_signal.connect(self.update_value_display)

        self.ui.action_Exit.triggered.connect(QApplication.instance().quit)
        self.ui.action_Load_CSV.triggered.connect(self.load_csv)
        self.ui.treeWidgetDataInfo.resizeColumnToContents(0)
        self.ui.treeWidgetPackageInfo.resizeColumnToContents(0)

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

        model = self.ui.treeViewValueDisplay.model()
        if model:
            model.update()
            self.ui.treeViewValueDisplay.reset()
        pass

    def load_csv(self):
        fdg = QFileDialog()
        csv_file_path = os.path.join(file_path_base, '../datadictionarysource/')
        fdg.setDirectory(csv_file_path)
        fdg.setNameFilter("CSV Files (*.csv);;Text Files (*.txt);;All Files (*)")
        if fdg.exec():
            self.ui.treeViewDataDictionary.setModel(None)
            self.datagram_tree_view_manager.clear()
            self.datagram_tree_view_manager.load_data_from_csv(fdg.selectedFiles()[0])
            self.datagram_tree_view_manager.build_list_view(self.datagram_tree_view_model.root_item)
            self.ui.treeViewDataDictionary.setModel(self.datagram_tree_view_model)
            self.ui.treeViewDataDictionary.selectionModel().selectionChanged.connect(
                self.update_datagram_property_display)
            self.ui.treeViewDataDictionary.resizeColumnToContents(0)
            pass
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
        hash_id = item.datagram.id
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
        choice_list_item = self.ui.treeWidgetDataInfo.topLevelItem(10)
        choice_list_item.takeChildren()
        choice_list = dg.property.choice_list
        if choice_list != {}:
            choice_list_item.setText(1, '...')
            for (k, d) in choice_list.items():
                str_list.append(k)
            str_list.sort()
            for s in str_list:
                sub_item = QTreeWidgetItem([s, str(choice_list[s])])
                choice_list_item.addChild(sub_item)
            self.ui.treeWidgetDataInfo.expandItem(choice_list_item)
        else:
            choice_list_item.setText(1, '')

        self.ui.treeWidgetDataInfo.topLevelItem(11).setText(1, dg.property.scale_unit)
        self.ui.treeWidgetDataInfo.topLevelItem(12).setText(1, str(dg.property.precision))
        self.ui.treeWidgetDataInfo.topLevelItem(13).setText(1, str(dg.property.is_alarm))
        self.ui.treeWidgetDataInfo.topLevelItem(14).setText(1, str(dg.property.is_evt_log))

        self.ui.treeWidgetDataInfo.topLevelItem(15).setText(1, str(dg.property.producer))
        self.ui.treeWidgetDataInfo.topLevelItem(16).setText(1, str(dg.property.consumer))

        hash_str = '0x' + '{:0>8}'.format(hex(hash_id)[2:].upper())

        self.ui.treeWidgetDataInfo.topLevelItem(17).setText(1, hash_str)

        self.data_package.device_instance_index = dev_index + 1
        self.data_package.hash_id = hash_id
        self.data_package.value = dg.get_value(dev_index)
        self.ui.treeWidgetDataInfo.resizeColumnToContents(0)

        self.ui.treeWidgetPackageInfo.topLevelItem(0).setText(1, str(self.data_package.payload_type))
        self.ui.treeWidgetPackageInfo.topLevelItem(1).setText(1, str(self.data_package.payload_version))
        self.ui.treeWidgetPackageInfo.topLevelItem(2).setText(1, hash_str)
        # self.ui.treeWidgetPackageInfo.topLevelItem(3).setData(1, 0, self.data_package.producer_mask)
        self.ui.treeWidgetPackageInfo.topLevelItem(3).setText(1, str(self.data_package.producer_mask))
        self.ui.treeWidgetPackageInfo.topLevelItem(4).setText(1, str(self.data_package.action))
        self.ui.treeWidgetPackageInfo.topLevelItem(5).setText(1, str(self.data_package.time_stamp_ms))
        self.ui.treeWidgetPackageInfo.topLevelItem(6).setText(1, str(self.data_package.time_stamp_second))
        self.ui.treeWidgetPackageInfo.topLevelItem(7).setText(1, str(self.data_package.device_instance_index))

        from simulator.uiapplication.GeneralValueDspTreeViewModel import GeneralValueDspTreeViewModel
        from simulator.uiapplication.GeneralValueEditTreeViewModel import GeneralValueEditTreeViewModel
        from simulator.uiapplication.DictionaryValueDspTreeModel import DictionaryValueDspTreeModel
        from simulator.uiapplication.DictionaryValueEditTreeModel import DictionaryValueEditTreeModel
        from simulator.uiapplication.ListValueDspTreeModel import ListValueDspTreeModel
        from simulator.uiapplication.ListValueEditTreeModel import ListValueEditTreeModel
        from simulator.uiapplication.DictionaryTreeViewDelegate import DictionaryTreeViewDelegate
        from simulator.uiapplication.ListTreeViewDelegate import ListTreeViewDelegate

        if dg.property.type == 'STATUS':
            value_dsp_model = DictionaryValueDspTreeModel(dg, dev_index)
            value_edit_model = DictionaryValueEditTreeModel(dg, dev_index)
            value_edit_delegate = DictionaryTreeViewDelegate(dg)
        elif dg.property.type == 'MEASURE':
            value_dsp_model = ListValueDspTreeModel(dg, dev_index)
            value_edit_model = ListValueEditTreeModel(dg, dev_index)
            value_edit_delegate = ListTreeViewDelegate(dg)
        else:
            value_dsp_model = GeneralValueDspTreeViewModel(dg, dev_index)
            value_edit_model = GeneralValueEditTreeViewModel(dg, dev_index)
            value_edit_delegate = ListTreeViewDelegate(dg)

        self.ui.treeViewValueEdit.setItemDelegate(value_edit_delegate)
        self.ui.treeViewValueDisplay.setModel(value_dsp_model)
        self.ui.treeViewValueEdit.setModel(value_edit_model)
        self.statusBar().showMessage("Clicked: " + topic + " @ " + hash_str)

    @pyqtSlot()
    def on_pushButtonPublish_clicked(self):
        sender = self.sender()
        try:
            index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        except AttributeError:
            self.statusBar().showMessage(sender.text() + ' was pressed: No Topic')
            return
            pass
        model = self.ui.treeViewDataDictionary.model()
        item = model.get_item(index)
        if not item.parent_item:
            self.statusBar().showMessage(sender.text() + ' was pressed: No Topic')
            return
        hash_id = item.datagram.id
        dev_index = item.id

        model = self.ui.treeViewValueEdit.model()
        if not model:
            self.statusBar().showMessage(sender.text() + ' was pressed: Invalid Value Type')
            return

        self.data_package.value = model.get_value()
        try:
            self.data_package.payload_type = int(self.ui.treeWidgetPackageInfo.topLevelItem(0).text(1))
            self.data_package.payload_version = int(self.ui.treeWidgetPackageInfo.topLevelItem(1).text(1))
            self.data_package.action = int(self.ui.treeWidgetPackageInfo.topLevelItem(4).text(1))
            self.data_package.time_stamp_ms = int(self.ui.treeWidgetPackageInfo.topLevelItem(5).text(1))
            self.data_package.time_stamp_second = int(self.ui.treeWidgetPackageInfo.topLevelItem(6).text(1))
            pass
        except TypeError:
            pass
        if self.datagram_manager.send_data_to_server(hash_id, dev_index, self.data_package):
            result = 'Send OK'
        else:
            result = 'Send Failed'
        self.statusBar().showMessage(sender.text() + ' was pressed: ' + result)
    pass
########################################################################################################################
sys.except_hook = sys.excepthook


def exception_hook(exc_type, value, traceback):
    sys.except_hook(exc_type, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec_())
