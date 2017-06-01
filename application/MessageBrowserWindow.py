import os as _os

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from MessageFilterConfig import MessageFilterConfig
from UiMessageBrowserWindow import Ui_MessageBrowserWindow
from ddclient.valueprinter import ValuePrinter


class MessageBrowserWindow(QMainWindow):

    __print_msg_header_format = '''\
----------{time}----------
 qos    : {qos}
 retain : {retain}
 topic  : {topic}
 payload:'''

    def __init__(self, datagram_manager, parent=None, flags=Qt.Widget):
        super(MessageBrowserWindow, self).__init__(parent, flags)
        self.ui = Ui_MessageBrowserWindow()
        self.ui.setupUi(self)
        self.__dgm = datagram_manager
        self.__value_printer = ValuePrinter()
        self.__value_printer.print = self.__print
        self.__message_filter_config = MessageFilterConfig(datagram_manager, {})
        self.__is_start_to_watch = False

        self.ui.actionStopToWatch.setEnabled(False)

        # Set callback for all action
        self.ui.actionStopToWatch.triggered.connect(self.__action_stop)
        self.ui.actionStartToWatch.triggered.connect(self.__action_start)
        self.ui.actionClearAllMessages.triggered.connect(self.__action_clear)
        self.ui.actionOpenFilterConfigFile.triggered.connect(self.__action_open_filter_config_file)
        self.ui.actionSaveFilterConfigFile.triggered.connect(self.__action_save_filter_config_file)
        self.ui.actionSaveAsFilterConfigFile.triggered.connect(self.__action_save_as_filter_config_file)

        self.__filter_config_file = 'default_config.xml'
        self.ui.filter_config_file_line_edit.setText(self.__filter_config_file)
        self.__data_dictionary_tree_view = parent.ui.data_dictionary_tree_view
        pass

    def print_message(self, message, date_time):
        if self.__is_start_to_watch and message.is_valid:
            _payload = message.payload
            _hash_id = _payload.hash_id
            _device_index = _payload.device_instance_index - 1
            if not self.__message_filter_config.is_item_exist(_hash_id, _device_index):
                return
                pass

            # Print message header
            _msg_header_text = self.__print_msg_header_format.format(time=date_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                                                                     qos=message.qos,
                                                                     retain=message.retain,
                                                                     topic=message.topic)
            self.ui.message_browser_plain_text_edit.appendPlainText(_msg_header_text)

            # Print payload
            self.ui.message_browser_plain_text_edit.appendPlainText('  |->' + str(_payload).replace('\n', '\n  |->'))

            # Print Value
            self.ui.message_browser_plain_text_edit.appendPlainText('  =============Value Display===========')
            _dg = self.__dgm.get_datagram(_hash_id)
            if _dg:
                _value_type = _dg.get_value_type(_payload.action)
                self.__value_printer.print_value(name=_dg.attribute.name,
                                                 value=_payload.value,
                                                 value_type=_value_type,
                                                 deep=1)
            self.ui.message_browser_plain_text_edit.appendPlainText('  =================End=================')
            pass
        pass

    def __print(self, text):
        self.ui.message_browser_plain_text_edit.appendPlainText(text)
        pass

    def __action_start(self):
        self.__is_start_to_watch = True
        self.ui.actionStopToWatch.setEnabled(True)
        self.ui.actionStartToWatch.setEnabled(False)
        pass

    def __action_stop(self):
        self.__is_start_to_watch = False
        self.ui.actionStopToWatch.setEnabled(False)
        self.ui.actionStartToWatch.setEnabled(True)
        pass

    def __action_clear(self):
        self.ui.message_browser_plain_text_edit.clear()
        pass

    def __action_open_filter_config_file(self):
        _file_dlg = QFileDialog()
        _file = _file_dlg.getOpenFileName(parent=self,
                                          caption='Open Config',
                                          directory=_os.path.dirname(self.__filter_config_file)
                                          if _os.path.exists(self.__filter_config_file) else '.',
                                          filter="Xml Files (*.xml);;Text Files (*.txt);;All Files (*)",
                                          options=QFileDialog.ShowDirsOnly)
        if _file[0]:
            self.__filter_config_file = _file[0]
            self.ui.filter_config_file_line_edit.setText(self.__filter_config_file)
            self.__message_filter_config.import_file(self.__filter_config_file)
            self.__data_dictionary_tree_view.model().update_selections()
        pass

    def __action_save_filter_config_file(self):
        self.__message_filter_config.export_file(self.__filter_config_file)
        pass

    def __action_save_as_filter_config_file(self):
        _file_dlg = QFileDialog()
        _file = _file_dlg.getSaveFileName(parent=self,
                                          caption='Save Config',
                                          directory=self.__filter_config_file
                                          if _os.path.exists(self.__filter_config_file) else 'default_config.xml',
                                          filter="Xml Files (*.xml);;Text Files (*.txt);;All Files (*)",
                                          options=QFileDialog.ShowDirsOnly)
        if _file[0]:
            self.__filter_config_file = _file[0]
            self.ui.filter_config_file_line_edit.setText(self.__filter_config_file)
            self.__message_filter_config.export_file(self.__filter_config_file)
        pass

    @property
    def message_filter_config(self):
        return self.__message_filter_config
    pass
