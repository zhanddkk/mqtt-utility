from PyQt5.QtCore import QTimer
from PyQt5.Qt import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog
from UiWaitingDlg import Ui_WaitingDialog


class WaitingDlg(QDialog):
    __time_out_signal = pyqtSignal(bool, name='TimeOutSignal')
    __timer_counter_update_display_signal = pyqtSignal(int, name='TimerCounterUpdateDisplaySignal')

    def __init__(self, parent=None):
        super(WaitingDlg, self).__init__(parent, flags=Qt.FramelessWindowHint)
        self.ui = Ui_WaitingDialog()
        self.ui.setupUi(self)
        self.__time_out_signal.connect(self.quit)
        self.__result = False
        self.__timer_counter_update_display_signal.connect(self.__timer_counter_update_display)
        self.__timer_counter = 0

        self.__waiting_timer = QTimer(self)
        getattr(self.__waiting_timer, 'timeout').connect(self.__emit_update_timer)
        self.__waiting_timer.start(1000)

    def quit(self, ret):
        self.__waiting_timer.stop()
        self.__result = ret
        self.close()

    def __emit_update_timer(self):
        self.__timer_counter += 1
        self.__timer_counter_update_display_signal.emit(self.__timer_counter)
        pass

    def __timer_counter_update_display(self, counter):
        self.ui.time_lcd_number.display(counter)
        pass

    @property
    def time_out_signal(self):
        return self.__time_out_signal

    @property
    def result(self):
        return self.__result
    pass
