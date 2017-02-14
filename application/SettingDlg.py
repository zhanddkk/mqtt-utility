from PyQt5.Qt import Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog
from UiSettingDlg import Ui_SettingDialog
from LogFilterDataTableViewModel import LogFilterDataTableViewModel


class SettingDlg(QDialog):
    E_CONNECT_BROKER_IP = 0b1
    E_CONNECT_BROKER_IP_PORT = 0b10
    E_LOG_FILTER_DATA = 0b100

    def __init__(self, configuration_info, parent=None):
        super(SettingDlg, self).__init__(parent, flags=Qt.Window)
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)

        self.__is_edited_mask = 0

        self.ui.apply_push_button.clicked.connect(self.apply)
        self.ui.contents_list_widget.currentItemChanged.connect(self.change_page)
        self.ui.broker_address_line_edit.textChanged.connect(self.edit_connect_broker_ip)
        self.ui.broker_port_spin_box.valueChanged.connect(self.edit_connect_broker_ip_port)

        self.__configuration = configuration_info
        self.ui.broker_address_line_edit.setText(self.__configuration.connect_broker_ip)
        self.ui.broker_port_spin_box.setValue(self.__configuration.connect_broker_ip_port)
        self.__log_filter_data_table_view_module =\
            LogFilterDataTableViewModel(self.__configuration.log_filter_hash_id_list)
        self.ui.log_filter_data_table_view.setModel(self.__log_filter_data_table_view_module)
        self.ui.log_filter_data_table_view.itemDelegate().closeEditor.connect(self.log_filter_data_table_view_end_edit)

        self.ui.contents_list_widget.setCurrentRow(0)

    def __update_display_status(self):
        if self.__is_edited_mask != 0:
            if not self.ui.apply_push_button.isEnabled():
                self.ui.apply_push_button.setEnabled(True)
            self.ui.status_label.clear()
        else:
            self.ui.apply_push_button.setEnabled(False)
        pass

    def log_filter_data_table_view_end_edit(self):  # (self, editor, hint):
        if self.__configuration.log_filter_hash_id_list != self.__log_filter_data_table_view_module.data_list:
            self.__is_edited_mask |= self.E_LOG_FILTER_DATA
        else:
            self.__is_edited_mask &= ~self.E_LOG_FILTER_DATA
        self.__update_display_status()
        pass

    def accept(self):
        self.apply()
        super(SettingDlg, self).accept()
        pass

    def apply(self):
        if self.ui.apply_push_button.isEnabled():
            self.__configuration.connect_broker_ip = self.ui.broker_address_line_edit.text()
            self.__configuration.connect_broker_ip_port = self.ui.broker_port_spin_box.value()
            self.__configuration.log_filter_hash_id_list = self.__log_filter_data_table_view_module.data_list
            self.__configuration.save_config()
            self.ui.status_label.setText('Saved')
            self.__is_edited_mask = 0
            self.ui.apply_push_button.setEnabled(False)
        pass

    def edit_connect_broker_ip(self):
        if self.ui.broker_address_line_edit.text() != self.__configuration.connect_broker_ip:
            self.__is_edited_mask |= self.E_CONNECT_BROKER_IP
        else:
            self.__is_edited_mask &= ~self.E_CONNECT_BROKER_IP
        self.__update_display_status()
        pass

    def edit_connect_broker_ip_port(self):
        if self.ui.broker_port_spin_box.value() != self.__configuration.connect_broker_ip_port:
            self.__is_edited_mask |= self.E_CONNECT_BROKER_IP_PORT
        else:
            self.__is_edited_mask &= ~self.E_CONNECT_BROKER_IP_PORT
        self.__update_display_status()
        pass

    def change_page(self, current, previous):
        if not current:
            current = previous
        self.ui.page_stacked_widget.setCurrentIndex(self.ui.contents_list_widget.row(current))
        pass

    @pyqtSlot(name='')
    def on_add_push_button_clicked(self):
        _model = self.ui.log_filter_data_table_view.model()
        if not _model:
            return
        _row = _model.rowCount()
        _model.insertRow(_row)
        self.ui.log_filter_data_table_view.edit(_model.index(_row, 0))
        if self.__configuration.log_filter_hash_id_list != _model.data_list:
            self.__is_edited_mask |= self.E_LOG_FILTER_DATA
        else:
            self.__is_edited_mask &= ~self.E_LOG_FILTER_DATA
        self.__update_display_status()
        pass

    @pyqtSlot(name='')
    def on_delete_push_button_clicked(self):
        _model = self.ui.log_filter_data_table_view.model()
        if not _model:
            return
        _item_index = self.ui.log_filter_data_table_view.selectionModel().currentIndex()
        _row = _item_index.row()
        if _row < 0:
            return
        _model.removeRow(_row)
        if self.__configuration.log_filter_hash_id_list != _model.data_list:
            self.__is_edited_mask |= self.E_LOG_FILTER_DATA
        else:
            self.__is_edited_mask &= ~self.E_LOG_FILTER_DATA
        self.__update_display_status()
        pass

    pass
