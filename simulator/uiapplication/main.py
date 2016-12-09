########################################################################################################################
# Simulation main application
########################################################################################################################
import os as _os
import sys
import datetime
from PyQt5.Qt import Qt
from PyQt5.QtCore import QDir
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFontMetrics

_path = _os.path.dirname(__file__)
_path = _os.path.join(_path, '../../')
sys.path.append(_path)


class MainWin(QMainWindow):
    from simulator.core.PayloadPackage import PayloadPackage
    update_datagram_info_display_signal = pyqtSignal(list, name='UpdateDatagramInfoDisplaySignal')
    update_datagram_value_display_signal = pyqtSignal(PayloadPackage, name='UpdateDatagramValueDisplaySignal')
    record_datagram_server_message_signal = pyqtSignal(str, name='RecordDatagramServerMessageSignal')

    def __init__(self, parent=None):
        from simulator.uiapplication.WinMainUi import Ui_MainWindow
        from simulator.uiapplication.DataMonitorTableViewModel import DataMonitorTableViewModel
        from simulator.uiapplication.DataDictionaryTreeViewModel import DataDictionaryTreeViewModel

        from simulator.core.NameClass import NameClass
        cmd_bit_format_class = NameClass('CmdBitFormatClass', 'Producer, Sequence, AckCmdCode').new_class
        setting_response_bit_format_class = NameClass('SettingRespBitFormatClass', 'Producer, ErrorCode').new_class

        self.cmd_bit_format = cmd_bit_format_class(Producer=[8, {0: 'UC', 1: 'SLC_UPS', 2: 'SLC_NMC',
                                                                 3: 'HMI', 4: 'TUNER'}],
                                                   Sequence=[16, None],
                                                   AckCmdCode=[8, {0: 'Rest', 1: 'Set', 0x10: 'Idle',
                                                               0x11: 'Receive',
                                                               0x12: 'Completed',
                                                               0x13: 'Locked',
                                                               0x14: 'Refused'}])
        self.setting_response_bit_format = setting_response_bit_format_class(Producer=[16, {0: 'UC',
                                                                                       1: 'SLC_UPS',
                                                                                       2: 'SLC_NMC',
                                                                                       3: 'HMI',
                                                                                       4: 'TUNER'}],
                                                                             ErrorCode=[16, {0: 'OK'}])

        super(MainWin, self).__init__(parent, flags=Qt.Window)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionExit.triggered.connect(QApplication.instance().quit)
        self.ui.actionImport.triggered.connect(self.import_csv)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionSettings.triggered.connect(self.setting)
        self.ui.actionConnect_Broker.triggered.connect(self.connect_mqtt)

        self.tabifyDockWidget(self.ui.package_dock_widget, self.ui.repeater_dock_widget)
        self.ui.package_dock_widget.raise_()
        self.ui.data_monitor_table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.__add_view_menu_items()

        from simulator.uiapplication.Configuration import Configuration

        self.configuration = Configuration()
        self.configuration.read_config()

        from simulator.core.DatagramManager import DatagramManager
        from simulator.core.PayloadPackage import PayloadPackage
        from simulator.core.DatagramServer import DatagramServer
        from simulator.core.Repeater import Repeater

        self.datagram_manager = DatagramManager()
        self.datagram_manager.value_update_user_data = self
        self.datagram_manager.value_update_callback = self.update_datagram_value_display_callback
        self.current_datagram_index = None

        self.payload_package = PayloadPackage()

        self.datagram_server = DatagramServer(self.datagram_manager)
        self.datagram_server.record_message_user_data = self
        self.datagram_server.record_message_callback = self.record_datagram_server_message_callback

        self.datagram_repeater = Repeater(self.datagram_server, 0.1)
        self.datagram_repeater.start()

        self.datagram_manager_tree_view_model = DataDictionaryTreeViewModel(self.datagram_manager)
        self.data_monitor_table_view_model = DataMonitorTableViewModel(self.datagram_manager)

        self.ui.data_dictionary_tree_view.setModel(self.datagram_manager_tree_view_model)
        self.ui.data_monitor_table_view.setModel(self.data_monitor_table_view_model)

        self.ui.data_dictionary_tree_view.selectionModel().selectionChanged.connect(
            self.data_dictionary_tree_view_item_selected)
        self.ui.data_monitor_table_view.selectionModel().selectionChanged.connect(
            self.data_monitor_table_view_item_selected)
        self.update_datagram_info_display_signal.connect(self.update_datagram_info_display)
        self.update_datagram_value_display_signal.connect(self.update_datagram_value_display)
        self.record_datagram_server_message_signal.connect(self.record_datagram_server_message)

    def __add_view_menu_items(self):
        self.ui.menuView.addAction(self.ui.data_dictionary_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.menuView.addAction(self.ui.data_attribute_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.menuView.addAction(self.ui.package_dock_widget.toggleViewAction())
        self.ui.menuView.addAction(self.ui.repeater_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.menuView.addAction(self.ui.data_history_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.menuView.addAction(self.ui.log_dock_widget.toggleViewAction())
        pass

    def about(self):
        msg_dlg = QMessageBox()
        data_dictionary_info_text = '<p>----------Data Dictionary Info----------</p>'
        for (key, data) in self.datagram_manager.data_dictionary.info.items():
            data_dictionary_info_text += '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; ' \
                                         'margin-right:0px; -qt-block-indent:0; text-indent:0px;\">' \
                                         '<span style=\" font-weight:600;\">' + key + '</span> : ' +\
                                         data.replace('_', '.') + \
                                         '</p>'
            pass

        msg_dlg.about(self, "About Application", '''<p>----------Application Info----------</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;-qt-block-indent:0; text-indent:0px;">
    This <span style=" font-weight:600;">Application</span> is a simulator.
</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
    <span style=" font-weight:600;">Version</span> : 0.5.1
</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
    <span style=" font-weight:600;">Copyright</span> :
    <span style=" font-style:italic; text-decoration: underline; color:#3bb300;"> Schneider Electric (China) Co., Ltd.
    </span>
</p>''' + data_dictionary_info_text)
        pass

    def quit(self):
        self.datagram_repeater.stop()
        self.datagram_server.stop()
        QApplication.instance().quit()
        pass

    def import_csv(self):
        fdg = QFileDialog()
        q_dir = QDir('../datadictionarysource/')
        csv_path = q_dir.absolutePath()
        fdg.setDirectory(csv_path)
        fdg.setNameFilter("CSV Files (*.csv);;Text Files (*.txt);;All Files (*)")
        if fdg.exec():

            self.data_monitor_table_view_model.beginResetModel()
            self.datagram_manager.clear()
            self.datagram_manager.import_csv(fdg.selectedFiles()[0])
            self.datagram_manager_tree_view_model.update()
            self.data_monitor_table_view_model.endResetModel()

            self.ui.data_monitor_table_view.resizeColumnsToContents()

            font = self.ui.data_monitor_table_view.font()
            font_metrics = QFontMetrics(font)
            font_height = font_metrics.height() + 4
            for i in range(self.data_monitor_table_view_model.rowCount()):
                self.ui.data_monitor_table_view.setRowHeight(i, font_height)

            self.statusBar().showMessage(fdg.selectedFiles()[0])
            pass
        pass

    def setting(self):
        from simulator.uiapplication.SettingDlg import SettingDlg
        set_dlg = SettingDlg(self.configuration)
        set_dlg.exec()

    def connect_mqtt(self):
        if self.ui.actionConnect_Broker.isChecked():
            if self.datagram_server.is_running:
                self.statusBar().showMessage('Is Connected')
                pass
            else:
                self.datagram_server.broker = self.configuration.mqtt_connect_addr
                self.datagram_server.port = self.configuration.mqtt_connect_port
                self.statusBar().showMessage('Connecting...')
                ret_val = self.datagram_server.run()
                self.ui.actionConnect_Broker.setChecked(ret_val)
                if ret_val is False:
                    msg_dlg = QMessageBox()
                    msg_dlg.critical(self, 'Connect Error',
                                     'Can\'t connect to the broker'
                                     '<p><b>Address:</b> ' + self.datagram_server.broker + '</p>'
                                     '<p><b>Port:</b> ' + str(self.datagram_server.port) + '</p>',
                                     QMessageBox.Ok)
                    self.statusBar().showMessage('Connect Failed')
                else:
                    self.statusBar().showMessage('Connected@' + self.datagram_server.broker + ':' +
                                                 str(self.datagram_server.port))
                    pass
        else:
            if self.datagram_server.is_running:
                self.datagram_server.stop()
                self.statusBar().showMessage('Disconnected')
        pass

    def data_dictionary_tree_view_item_selected(self):
        item_index = self.ui.data_dictionary_tree_view.selectionModel().currentIndex()
        model = self.ui.data_dictionary_tree_view.model()
        item = model.get_item(item_index)
        if item.hide_data is None:
            return
        else:
            model = self.ui.data_monitor_table_view.model()
            row = model.datagram_index.index(item.hide_data)
            row_index = model.index(row, 0)
            self.ui.data_monitor_table_view.setCurrentIndex(row_index)
            self.ui.data_monitor_table_view.scrollTo(row_index)
        pass

    def data_monitor_table_view_item_selected(self):
        model = self.ui.data_monitor_table_view.model()
        item_index = self.ui.data_monitor_table_view.selectionModel().currentIndex()
        row = item_index.row()
        self.update_datagram_info_display_signal.emit(model.datagram_index[row])
        pass

    def update_datagram_info_display(self, index):
        self.current_datagram_index = index
        dg = self.datagram_manager.datagram_dict[index[0]]
        d = dg.data_list[index[1]]
        self.ui.data_attribute_tree_widget.topLevelItem(0).setText(1, dg.attribute.sub_system)
        self.ui.data_attribute_tree_widget.topLevelItem(1).setText(1, dg.attribute.data_path)
        self.ui.data_attribute_tree_widget.topLevelItem(2).setText(1, dg.attribute.name)
        self.ui.data_attribute_tree_widget.topLevelItem(3).setText(1, dg.attribute.description)
        self.ui.data_attribute_tree_widget.topLevelItem(4).setText(1, dg.attribute.type)
        self.ui.data_attribute_tree_widget.topLevelItem(5).setText(1, dg.attribute.format)
        self.ui.data_attribute_tree_widget.topLevelItem(6).setText(1, str(dg.attribute.max_size))
        self.ui.data_attribute_tree_widget.topLevelItem(7).setText(1, str(dg.attribute.default))
        self.ui.data_attribute_tree_widget.topLevelItem(8).setText(1, str(dg.attribute.min))
        self.ui.data_attribute_tree_widget.topLevelItem(9).setText(1, str(dg.attribute.max))
        choice_list_item = self.ui.data_attribute_tree_widget.topLevelItem(10)
        choice_list_item.takeChildren()
        choice_list = dg.attribute.choice_list
        if choice_list is not None:
            choice_list_item.setText(1, '...')
            for (key, choice_item_data) in choice_list.items():
                sub_item = QTreeWidgetItem([key, str(choice_item_data[0])])
                choice_list_item.addChild(sub_item)
            self.ui.data_attribute_tree_widget.expandItem(choice_list_item)
        else:
            choice_list_item.setText(1, '')
        self.ui.data_attribute_tree_widget.topLevelItem(11).setText(1, dg.attribute.scale_unit)
        self.ui.data_attribute_tree_widget.topLevelItem(12).setText(1, str(dg.attribute.precision))
        self.ui.data_attribute_tree_widget.topLevelItem(13).setText(1, str(dg.attribute.is_alarm))
        self.ui.data_attribute_tree_widget.topLevelItem(14).setText(1, str(dg.attribute.is_evt_log))
        self.ui.data_attribute_tree_widget.topLevelItem(15).setText(1, str(dg.attribute.cmd_time_out))
        self.ui.data_attribute_tree_widget.topLevelItem(16).setText(1, str(dg.attribute.producer))
        self.ui.data_attribute_tree_widget.topLevelItem(17).setText(1, str(dg.attribute.consumer))
        hash_str = '0x' + '{0:0>8}'.format(hex(index[0])[2:].upper())
        self.ui.data_attribute_tree_widget.topLevelItem(18).setText(1, hash_str)
        self.ui.data_attribute_tree_widget.resizeColumnToContents(0)

        self.payload_package.hash_id = index[0]
        self.payload_package.device_instance_index = index[1] + 1

        from simulator.core import PayloadPackage

        self.ui.topic_line_edit.setText(d.get_topic(index[2]))

        select_list = PayloadPackage.payload_package_item_info[PayloadPackage.E_PAYLOAD_TYPE][1]
        if self.payload_package.payload_type in select_list:
            select_index = self.ui.payload_type_combo_box.findText(str(self.payload_package.payload_type) + ' | ' +
                                                                   select_list[self.payload_package.payload_type])
            if select_index != -1:
                self.ui.payload_type_combo_box.setCurrentIndex(select_index)
            else:
                self.ui.payload_type_combo_box.setCurrentText(str(self.payload_package.payload_type))
        else:
            self.ui.payload_type_combo_box.setCurrentText(str(self.payload_package.payload_type))

        self.ui.payoad_version_line_edit.setText(str(self.payload_package.payload_version))
        self.ui.hash_id_line_edit.setText(hash_str)

        select_list = PayloadPackage.payload_package_item_info[PayloadPackage.E_PRODUCER_MASK][1]
        if self.payload_package.producer_mask in select_list:
            select_index = self.ui.producer_mask_combo_box.findText(str(self.payload_package.producer_mask) + ' | ' +
                                                                    select_list[self.payload_package.producer_mask])
            if select_index != -1:
                self.ui.producer_mask_combo_box.setCurrentIndex(select_index)
            else:
                self.ui.producer_mask_combo_box.setCurrentText(str(self.payload_package.producer_mask))
        else:
            self.ui.producer_mask_combo_box.setCurrentText(str(self.payload_package.producer_mask))

        select_list = PayloadPackage.payload_package_item_info[PayloadPackage.E_ACTION][1]
        self.payload_package.action = index[2]
        if self.payload_package.action in select_list:
            select_index = self.ui.action_combo_box.findText(str(self.payload_package.action) + ' | ' +
                                                             select_list[self.payload_package.action])
            if select_index != -1:
                self.ui.action_combo_box.setCurrentIndex(select_index)
            else:
                self.ui.action_combo_box.setCurrentText(str(self.payload_package.action))
        else:
            self.ui.action_combo_box.setCurrentText(str(self.payload_package.action))
        self.ui.time_stamp_s_line_edit.setText(str(self.payload_package.time_stamp_second))
        self.ui.time_stamp_ms_line_edit.setText(str(self.payload_package.time_stamp_ms))
        self.ui.device_index_line_edit.setText(str(self.payload_package.device_instance_index))
        self.ui.reference_type_line_edit.setText(str(self.payload_package.data_object_reference_type))
        self.ui.reference_value_line_edit.setText(str(self.payload_package.data_object_reference_value))

        self.ui.interval_spin_box.setValue(d.repeater_info.tagger_count)
        self.ui.repeate_times_spin_box.setValue(d.repeater_info.exit_times)
        self.ui.user_function_plain_text_edit.setPlainText(d.repeater_info.user_function_str)

        if d.repeater_info.is_running is True:
            self.ui.repeater_push_button.setText('Stop')
            self.ui.publish_push_button.setEnabled(False)
        else:
            self.ui.repeater_push_button.setText('Start')
            self.ui.publish_push_button.setEnabled(True)
        pass

        self.statusBar().showMessage('Hash Id : ' + hash_str + ' | Device index : ' + str(index[1] + 1))

        from simulator.uiapplication.GeneralValueDspTreeViewModel import GeneralValueDspTreeViewModel
        from simulator.uiapplication.GeneralValueEditTreeViewModel import GeneralValueEditTreeViewModel
        from simulator.uiapplication.GeneralTreeViewDelegate import GeneralTreeViewDelegate

        from simulator.uiapplication.DictionaryValueDspTreeModel import DictionaryValueDspTreeModel
        from simulator.uiapplication.DictionaryValueEditTreeModel import DictionaryValueEditTreeModel
        from simulator.uiapplication.DictionaryTreeViewDelegate import DictionaryTreeViewDelegate

        from simulator.uiapplication.ListValueDspTreeModel import ListValueDspTreeModel
        from simulator.uiapplication.ListValueEditTreeModel import ListValueEditTreeModel

        from simulator.uiapplication.StructValueDspModel import StructValueDspModel
        from simulator.uiapplication.StructValueEditModel import StructValueEditModel
        from simulator.uiapplication.StructTreeViewDelegate import StructTreeViewDelegate

        from simulator.uiapplication.BitMapValueDspModel import BitMapValueDspModel
        from simulator.uiapplication.BitMapValueEditModel import BitMapValueEditModel
        from simulator.uiapplication.BitMapDelegate import BitMapDelegate

        if dg.attribute.type == 'COMMAND':
            if index[2] == PayloadPackage.E_DATAGRAM_ACTION_PUBLISH:
                value = d.get_value(index[2])
                value &= 0xff0000ff
                value |= 0x00ffff00 & (self.datagram_manager.seq_num << 8)
                value_dsp_model = BitMapValueDspModel(dg, index, self.cmd_bit_format)
                value_edit_model = BitMapValueEditModel(dg, index, self.cmd_bit_format, value)
                value_edit_delegate = BitMapDelegate(dg, self.cmd_bit_format)
                pass
            elif index[2] == PayloadPackage.E_DATAGRAM_ACTION_RESPONSE:
                value_dsp_model = BitMapValueDspModel(dg, index, self.cmd_bit_format)
                value_edit_model = BitMapValueEditModel(dg, index, self.cmd_bit_format)
                value_edit_delegate = BitMapDelegate(dg, self.cmd_bit_format)
                pass
            else:
                value_dsp_model = GeneralValueDspTreeViewModel(dg, index[1], index[2])
                value_edit_model = GeneralValueEditTreeViewModel(dg, index[1], index[2])
                value_edit_delegate = GeneralTreeViewDelegate(dg)
            pass
        elif dg.attribute.type == 'SETTING':
            if index[2] == PayloadPackage.E_DATAGRAM_ACTION_RESPONSE:
                value_dsp_model = BitMapValueDspModel(dg, index, self.setting_response_bit_format)
                value_edit_model = BitMapValueEditModel(dg, index, self.setting_response_bit_format)
                value_edit_delegate = BitMapDelegate(dg, self.setting_response_bit_format)
                pass
            elif index[2] == PayloadPackage.E_DATAGRAM_ACTION_ALLOW:
                value_dsp_model = GeneralValueDspTreeViewModel(dg, index[1], index[2])
                value_edit_model = GeneralValueEditTreeViewModel(dg, index[1], index[2])
                value_edit_delegate = GeneralTreeViewDelegate(dg)
                pass
            else:
                if dg.attribute.format == 'Enum':
                    value_dsp_model = DictionaryValueDspTreeModel(dg, index[1])
                    value_edit_model = DictionaryValueEditTreeModel(dg, index[1])
                    value_edit_delegate = DictionaryTreeViewDelegate(dg)
                elif dg.attribute.format == 'Structure':
                    value_dsp_model = StructValueDspModel(dg, index[1])
                    value_edit_model = StructValueEditModel(dg, index[1])
                    value_edit_delegate = StructTreeViewDelegate(dg)
                    pass
                else:
                    if dg.attribute.length > 1:
                        value_dsp_model = ListValueDspTreeModel(dg, index[1])
                        value_edit_model = ListValueEditTreeModel(dg, index[1])
                        value_edit_delegate = GeneralTreeViewDelegate(dg)
                        pass
                    else:
                        value_dsp_model = GeneralValueDspTreeViewModel(dg, index[1])
                        value_edit_model = GeneralValueEditTreeViewModel(dg, index[1])
                        value_edit_delegate = GeneralTreeViewDelegate(dg)
                        pass
                    pass
                value_dsp_model.action = index[2]
                value_edit_model.action = index[2]
                pass
            pass
        elif dg.attribute.type == 'STATUS':
            value_dsp_model = DictionaryValueDspTreeModel(dg, index[1])
            value_edit_model = DictionaryValueEditTreeModel(dg, index[1])
            value_edit_delegate = DictionaryTreeViewDelegate(dg)
            pass
        else:
            if dg.attribute.format == 'Enum':
                value_dsp_model = DictionaryValueDspTreeModel(dg, index[1])
                value_edit_model = DictionaryValueEditTreeModel(dg, index[1])
                value_edit_delegate = DictionaryTreeViewDelegate(dg)
            elif dg.attribute.format == 'Structure':
                value_dsp_model = StructValueDspModel(dg, index[1])
                value_edit_model = StructValueEditModel(dg, index[1])
                value_edit_delegate = StructTreeViewDelegate(dg)
                pass
            else:
                if dg.attribute.length > 1:
                    value_dsp_model = ListValueDspTreeModel(dg, index[1])
                    value_edit_model = ListValueEditTreeModel(dg, index[1])
                    value_edit_delegate = GeneralTreeViewDelegate(dg)
                    pass
                else:
                    value_dsp_model = GeneralValueDspTreeViewModel(dg, index[1])
                    value_edit_model = GeneralValueEditTreeViewModel(dg, index[1])
                    value_edit_delegate = GeneralTreeViewDelegate(dg)
                    pass
                pass

        self.ui.data_history_tree_view.setModel(value_dsp_model)
        self.ui.value_edit_tree_view.setModel(value_edit_model)
        self.ui.value_edit_tree_view.setItemDelegate(value_edit_delegate)
        self.ui.value_edit_tree_view.resizeColumnToContents(0)

    def update_datagram_value_display(self, payload_package):
        hash_id = payload_package.hash_id
        dev_index = payload_package.device_instance_index - 1
        model = self.ui.data_monitor_table_view.model()
        if model is None:
            return
        try:
            row = model.datagram_index.index([hash_id, dev_index, payload_package.action])
        except ValueError:
            return
        model_index = model.index(row, 2)
        model.dataChanged.emit(model_index, model_index)

        model = self.ui.data_history_tree_view.model()
        if model is not None:
            if (model.datagram.attribute.hash_id != hash_id) or\
                    ((model.datagram.attribute.hash_id == hash_id) and (model.dev_index != dev_index)):
                return
            model.update()
        pass

    def record_datagram_server_message(self, msg_str):
        self.ui.log_plain_text_edit.appendPlainText('--------' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                                                    '--------\n' + msg_str)
        pass

    @pyqtSlot()
    def on_repeater_push_button_clicked(self):
        sender = self.sender()
        try:
            item_index = self.ui.data_monitor_table_view.selectionModel().currentIndex()
            model = self.ui.data_monitor_table_view.model()
            row = item_index.row()
            index = model.datagram_index[row]
            dg = self.datagram_manager.datagram_dict[index[0]]
            d = dg.data_list[index[1]]

            if d.repeater_info.is_running is True:
                self.datagram_repeater.remove_data(index)
                self.statusBar().showMessage(sender.text() + ' OK')
                self.ui.repeater_push_button.setText('Start')
                self.ui.publish_push_button.setEnabled(True)
                pass
            else:
                d.repeater_info.tagger_count = self.ui.interval_spin_box.value()
                if d.repeater_info.tagger_count > 0:
                    d.repeater_info.exit_times = self.ui.repeate_times_spin_box.value()
                    d.repeater_info.user_function_str = self.ui.user_function_plain_text_edit.toPlainText()
                    self.datagram_repeater.append_data(index, self.payload_package)
                    self.statusBar().showMessage(sender.text() + ' OK')
                    self.ui.repeater_push_button.setText('Stop')
                    self.ui.publish_push_button.setEnabled(False)
                else:
                    self.statusBar().showMessage(sender.text() + ' Failed')
                pass
            pass
        except Exception as exception:
            print('ERROR:', exception)
            self.statusBar().showMessage(sender.text() + ' Failed')
            return
        pass

    @staticmethod
    def get_package_val_from_text(text=''):
        text = text.split('|')[0].strip(' ').upper()
        if text.startswith('0X'):
            return int(text, base=16)
        return int(text)

    @pyqtSlot()
    def on_publish_push_button_clicked(self):
        try:
            model = self.ui.value_edit_tree_view.model()
            if model is None:
                self.statusBar().showMessage('Invalid Value Type')
                return
            self.payload_package.value = model.get_value()
            from PyQt5.QtCore import Qt
            self.payload_package.payload_type =\
                self.get_package_val_from_text(self.ui.payload_type_combo_box.currentText())
            self.payload_package.payload_version =\
                self.get_package_val_from_text(self.ui.payoad_version_line_edit.text())
            self.payload_package.hash_id = self.get_package_val_from_text(self.ui.hash_id_line_edit.text())
            self.payload_package.producer_mask =\
                self.get_package_val_from_text(self.ui.producer_mask_combo_box.currentText())
            self.payload_package.action = self.get_package_val_from_text(self.ui.action_combo_box.currentText())
            self.payload_package.time_stamp_second =\
                self.get_package_val_from_text(self.ui.time_stamp_s_line_edit.text())
            self.payload_package.time_stamp_ms = self.get_package_val_from_text(self.ui.time_stamp_ms_line_edit.text())
            self.payload_package.device_instance_index =\
                self.get_package_val_from_text(self.ui.device_index_line_edit.text())
            self.payload_package.data_object_reference_type =\
                self.get_package_val_from_text(self.ui.reference_type_line_edit.text())
            self.payload_package.data_object_reference_value =\
                self.get_package_val_from_text(self.ui.reference_value_line_edit.text())

            if self.datagram_server.publish(self.payload_package, self.ui.topic_line_edit.text()):
                dg = self.datagram_manager.datagram_dict[self.payload_package.hash_id]
                if (dg.attribute.type == 'COMMAND') and (self.payload_package.action == 0):
                    value = self.payload_package.value & 0xff0000ff
                    value |= 0x00ffff00 & (self.datagram_manager.seq_num << 8)
                    try:
                        model.value = value
                        model.update()
                    except AttributeError as exception:
                        print('ERROR:', exception)
                        pass
                result = 'Publish OK'
            else:
                result = 'Publish Failed'
            self.statusBar().showMessage(result)

        except Exception as exception:
            print('ERROR:', exception)
            self.statusBar().showMessage('Publish Failed')
            return

    @staticmethod
    def update_datagram_value_display_callback(obj, payload_package):
        obj.update_datagram_value_display_signal.emit(payload_package)
        pass

    @staticmethod
    def record_datagram_server_message_callback(obj, msg_str):
        obj.record_datagram_server_message_signal.emit(msg_str)
        pass

    pass

########################################################################################################################
except_hook = sys.excepthook


def exception_hook(exc_type, value, traceback):
    except_hook(exc_type, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook
########################################################################################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWin()
    window.show()
    ret = app.exec_()
    window.quit()
    sys.exit(ret)
    pass
