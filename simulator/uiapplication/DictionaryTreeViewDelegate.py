from PyQt5.QtWidgets import QStyledItemDelegate, QSpinBox, QComboBox, QLineEdit
from simulator.core.DatagramAttribute import integer_data_type_info
from simulator.uiapplication.QUint32SpinBox import QUint32SpinBox


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
            choice_list = self.datagram.attribute.choice_list
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
            try:
                info = integer_data_type_info[self.datagram.attribute.format]
                if info[1] > 2147483647:
                    editor = QUint32SpinBox(parent)
                    pass
                else:
                    editor = QSpinBox(parent)
                editor.setRange(info[0], info[1])
                pass
            except KeyError:
                pass
        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
