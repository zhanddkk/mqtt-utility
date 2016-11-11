from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, data=[], parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.combobox_data = data
        pass

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        data = index.data()
        editor.addItems(self.combobox_data)
        if data:
            editor.setCurrentText(data)
        else:
            editor.setCurrentIndex(0)
        return editor
    pass
