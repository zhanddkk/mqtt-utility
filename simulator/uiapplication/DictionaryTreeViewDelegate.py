from PyQt5.QtWidgets import QStyledItemDelegate, QSpinBox, QComboBox, QLineEdit    # , QDoubleSpinBox


class DictionaryTreeViewDelegate(QStyledItemDelegate):
    def __init__(self, datagram, parent=None):
        super(DictionaryTreeViewDelegate, self).__init__(parent)
        self.datagram = datagram
        pass

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        if index.column() == 0:
            editor = QComboBox(parent)
            data = index.data()
            choice_list = self.datagram.property.choice_list
            str_list = []
            if choice_list != {}:
                str_list = []
                for (k, d) in choice_list.items():
                    str_list.append(k)
                str_list.sort()
            str_list.append('USER DEFINE')
            editor.addItems(str_list)
            if data:
                editor.setCurrentText(data)
            else:
                editor.setCurrentIndex(0)
        elif index.column() == 1:
            if self.datagram.property.format == '16BUS':
                editor = QSpinBox(parent)
                editor.setMinimum(0)
                editor.setMaximum(0xffff)
                pass
            else:
                pass
        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
