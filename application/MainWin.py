import datetime
from collections import OrderedDict
from PyQt5.Qt import Qt, QDir, QFileInfo, QFontMetrics, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QHeaderView, QTreeWidgetItem, QMenu
from PyQt5.QtWidgets import QAction
from UiMainWin import Ui_MainWindow
from AppVersion import __doc__ as __app_version__
from DataDictionaryTreeViewModel import DataDictionaryTreeViewModel
from DataMonitorTableViewModel import DataMonitorTableViewModel
from Configuration import Configuration
from QSimpleThread import QSimpleThread
from SettingDlg import SettingDlg
from WaitingDlg import WaitingDlg
from LogWin import LogWin
from SafeConnector import SafeConnector
from ValueEditorTreeViewModel import ValueEditorTreeViewModel
from ValueEditorTreeViewDelegate import ValueEditorTreeViewDelegate
from HistoryDataDisplayTreeViewModel import HistoryDataDisplayTreeViewModel
from SettingDatagramValues import SettingDatagramValues
from MessageBrowserWindow import MessageBrowserWindow
from ddclient import __version__ as __dd_client_pkg_version__
from ddclient.dgmanager import DatagramManager, message_format_class
from ddclient.dgpayload import (E_DATAGRAM_ACTION_PUBLISH, E_DATAGRAM_ACTION_RESPONSE, E_DATAGRAM_ACTION_REQUEST,
                                E_DATAGRAM_ACTION_ALLOW)
from ddclient.dgpayload import E_PAYLOAD_TYPE, E_PRODUCER_MASK, E_ACTION, payload_package_info, DatagramPayload
from ddclient.repeater import (Repeater,
                               user_function_header_str,
                               default_user_input_str,
                               user_function_end_str,
                               get_user_function_source_code)
from ddclient.bitmapparser import command_bit_map, BitMapParser
from ddclient.valuetype import ValueType
from ddclient.ddinterface import enum_item_attribute_type
_about_application_message_format = """\
<p>----------Application Info----------</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;-qt-block-indent:0; text-indent:0px;">
    This <span style=" font-weight:600;">Application</span> is a simulator which depends on the
    <span style=" font-weight:600;">ddclient</span>({dd_client_pkg_version}).
</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
    <span style=" font-weight:600;">Version</span> : {app_version}
</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
    <span style=" font-weight:600;">Copyright</span> :
    <span style=" font-style:italic; text-decoration: underline; color:#3bb300;"> Schneider Electric (China) Co., Ltd.
    </span>
</p>
<p>----------Data Dictionary Info----------</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
<span style=font-weight:600;>{template_doc}</span> : {template}</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
<span style=font-weight:600;>{content_doc}</span> : {content}</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
<span style=font-weight:600;>Product Name</span> : {pro_name}</p>
"""


