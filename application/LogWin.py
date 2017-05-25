from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow
from UiLogWin import Ui_LogWindow
_log_text_format = '''\
----------{time}----------
 qos: {qos}
 retain: {retain}
 topic: {topic}
 payload: {payload}
'''


class LogWin(QMainWindow):
    def __init__(self, config_data, parent=None):
        super(LogWin, self).__init__(parent, flags=Qt.Widget)
        self.ui = Ui_LogWindow()
        self.ui.setupUi(self)
        self.ui.actionClear.triggered.connect(self.clear_action)
        self.__configuration = config_data

    def clear_action(self):
        self.ui.log_plain_text_edit.clear()
        pass

    def update_log_display(self, message, date_time):
        if self.ui.actionFilter.isChecked():
            if message.is_valid and message.payload.hash_id in self.__configuration.log_filter_hash_id_list:
                return
        log_text = _log_text_format.format(
            time=date_time.strftime("%Y-%m-%d %H:%M:%S"),
            qos=message.qos,
            retain=message.retain,
            topic=message.topic,
            payload='☟\n  |->' + str(message.payload).replace('\n', '\n  |->')
            if message.is_valid else message.payload)
        self.ui.log_plain_text_edit.appendPlainText(log_text)
        pass

    pass
