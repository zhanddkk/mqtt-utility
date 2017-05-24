from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from UiMessageBrowserWindow import Ui_MessageBrowserWindow
import os as _os


class MessageBrowserWindow(QMainWindow):
    def __init__(self, parent=None, flags=Qt.Widget):
        super(MessageBrowserWindow, self).__init__(parent, flags)
        self.ui = Ui_MessageBrowserWindow()
        self.ui.setupUi(self)
        self.__filter_data = {}
        self.__is_start_to_watch = False
        self.ui.actionStopToWatch.setEnabled(False)
        self.ui.actionStopToWatch.triggered.connect(self.__action_stop)
        self.ui.actionStartToWatch.triggered.connect(self.__action_start)
        self.ui.actionClearAllMessages.triggered.connect(self.__action_clear)
        self.ui.actionOpenFilterConfigFile.triggered.connect(self.__action_open_filter_config_file)
        self.ui.actionSaveFilterConfigFile.triggered.connect(self.__action_save_filter_config_file)
        self.ui.actionSaveAsFilterConfigFile.triggered.connect(self.__action_save_as_filter_config_file)
        self.__filter_config_file = 'default_config.xml'
        self.ui.filter_config_file_line_edit.setText(self.__filter_config_file)
        pass

    def add_item(self, hash_id, device_index):
        if hash_id in self.__filter_data:
            _device_indexes = self.__filter_data[hash_id]
            if device_index in _device_indexes:
                pass
            else:
                _device_indexes.append(device_index)
                pass
        else:
            self.__filter_data[hash_id] = [device_index]
            pass
        pass

    def remove_item(self, hash_id, device_index):
        if hash_id in self.__filter_data:
            _device_indexes = self.__filter_data[hash_id]
            try:
                _device_indexes.remove(device_index)
                if not _device_indexes:
                    self.__filter_data.pop(hash_id)
                    pass
            except ValueError:
                pass
        pass

    def print_message(self, message):
        if self.__is_start_to_watch:
            _payload = message.payload
            _hash_id = _payload.hash_id
            _device_index = _payload.device_instance_index - 1
            if self.__is_need_print(_hash_id, _device_index):
                self.ui.message_browser_plain_text_edit.appendPlainText('{}'.format(_payload))
                pass
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
            print('Open:', _file)
        pass

    def __action_save_filter_config_file(self):
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
            print('Save As:', _file)
        pass

    def __is_need_print(self, hash_id, device_index):
        _ret = False
        try:
            _ret = device_index in self.__filter_data[hash_id]
        except IndexError:
            pass
        except KeyError:
            pass
        return _ret
        pass

    def __open_config(self, file_name):
        pass

    def __save_config(self, file_name):
        
        pass

    pass
