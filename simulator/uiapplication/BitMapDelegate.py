from PyQt5.QtWidgets import QStyledItemDelegate, QItemEditorFactory, QComboBox
from PyQt5.QtCore import Qt, QVariant
from simulator.core.DatagramAttribute import general_data_type, integer_data_type_name
from simulator.uiapplication.InputBox import InputBox


class BitMapDelegate(QStyledItemDelegate):
    def __init__(self, datagram, bit_format, parent=None):
        super(BitMapDelegate, self).__init__(parent)
        self.datagram = datagram
        self.bit_format = bit_format
        pass

    def createEditor(self, parent, option, index):
        editor = InputBox(parent, default_return_val=index.data())
        editor.value_type = 'integral'
        row = index.row()
        try:
            bit_field = self.bit_format.fields[len(self.bit_format.fields) - row - 1]
            choice_list = getattr(self.bit_format, bit_field)[1]
            if type(choice_list) is dict:
                editor = QComboBox(parent=parent)
                editor.setEditable(True)
                data = index.data()
                str_list = []
                if choice_list != {}:
                    str_list = []
                    for item in sorted(choice_list.items(), key=lambda d: d[0]):
                        text = str(item[0]) + ' | ' + item[1]
                        str_list.append(text)
                editor.addItems(str_list)
                if data:
                    editor.setCurrentText(data)
                else:
                    editor.setCurrentIndex(0)
        except IndexError:
            print('ERROR:', 'Can not find bit field', row)
        return editor

    def setModelData(self, editor, model, index):
        n = editor.metaObject().userProperty().name()
        if n is None:
            item_editor_factory = self.itemEditorFactory()
            if item_editor_factory is None:
                item_editor_factory = QItemEditorFactory.defaultFactory()
            user_type = QVariant(model.data(index, Qt.EditRole)).userType()
            n = item_editor_factory.valuePropertyName(user_type)
            pass
        if n is not None:
            model.setData(index, editor.property(n), Qt.EditRole)
            pass
        pass

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


