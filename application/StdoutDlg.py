from PyQt5.Qt import Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QBrush, QColor
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QProcess, QObject, pyqtSignal
from UiStdoutDlg import Ui_StdoutDlg


class StdoutDlg(QDialog):
    print_signal = pyqtSignal(str, int, int, int, int, name='PrintSignal')
    close_signal = pyqtSignal(name='CloseSignal')

    def __init__(self, parent=None):
        super(StdoutDlg, self).__init__(parent, flags=Qt.Window)
        self.ui = Ui_StdoutDlg()
        self.ui.setupUi(self)
        self.print_signal.connect(self.__process_puts)
        self.close_signal.connect(self.quit)

    def puts(self, string, r=0, g=0, b=0, a=255):
        self.print_signal.emit(string, r, g, b, a)
        pass

    def quit(self):
        self.close()
        pass

    def __process_puts(self, string, r, g, b, a):
        tmp = QTextCursor(self.ui.stdout_text_edit.document())
        vbar = self.ui.stdout_text_edit.verticalScrollBar()
        at_bottom = vbar.value() >= vbar.maximum() if self.ui.stdout_text_edit.isReadOnly() else \
            self.ui.stdout_text_edit.textCursor().atEnd()

        tmp.beginEditBlock()
        tmp.movePosition(QTextCursor.End)

        old_format = self.ui.stdout_text_edit.currentCharFormat()
        new_format = QTextCharFormat(old_format)

        new_format.setForeground(QBrush(QColor(r, g, b, a)))
        tmp.setCharFormat(new_format)

        tmp.insertText(string)

        if self.ui.stdout_text_edit.textCursor().hasSelection():
            self.ui.stdout_text_edit.setCurrentCharFormat(old_format)

        tmp.endEditBlock()

        if at_bottom:
            vbar.setValue(vbar.maximum())
        pass


class ProcessStdoutDlg(QDialog):
    def __init__(self, parent=None, process=QProcess(), title_name=None):
        super(ProcessStdoutDlg, self).__init__(parent, flags=Qt.Window)
        self.ui = Ui_StdoutDlg()
        self.ui.setupUi(self)
        if isinstance(title_name, str):
            self.setWindowTitle(title_name)
            pass
        self.process_stdout_message = ProcessStdoutMessage()
        self.process = process
        self.process.readyReadStandardOutput.connect(self.stdout_process)
        self.process.readyReadStandardError.connect(self.stderr_process)
        self.process.finished.connect(self.close)
        # self.__process_stdout_message.message_signal.connect(self.stdout_on_message)

    def stdout_process(self):
        tmp = QTextCursor(self.ui.stdout_text_edit.document())
        vbar = self.ui.stdout_text_edit.verticalScrollBar()
        at_bottom = vbar.value() >= vbar.maximum() if self.ui.stdout_text_edit.isReadOnly() else\
            self.ui.stdout_text_edit.textCursor().atEnd()

        tmp.beginEditBlock()
        tmp.movePosition(QTextCursor.End)

        old_format = self.ui.stdout_text_edit.currentCharFormat()
        new_format = QTextCharFormat(old_format)

        new_format.setForeground(QBrush(QColor(0, 0, 0)))
        tmp.setCharFormat(new_format)

        _text = bytes(self.process.readAllStandardOutput()).decode()
        self.process_stdout_message.parser(_text)
        tmp.insertText(_text)

        if self.ui.stdout_text_edit.textCursor().hasSelection():
            self.ui.stdout_text_edit.setCurrentCharFormat(old_format)

        tmp.endEditBlock()

        if at_bottom:
            vbar.setValue(vbar.maximum())
        pass

    def stderr_process(self):
        tmp = QTextCursor(self.ui.stdout_text_edit.document())
        vbar = self.ui.stdout_text_edit.verticalScrollBar()
        at_bottom = vbar.value() >= vbar.maximum() if self.ui.stdout_text_edit.isReadOnly() else \
            self.ui.stdout_text_edit.textCursor().atEnd()

        tmp.beginEditBlock()
        tmp.movePosition(QTextCursor.End)

        old_format = self.ui.stdout_text_edit.currentCharFormat()
        new_format = QTextCharFormat(old_format)

        new_format.setForeground(QBrush(QColor(0xff, 0, 0)))
        tmp.setCharFormat(new_format)

        _text = bytes(self.process.readAllStandardError()).decode()

        tmp.insertText(_text)

        if self.ui.stdout_text_edit.textCursor().hasSelection():
            self.ui.stdout_text_edit.setCurrentCharFormat(old_format)

        tmp.endEditBlock()

        if at_bottom:
            vbar.setValue(vbar.maximum())
        pass

    # def stdout_on_message(self, msg):
    #     print(msg)

    def closeEvent(self, close_event):
        self.process.kill()
        # import sys
        # self.process.write(bytearray('stop\n', encoding=sys.getfilesystemencoding()))
        pass

    pass


class ProcessStdoutMessage(QObject):
    message_signal = pyqtSignal(str, name='MessageSignal')

    def __init__(self, parent=None):
        super(ProcessStdoutMessage, self).__init__(parent)
        self.__last_str = ''
        self.__start_index = 0
        self.__start_depth = 0
        pass

    def parser(self, string):
        start_index = 0
        index = 0
        for sub_str in string:
            if sub_str == '{':
                if self.__start_depth == 0:
                    start_index = index
                self.__start_depth += 1
            elif sub_str == '}':
                self.__start_depth -= 1
                if self.__start_depth == 0:
                    if self.__last_str:
                        msg = self.__last_str + string[start_index:index]
                        self.__last_str = ''
                    else:
                        msg = string[start_index:index].lstrip('{')
                    self.message_signal.emit(msg)
                    pass
                elif self.__start_depth < 0:
                    self.__start_depth = 0
            index += 1
        if self.__start_depth > 0:
            self.__last_str += string[start_index + 1:]
        pass

    @property
    def messages(self):
        return self.__messages
    pass


if __name__ == '__main__':
    pass
