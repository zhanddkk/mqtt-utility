from PyQt5.QtWidgets import (QStyledItemDelegate, QSpinBox, QDoubleSpinBox,
                             QLineEdit, QItemEditorFactory)
from PyQt5.QtCore import Qt, QVariant
from simulator.uiapplication.QUint32SpinBox import QUint32SpinBox

integer_data_type_info = {
    'int8_t': [-128, 127],
    'int16_t': [-32768, 32767],
    'int32_t': [-2147483648, 2147483647],
    'bool': [0, 1],
    'uint8_t': [0, 0xff],
    'uint16_t': [0, 0xffff],
    'uint32_t': [0, 0xffffffff],
}


class StructTreeViewDelegate(QStyledItemDelegate):
    def __init__(self, datagram, parent=None):
        super(StructTreeViewDelegate, self).__init__(parent)
        self.datagram = datagram
        pass

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

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        model = index.model()
        value_type = model.get_item(index).data(1)
        try:
            info = integer_data_type_info[value_type]
            if info[1] > 2147483647:
                editor = QUint32SpinBox(parent)
                pass
            else:
                editor = QSpinBox(parent)
            editor.setRange(info[0], info[1])
            pass
        except KeyError:
            if value_type == 'float':
                editor = QDoubleSpinBox(parent)
                pass
            pass
        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


if __name__ == "__main__":
    pass
