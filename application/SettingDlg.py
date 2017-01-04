from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDialog
from UiSettingDlg import Ui_SettingDialog


class SettingDlg(QDialog):
    def __init__(self, configuration_info, parent=None):
        super(SettingDlg, self).__init__(parent, flags=Qt.Window)
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)

        self.ui.apply_push_button.clicked.connect(self.apply)
        self.ui.contents_list_widget.currentItemChanged.connect(self.change_page)
        self.ui.broker_address_line_edit.textChanged.connect(self.edit_connect_broker_ip)
        self.ui.broker_port_spin_box.valueChanged.connect(self.edit_connect_broker_ip_port)

        self.__configuration = configuration_info
        self.ui.broker_address_line_edit.setText(self.__configuration.connect_broker_ip)
        self.ui.broker_port_spin_box.setValue(self.__configuration.connect_broker_ip_port)

    def accept(self):
        self.apply()
        super(SettingDlg, self).accept()
        pass

    def apply(self):
        if self.ui.apply_push_button.isEnabled():
            self.__configuration.connect_broker_ip = self.ui.broker_address_line_edit.text()
            self.__configuration.connect_broker_ip_port = self.ui.broker_port_spin_box.value()
            self.__configuration.save_config()
            self.ui.status_label.setText('Saved')
            self.ui.apply_push_button.setEnabled(False)
        pass

    def edit_connect_broker_ip(self):
        if self.ui.broker_address_line_edit.text() != self.__configuration.connect_broker_ip:
            if not self.ui.apply_push_button.isEnabled():
                self.ui.apply_push_button.setEnabled(True)
            self.ui.status_label.clear()
        else:
            self.ui.apply_push_button.setEnabled(False)
        pass

    def edit_connect_broker_ip_port(self):
        if self.ui.broker_port_spin_box.value() != self.__configuration.connect_broker_ip_port:
            if not self.ui.apply_push_button.isEnabled():
                self.ui.apply_push_button.setEnabled(True)
            self.ui.status_label.clear()
        else:
            self.ui.apply_push_button.setEnabled(False)
        pass

    def change_page(self, current, previous):
        if not current:
            current = previous
        self.ui.page_stacked_widget.setCurrentIndex(self.ui.contents_list_widget.row(current))
        pass
    pass