class MainWin(QMainWindow):
    update_datagram_info_display_signal = pyqtSignal(tuple, name='UpdateDatagramInfoDisplaySignal')
    update_datagram_value_display_signal = pyqtSignal(tuple, name='UpdateDatagramValueDisplaySignal')
    update_history_data_display_signal = pyqtSignal(tuple, name='UpdateHistoryDataDisplaySignal')
    record_message_signal = pyqtSignal(message_format_class, name='RecordMessageSignal')

    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent, flags=Qt.Window)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__application_version = __app_version__
        self.__dd_client_pkg_version = __dd_client_pkg_version__
        self.__qt_signal_safe_convert = SafeConnector()
        self.__qt_signal_safe_convert.connect(self.record_message_signal, self.do_record_message)
        self.__qt_signal_safe_convert.connect(self.update_datagram_value_display_signal,
                                              self.update_datagram_value_display)

        self.__command_bit_map_parser = BitMapParser(command_bit_map)

        self.__current_datagram_topic_index = None
        self.__payload = DatagramPayload()

        self.__configuration = Configuration()
        self.__configuration.read_config()

        self.__log_win = LogWin(self.__configuration, self)
        self.ui.log_dock_widget.setWidget(self.__log_win)

        self.__datagram_manager = DatagramManager(self)
        self.__datagram_manager.init_datagram_access_client('UI',
                                                            self.__configuration.connect_broker_ip,
                                                            self.__configuration.connect_broker_ip_port)
        self.__datagram_topic_index = []

        self.__repeater = Repeater(self.__datagram_manager)

        self.__message_browser_win = MessageBrowserWindow(self.__datagram_manager, self)
        self.ui.mesg_browser_dock_widget.setWidget(self.__message_browser_win)

        # Define model
        self.__data_dictionary_tree_view_module =\
            DataDictionaryTreeViewModel(self.__datagram_manager,
                                        self.__datagram_topic_index,
                                        self.__message_browser_win.message_filter_config)
        self.__data_monitor_table_view_model = DataMonitorTableViewModel(self.__datagram_manager)
        self.__value_editor_tree_view_model = ValueEditorTreeViewModel()
        self.__history_data_display_tree_view_model = HistoryDataDisplayTreeViewModel()

        # Set model
        self.ui.data_dictionary_tree_view.setModel(self.__data_dictionary_tree_view_module)
        self.ui.data_monitor_table_view.setModel(self.__data_monitor_table_view_model)
        self.ui.value_editor_tree_view.setModel(self.__value_editor_tree_view_model)
        self.ui.history_data_display_tree_view.setModel(self.__history_data_display_tree_view_model)

        # Set delegate
        self.ui.value_editor_tree_view.setItemDelegate(ValueEditorTreeViewDelegate())

        # Set data monitor table view all cells' height
        font = self.ui.data_monitor_table_view.font()
        font_metrics = QFontMetrics(font)
        font_height = font_metrics.height() + 4
        vertical_header = self.ui.data_monitor_table_view.verticalHeader()
        vertical_header.setDefaultSectionSize(font_height)

        # Menu action
        self.ui.actionExit.triggered.connect(getattr(QApplication, 'instance')().quit)
        self.ui.actionImport.triggered.connect(self.import_data_dictionary)
        self.ui.actionConnect_Broker.triggered.connect(self.connect_to_broker)
        self.ui.actionSettings.triggered.connect(self.setting)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionDump_Setting_Data.triggered.connect(self.dump_setting_data)
        self.ui.actionRestore_Setting_Data.triggered.connect(self.restore_setting_data)

        # Set dock widget
        self.tabifyDockWidget(self.ui.payload_dock_widget, self.ui.repeater_dock_widget)
        self.tabifyDockWidget(self.ui.repeater_dock_widget, self.ui.mesg_browser_dock_widget)
        self.ui.payload_dock_widget.raise_()

        # Set data monitor table view attribute
        self.ui.data_monitor_table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Init event callback function
        self.ui.data_dictionary_tree_view.selectionModel().selectionChanged.connect(
            self.data_dictionary_tree_view_item_selected)
        self.ui.data_monitor_table_view.selectionModel().selectionChanged.connect(
            self.data_monitor_table_view_item_selected)
        self.update_datagram_info_display_signal.connect(self.update_datagram_info_display)
        self.ui.enable_data_object_check_box.clicked.connect(self.enable_data_object_check_box_clicked)
        self.ui.force_edit_package_check_box.clicked.connect(self.force_edit_package_check_box_clicked)
        self.update_history_data_display_signal.connect(self.update_history_data_display)

        # Data dictionary tree view context menu
        self.__data_dictionary_tree_view_context_menu = QMenu(self)
        self.__add_datagram_to_watch_action = QAction('Add to watch',
                                                      self.__data_dictionary_tree_view_context_menu)
        getattr(self.__add_datagram_to_watch_action.triggered, 'connect')(
            self.__add_datagram_to_watch_action_triggered)
        self.__remove_datagram_from_watch_browser = QAction('Remove from watch browser',
                                                            self.__data_dictionary_tree_view_context_menu)
        getattr(self.__remove_datagram_from_watch_browser.triggered, 'connect')(
            self.__remove_datagram_from_watch_browser_triggered)
        self.__data_dictionary_tree_view_context_menu.addAction(self.__add_datagram_to_watch_action)
        self.__data_dictionary_tree_view_context_menu.addAction(self.__remove_datagram_from_watch_browser)
        self.ui.data_dictionary_tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.data_dictionary_tree_view.customContextMenuRequested.connect(
            self.__data_dictionary_tree_view_context_menu_req)

        # Do init
        self.__init_payload_dock_widget()
        self.__init_view_menu_items()
        self.__init_data_attribute_tree_widget()

        self.__set_dlg = None

        # For test

    def __init_payload_dock_widget(self):
        str_list = []
        for item in sorted(payload_package_info[E_PAYLOAD_TYPE].choice_list.items(), key=lambda d: d[0]):
            str_list.append('{key} | {data}'.format(key=item[0], data=item[1]))
        self.ui.payload_type_combo_box.addItems(str_list)
        str_list.clear()
        for item in sorted(payload_package_info[E_PRODUCER_MASK].choice_list.items(), key=lambda d: d[0]):
            str_list.append('0x{key:>02X} | {data}'.format(key=item[0], data=item[1]))
        self.ui.producer_mask_combo_box.addItems(str_list)
        str_list.clear()
        for item in sorted(payload_package_info[E_ACTION].choice_list.items(), key=lambda d: d[0]):
            str_list.append('{key} | {data}'.format(key=item[0], data=item[1]))
        self.ui.action_combo_box.addItems(str_list)
        self.__set_reference_data_hidden_in_payload(True)
        pass

    def __init_view_menu_items(self):
        self.ui.menuView.addAction(self.ui.data_dictionary_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.menuView.addAction(self.ui.data_attribute_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.menuView.addAction(self.ui.payload_dock_widget.toggleViewAction())
        self.ui.menuView.addAction(self.ui.repeater_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.menuView.addAction(self.ui.data_history_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.log_dock_widget.setVisible(False)
        self.ui.menuView.addAction(self.ui.log_dock_widget.toggleViewAction())
        self.ui.menuView.addSeparator()
        self.ui.menuView.addAction(self.ui.mesg_browser_dock_widget.toggleViewAction())

    def __init_data_attribute_tree_widget(self):
        from ddclient.dditem import data_dictionary_item_type
        from DataAttributeTreeWidgetDelegate import DataAttributeTreeWidgetDelegate
        import string
        self.ui.data_attribute_tree_widget.setItemDelegate(DataAttributeTreeWidgetDelegate())
        widget = self.ui.data_attribute_tree_widget
        for field_name in getattr(data_dictionary_item_type, '_fields'):
            name = field_name.replace('_', ' ')
            top_item = QTreeWidgetItem((string.capwords(name), ))
            widget.addTopLevelItem(top_item)
        pass

    def __set_reference_data_hidden_in_payload(self, state):
        self.ui.data_object_id_label.setHidden(state)
        self.ui.data_object_id_line_edit.setHidden(state)
        pass

    def __expand_datagram_index_to_topic_index(self):
        self.__datagram_topic_index.clear()
        for index in self.__datagram_manager.datagram_indexes:
            hash_id = index[0]
            instance = index[1]
            dg = self.__datagram_manager.get_datagram(hash_id)
            if dg is None:
                continue
            self.__datagram_topic_index.append((hash_id, instance, E_DATAGRAM_ACTION_PUBLISH))
            if dg.attribute.type == 'Command':
                self.__datagram_topic_index.append((hash_id, instance, E_DATAGRAM_ACTION_RESPONSE))
                self.__datagram_topic_index.append((hash_id, instance, E_DATAGRAM_ACTION_ALLOW))
            elif dg.attribute.type == 'Setting':
                self.__datagram_topic_index.append((hash_id, instance, E_DATAGRAM_ACTION_RESPONSE))
                self.__datagram_topic_index.append((hash_id, instance, E_DATAGRAM_ACTION_REQUEST))
                self.__datagram_topic_index.append((hash_id, instance, E_DATAGRAM_ACTION_ALLOW))
                pass
            pass
        pass

    def __build_value_type_attribute_tree_widget_sub_item(self, parent_item, _type):
        if isinstance(_type, ValueType):
            for filed_name in _type.fields:
                if filed_name == 'special_data':
                    _special_data = getattr(_type, filed_name)
                    item_value_str = '' if _special_data is None else _special_data.__class__.__name__
                    sub_item = QTreeWidgetItem([filed_name, item_value_str])
                    self.__build_value_type_attribute_tree_widget_sub_item(sub_item, _special_data)
                    pass
                else:
                    sub_item = QTreeWidgetItem([filed_name, str(getattr(_type, filed_name))])
                parent_item.addChild(sub_item)
            pass
        elif isinstance(_type, OrderedDict):
            for _key, _data in getattr(_type, 'items')():
                if isinstance(_data, enum_item_attribute_type):
                    sub_item = QTreeWidgetItem([_key, str(_data.value)])
                elif isinstance(_data, ValueType):
                    sub_item = QTreeWidgetItem([_key, str(_data.type_name)])
                    self.__build_value_type_attribute_tree_widget_sub_item(sub_item, _data)
                else:
                    sub_item = QTreeWidgetItem([_key, 'Undefined'])
                parent_item.addChild(sub_item)
                pass
            pass
        else:
            pass
        pass

    def __update_data_attribute_tree_widget(self, datagram_attribute):
        widget = self.ui.data_attribute_tree_widget
        for (index, field_name) in enumerate(getattr(getattr(datagram_attribute, '_source'), '_fields')):
            top_item = self.ui.data_attribute_tree_widget.topLevelItem(index)
            value = getattr(datagram_attribute, field_name)
            if field_name == 'value_type':
                top_item.takeChildren()
                item_value_str = value.type_name
                self.__build_value_type_attribute_tree_widget_sub_item(top_item, value)
                self.ui.data_attribute_tree_widget.expandItem(top_item)
                pass
            elif field_name == 'hash_id':
                if value is None:
                    item_value_str = ''
                    pass
                else:
                    item_value_str = '0x{:08X}'.format(value)
                pass
            else:
                if value is None:
                    item_value_str = ''
                elif type(value) is not str:
                    item_value_str = str(value)
                else:
                    item_value_str = value
            top_item.setText(1, item_value_str)
        widget.resizeColumnToContents(0)
        pass

    def __update_payload_display(self, topic, payload):
        self.ui.topic_line_edit.setText(topic)

        select_list = payload_package_info[E_PAYLOAD_TYPE].choice_list
        payload_type = getattr(payload, 'payload_type')
        if payload_type in select_list:
            select_index = self.ui.payload_type_combo_box.findText(
                '{value} | {type}'.format(value=payload_type, type=select_list[payload_type]))
            if select_index != -1:
                self.ui.payload_type_combo_box.setCurrentIndex(select_index)
            else:
                self.ui.payload_type_combo_box.setCurrentText(str(payload_type))
        else:
            self.ui.payload_type_combo_box.setCurrentText(str(payload_type))

        self.ui.payoad_version_line_edit.setText(str(getattr(payload, 'payload_version')))
        self.ui.hash_id_line_edit.setText('0x{hash_id:>08X}'.format(hash_id=getattr(payload, 'hash_id')))

        select_list = payload_package_info[E_PRODUCER_MASK].choice_list
        producer_mask = getattr(payload, 'producer_mask')
        if producer_mask in select_list:
            select_index = self.ui.producer_mask_combo_box.findText(
                '0x{value:02X} | {type}'.format(value=producer_mask, type=select_list[producer_mask]))
            if select_index != -1:
                self.ui.producer_mask_combo_box.setCurrentIndex(select_index)
            else:
                self.ui.producer_mask_combo_box.setCurrentText(str(producer_mask))
        else:
            self.ui.producer_mask_combo_box.setCurrentText(str(producer_mask))

        select_list = payload_package_info[E_ACTION].choice_list
        action = getattr(payload, 'action')
        if action in select_list:
            select_index = self.ui.action_combo_box.findText(
                '{value} | {type}'.format(value=action, type=select_list[action]))
            if select_index != -1:
                self.ui.action_combo_box.setCurrentIndex(select_index)
            else:
                self.ui.action_combo_box.setCurrentText(str(action))
        else:
            self.ui.action_combo_box.setCurrentText(str(action))

        self.ui.time_stamp_s_line_edit.setText(str(getattr(payload, 'time_stamp_second')))
        self.ui.time_stamp_ms_line_edit.setText(str(getattr(payload, 'time_stamp_ms')))
        self.ui.device_index_line_edit.setText(str(getattr(payload, 'device_instance_index')))
        # self.ui.reference_id_line_edit.setText(str(getattr(payload, 'data_object_reference_type')))
        self.ui.data_object_id_line_edit.setText('0x{:0>16X}'.format(getattr(payload, 'data_object_id')))
        pass

    def __update_repeater_info_display(self, repeater_resource):
        if repeater_resource is None:
            self.ui.interval_spin_box.setValue(1)
            self.ui.repeate_times_spin_box.setValue(0)
            user_input_str = default_user_input_str
            pass
        else:
            self.ui.interval_spin_box.setValue(repeater_resource.tagger_count)
            self.ui.repeate_times_spin_box.setValue(repeater_resource.repeat_times_count)
            user_input_str = repeater_resource.user_input_str
            pass
        self.ui.user_function_plain_text_edit.setPlainText(
            get_user_function_source_code(user_input_str)
        )
        pass

    def __update_value_editor_tree_view_display(self, datagram, instance, action):
        _value = datagram.get_device_data_value(instance, action)
        if datagram.attribute.type == 'Command':
            if action == E_DATAGRAM_ACTION_PUBLISH:
                _sequence_num = self.__datagram_manager.sequence_number
                # No general
                if _value is None:
                    _value = 0
                self.__command_bit_map_parser.decode(_value)
                _value = self.__command_bit_map_parser.encode(sequence=_sequence_num)
                # _value &= 0xff0000ff
                # _value |= 0x00ffff00 & (_sequence_num << 8)
                pass
            pass
        _value_attribute = datagram.get_value_type(action)
        self.__value_editor_tree_view_model.set_value(_value, _value_attribute)
        self.ui.value_editor_tree_view.expandAll()
        self.ui.value_editor_tree_view.resizeColumnToContents(0)
        self.ui.value_editor_tree_view.resizeColumnToContents(1)
        pass

    def __update_history_data_tree_view_display(self, datagram, instance, action):
        _history_data = datagram.get_device_data_history(instance, action)
        _additional_data_value_attribute = None
        _value_attribute = datagram.get_value_type(action)
        self.__history_data_display_tree_view_model.set_value(
            history_data=_history_data,
            value_attribute=_value_attribute,
            additional_data_value_attribute=_additional_data_value_attribute)
        self.ui.history_data_display_tree_view.resizeColumnToContents(0)
        self.ui.history_data_display_tree_view.resizeColumnToContents(1)
        pass

    def __data_dictionary_tree_view_context_menu_req(self, q_point):
        _item_index = self.ui.data_dictionary_tree_view.selectionModel().currentIndex()
        if _item_index:
            _model = self.ui.data_dictionary_tree_view.model()
            _item = _model.get_item(_item_index)
            try:
                self.__add_datagram_to_watch_action.setEnabled(not _item.is_selected_to_watch)
                self.__remove_datagram_from_watch_browser.setEnabled(_item.is_selected_to_watch)
                _pos = self.ui.data_dictionary_tree_view.mapToGlobal(q_point)
                self.__data_dictionary_tree_view_context_menu.exec(_pos)
                pass
            except AttributeError:
                pass
        else:
            pass
        pass

    def __add_datagram_to_watch_action_triggered(self):
        _item_index = self.ui.data_dictionary_tree_view.selectionModel().currentIndex()
        if _item_index:
            _model = self.ui.data_dictionary_tree_view.model()
            _model.select_to_watch(_item_index, True)
        pass

    def __remove_datagram_from_watch_browser_triggered(self):
        _item_index = self.ui.data_dictionary_tree_view.selectionModel().currentIndex()
        if _item_index:
            _model = self.ui.data_dictionary_tree_view.model()
            _model.select_to_watch(_item_index, False)
        pass

    @staticmethod
    def __waiting_thread_task(do_task, waiting_dlg):
        waiting_dlg.time_out_signal.emit(do_task())
        pass

    @staticmethod
    def __get_package_value_from_text(text=''):
        text = text.split('|')[0].strip(' ').upper()
        if text.startswith('0X'):
            return int(text, base=16)
        return int(text)

    def import_data_dictionary(self):
        _client = self.__datagram_manager.datagram_access_client
        if _client is not None:
            if _client.is_running:
                msg_dlg = QMessageBox()
                msg_dlg.critical(self, 'Import Error',
                                 'Please disconnect the client to the broker first!', QMessageBox.Ok)
                self.statusBar().showMessage('Import failed')
                return
        fdg = QFileDialog()
        q_dir = QDir(self.__configuration.data_dictionary_path)
        csv_path = q_dir.absolutePath()
        fdg.setDirectory(csv_path)
        fdg.setNameFilter("CSV Files (*.csv);;Text Files (*.txt);;All Files (*)")
        if fdg.exec():
            file_name = fdg.selectedFiles()[0]
            file_info = QFileInfo(file_name)
            self.__configuration.data_dictionary_path = file_info.absolutePath()
            self.__configuration.data_dictionary_file_name = file_info.fileName()
            self.__configuration.save_config()
            if self.__datagram_manager.import_data_dictionary(file_name):
                self.__expand_datagram_index_to_topic_index()
                self.__data_dictionary_tree_view_module.update()
                self.__data_monitor_table_view_model.update(self.__datagram_topic_index)
                self.ui.data_monitor_table_view.resizeColumnToContents(0)
                self.ui.data_monitor_table_view.resizeColumnToContents(1)

                self.statusBar().showMessage(file_name)
            else:
                self.statusBar().showMessage('Import failed')
            pass
        pass

    def data_dictionary_tree_view_item_selected(self):
        item_index = self.ui.data_dictionary_tree_view.selectionModel().currentIndex()
        model = self.ui.data_dictionary_tree_view.model()
        item = model.get_item(item_index)
        if item.hide_data is None:
            return
        model = self.ui.data_monitor_table_view.model()
        row = model.get_row(hash_id=item.hide_data[0], instance=item.hide_data[1], action=item.hide_data[2])
        if row is None:
            return
        row_index = model.index(row, 0)
        self.ui.data_monitor_table_view.setCurrentIndex(row_index)
        self.ui.data_monitor_table_view.scrollTo(row_index)
        pass

    def data_monitor_table_view_item_selected(self):
        model = self.ui.data_monitor_table_view.model()
        item_index = self.ui.data_monitor_table_view.selectionModel().currentIndex()
        row = item_index.row()
        self.update_datagram_info_display_signal.emit(model.topic_indexes[row])
        pass

    def update_datagram_info_display(self, topic_index):
        self.__current_datagram_topic_index = topic_index
        hash_id = topic_index[0]
        instance = topic_index[1]
        action = topic_index[2]
        dg = self.__datagram_manager.get_datagram(hash_id)
        if dg is None:
            return
        self.__update_data_attribute_tree_widget(dg.attribute)
        self.__payload.hash_id = hash_id
        self.__payload.device_instance_index = instance + 1
        dev_data = dg.get_device_data(instance)
        if dev_data is None:
            return
        topic = dev_data.get_topic(action)
        if topic is None:
            return
        self.__payload.action = action
        _producer_mask_names = dg.attribute.producer
        if _producer_mask_names and isinstance(_producer_mask_names[0], str):
            _producer_mask_name = _producer_mask_names[0]
            for _key, _data in payload_package_info[E_PRODUCER_MASK].choice_list.items():
                if _producer_mask_name.upper() == _data.upper():
                    self.__payload.producer_mask = _key
                    break
        self.__update_payload_display(topic, self.__payload)
        repeater_resource = self.__repeater.get_repeater_item_resource(hash_id, instance, action)
        self.__update_repeater_info_display(repeater_resource)
        if self.__repeater.is_running and (repeater_resource is not None):
            self.ui.repeater_push_button.setText('Stop')
            self.ui.publish_push_button.setEnabled(False)
            pass
        else:
            self.ui.repeater_push_button.setText('Start')
            self.ui.publish_push_button.setEnabled(True)
            pass
        self.__update_value_editor_tree_view_display(dg, instance, action)
        self.__update_history_data_tree_view_display(dg, instance, action)
        self.statusBar().showMessage('Hash ID: 0x{hash_id:>08X}, Device Index: {instance}, Action: {action}'.format(
            hash_id=hash_id, instance=instance + 1,
            action='{value} | {action}'.format(value=action,
                                               action=payload_package_info[E_ACTION].choice_list[action])
            if action in payload_package_info[E_ACTION].choice_list else action))
        pass

    def update_datagram_value_display(self, topic_index):
        hash_id = topic_index[0]
        instance = topic_index[1]
        action = topic_index[2]
        model = self.ui.data_monitor_table_view.model()
        if model is None:
            return
        row = model.get_row(hash_id, instance, action)
        if row is None:
            return
        model_index = model.index(row, 2)
        model.dataChanged.emit(model_index, model_index)
        if topic_index == self.__current_datagram_topic_index:
            self.update_history_data_display_signal.emit(topic_index)
        pass

    def update_history_data_display(self, topic_index):
        model = self.ui.data_monitor_table_view.model()
        item_index = self.ui.data_monitor_table_view.selectionModel().currentIndex()
        row = item_index.row()
        if topic_index == model.topic_indexes[row]:
            _dg = self.__datagram_manager.get_datagram(topic_index[0])
            if _dg:
                self.__update_history_data_tree_view_display(_dg, topic_index[1], topic_index[2])
        pass

    def do_record_message(self, message):
        _date_time = datetime.datetime.now()
        self.__log_win.update_log_display(message, _date_time)
        self.__message_browser_win.print_message(message, _date_time)
        pass

    def setting(self):
        if self.__set_dlg is None:
            self.__set_dlg = SettingDlg(self.__configuration)
        self.__set_dlg.exec()

    def dump_setting_data(self):
        fdg = QFileDialog()
        fdg.setAcceptMode(QFileDialog.AcceptSave)
        q_dir = QDir(self.__configuration.setting_data_file_path)
        csv_path = q_dir.absolutePath()
        fdg.setDirectory(csv_path)
        fdg.setNameFilter("Json Files (*.json);;Text Files (*.txt);;All Files (*)")
        if fdg.exec():
            file_name = fdg.selectedFiles()[0]
            file_info = QFileInfo(file_name)
            self.__configuration.setting_data_file_path = file_info.absolutePath()
            self.__configuration.save_config()
            _values = SettingDatagramValues(self.__datagram_manager, self.__configuration, self)
            if _values.dump(file_name):
                self.statusBar().showMessage('Dumped to [{}]'.format(file_name))
            else:
                self.statusBar().showMessage('Dump failed')
        pass

    def restore_setting_data(self):
        fdg = QFileDialog()
        q_dir = QDir(self.__configuration.setting_data_file_path)
        csv_path = q_dir.absolutePath()
        fdg.setDirectory(csv_path)
        fdg.setNameFilter("Json Files (*.json);;Text Files (*.txt);;All Files (*)")
        if fdg.exec():
            file_name = fdg.selectedFiles()[0]
            file_info = QFileInfo(file_name)
            self.__configuration.setting_data_file_path = file_info.absolutePath()
            self.__configuration.save_config()
            _values = SettingDatagramValues(self.__datagram_manager, self.__configuration, self)
            if _values.load(file_name):
                self.statusBar().showMessage('Restored from [{}]'.format(file_name))
            else:
                self.statusBar().showMessage('Restored failed')
        pass

    def about(self):
        about_dlg = QMessageBox()
        about_dlg.about(self, 'About Application', _about_application_message_format.format(
            app_version=self.__application_version,
            dd_client_pkg_version=self.__dd_client_pkg_version,
            template_doc=self.__datagram_manager.data_dictionary_version.template.doc,
            template='{}.{}'.format(self.__datagram_manager.data_dictionary_version.template.major,
                                    self.__datagram_manager.data_dictionary_version.template.minor),
            content_doc=self.__datagram_manager.data_dictionary_version.content.doc,
            content='{}.{}'.format(self.__datagram_manager.data_dictionary_version.content.major,
                                   self.__datagram_manager.data_dictionary_version.content.minor),
            pro_name=self.__datagram_manager.product_information.name
        ))
        pass

    def connect_to_broker(self):
        client = self.__datagram_manager.datagram_access_client
        if self.ui.actionConnect_Broker.isChecked():
            if client.is_running:
                self.statusBar().showMessage('Is Connected')
                pass
            else:
                self.statusBar().showMessage('Connecting...')
                client.config(self.__configuration.connect_broker_ip, self.__configuration.connect_broker_ip_port)
                waiting_dlg = WaitingDlg(self)
                waiting_thread = QSimpleThread(target=self.__waiting_thread_task, args=(client.start, waiting_dlg))
                waiting_thread.start()
                waiting_dlg.exec()
                ret_val = waiting_dlg.result
                self.ui.actionConnect_Broker.setChecked(ret_val)
                if ret_val is False:
                    msg_dlg = QMessageBox()
                    msg_dlg.critical(self, 'Connect Error',
                                     'Can\'t connect to the broker'
                                     '<p><b>Address :</b> {ip}</p>'
                                     '<p><b>Port :</b> {port}</p>'.format(ip=client.ip, port=client.port),
                                     QMessageBox.Ok)
                    self.statusBar().showMessage('Connect Failed')
                else:
                    self.statusBar().showMessage('Connected@{ip}:{port}'.format(ip=client.ip, port=client.port))
                    pass
        else:
            if client.is_running:
                client.stop()
                self.statusBar().showMessage('Disconnected')
        pass

    def enable_data_object_check_box_clicked(self, state):
        self.__payload.is_object_reference_package = state
        self.__set_reference_data_hidden_in_payload(not state)
        pass

    def force_edit_package_check_box_clicked(self, state):
        self.ui.topic_line_edit.setReadOnly(not state)
        self.ui.hash_id_line_edit.setEnabled(state)
        self.ui.action_combo_box.setEnabled(state)
        self.ui.device_index_line_edit.setEnabled(state)
        pass

    def closeEvent(self, event):
        msg_dlg = QMessageBox()
        reply = msg_dlg.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot(name='')
    def on_publish_push_button_clicked(self):
        try:
            model = self.ui.value_editor_tree_view.model()
            if model is None:
                self.statusBar().showMessage('Invalid Value Type')
                return
            self.__payload.value = model.value
            self.__payload.payload_type = \
                self.__get_package_value_from_text(self.ui.payload_type_combo_box.currentText())
            self.__payload.payload_version = \
                self.__get_package_value_from_text(self.ui.payoad_version_line_edit.text())
            self.__payload.hash_id = self.__get_package_value_from_text(self.ui.hash_id_line_edit.text())
            self.__payload.producer_mask = \
                self.__get_package_value_from_text(self.ui.producer_mask_combo_box.currentText())
            self.__payload.action = self.__get_package_value_from_text(self.ui.action_combo_box.currentText())
            self.__payload.time_stamp_second = \
                self.__get_package_value_from_text(self.ui.time_stamp_s_line_edit.text())
            self.__payload.time_stamp_ms = self.__get_package_value_from_text(self.ui.time_stamp_ms_line_edit.text())
            self.__payload.device_instance_index = \
                self.__get_package_value_from_text(self.ui.device_index_line_edit.text())
            self.__payload.data_object_id = \
                self.__get_package_value_from_text(self.ui.data_object_id_line_edit.text())
            if self.__datagram_manager.send_package_by_payload(payload=self.__payload,
                                                               topic=self.ui.topic_line_edit.text()):
                _dg = self.__datagram_manager.get_datagram(self.__payload.hash_id)
                if _dg is not None:
                    if (_dg.attribute.type == 'Command') and (self.__payload.action == E_DATAGRAM_ACTION_PUBLISH):
                        # No general
                        # _value = self.__payload.value & 0xff0000ff
                        # _value |= 0x00ffff00 & (self.__datagram_manager.sequence_number << 8)
                        self.__command_bit_map_parser.decode(self.__payload.value)
                        _value = self.__command_bit_map_parser.encode(sequence=self.__datagram_manager.sequence_number)
                        model.set_value(_value, _dg.get_value_type(self.__payload.action))
                        self.ui.value_editor_tree_view.expandAll()
                        pass
                topic_index = (self.__payload.hash_id,
                               self.__payload.device_instance_index - 1,
                               self.__payload.action)
                if topic_index == self.__current_datagram_topic_index:
                    self.update_history_data_display_signal.emit(topic_index)
                result = 'Publish OK'
            else:
                result = 'Publish Failed'
            self.statusBar().showMessage(result)
        except Exception as exception:
            # import traceback
            # traceback.print_exc()
            print('ERROR:', type(exception).__name__, exception)
            self.statusBar().showMessage('Publish Failed')
        pass

    @pyqtSlot(name='')
    def on_repeater_push_button_clicked(self):
        sender = self.sender()
        try:
            hash_id = self.__current_datagram_topic_index[0]
            instance = self.__current_datagram_topic_index[1]
            action = self.__current_datagram_topic_index[2]

            repeater_resource = self.__repeater.get_repeater_item_resource(hash_id, instance, action)
            if self.__repeater.is_running and (repeater_resource is not None):
                if self.__repeater.delete_repeater_item(hash_id, instance, action):
                    self.ui.repeater_push_button.setText('Start')
                    self.ui.publish_push_button.setEnabled(True)
                pass
            else:
                from ddclient.repeater import repeater_parameter
                _input_text = str(self.ui.user_function_plain_text_edit.toPlainText())
                _input_text = _input_text.lstrip(user_function_header_str.rstrip('\n'))
                _input_text = _input_text.rstrip(user_function_end_str).strip('\n')
                repeater_resource = repeater_parameter(
                    tagger_count=self.ui.interval_spin_box.value(),
                    repeat_times_count=self.ui.repeate_times_spin_box.value(),
                    user_input_str=_input_text)
                if self.__repeater.append_repeater_item(hash_id, instance, action, repeater_resource):
                    self.ui.repeater_push_button.setText('Stop')
                    self.ui.publish_push_button.setEnabled(False)
                pass
            pass
        except Exception as exception:
            print('ERROR:', type(exception).__name__, exception)
            self.statusBar().showMessage('{} Failed'.format(sender.text()))

    def release_resource(self):
        self.__datagram_manager.delete_datagram_access_client()
        self.__repeater.stop_server()
        pass

    # Exec in python standard thread callback function
    # DatagramManager Callback
    def record_message(self, message):
        self.__qt_signal_safe_convert.emit(self.record_message_signal, message)
        pass

    def received_payload(self, *args):
        payload = args[1]
        self.__qt_signal_safe_convert.emit(self.update_datagram_value_display_signal,
                                           (payload.hash_id,
                                            payload.device_instance_index - 1,
                                            payload.action))
        pass

    pass


if __name__ == '__main__':
    pass
