from PyQt5.QtWidgets import QDialog
from simulator.uiapplication.SettingDlgUi import Ui_SettingDialog


class SettingDlg(QDialog):
    def __init__(self, configuration_info, parent=None):
        super(SettingDlg, self).__init__(parent)
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)

        self.ui.apply_push_button.clicked.connect(self.apply)
        self.ui.contents_list_widget.currentItemChanged.connect(self.change_page)
        self.ui.broker_address_line_edit.textChanged.connect(self.edit_mqtt_connect_addr)
        self.ui.broker_port_spin_box.valueChanged.connect(self.edit_mqtt_connect_port)

        self.configuration = configuration_info
        self.ui.broker_address_line_edit.setText(self.configuration.mqtt_connect_addr)
        self.ui.broker_port_spin_box.setValue(self.configuration.mqtt_connect_port)

    def accept(self):
        self.apply()
        super(SettingDlg, self).accept()
        pass

    def apply(self):
        if self.ui.apply_push_button.isEnabled():
            self.configuration.mqtt_connect_addr = self.ui.broker_address_line_edit.text()
            self.configuration.mqtt_connect_port = self.ui.broker_port_spin_box.value()
            self.configuration.save_config()
            self.ui.status_label.setText('Saved')
            self.ui.apply_push_button.setEnabled(False)
        pass

    def edit_mqtt_connect_addr(self):
        if self.ui.broker_address_line_edit.text() != self.configuration.mqtt_connect_addr:
            if not self.ui.apply_push_button.isEnabled():
                self.ui.apply_push_button.setEnabled(True)
            self.ui.status_label.clear()
        else:
            self.ui.apply_push_button.setEnabled(False)
        pass

    def edit_mqtt_connect_port(self):
        if self.ui.broker_port_spin_box.value() != self.configuration.mqtt_connect_port:
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
