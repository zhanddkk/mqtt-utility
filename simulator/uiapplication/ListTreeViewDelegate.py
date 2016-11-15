from PyQt5.QtWidgets import QStyledItemDelegate, QSpinBox, QDoubleSpinBox, QLineEdit, QItemEditorFactory
from PyQt5.QtCore import Qt, QVariant
from simulator.uiapplication.QUint32SpinBox import QUint32SpinBox

integer_data_type_info = {
    "BOOL": [0, 1],
    "8BS": [-128, 127],
    "8BUS": [0, 0xff],
    "16BS": [-32768, 32767],
    "16BUS": [0, 0xffff],
    "32BS": [-2147483648, 2147483647],
    "32BUS": [0, 0xffffffff],
}
#    "32BFL": "initPresetValueFloat32",
#    "32BMASK": "initPresetValueUint32",
#    "BINARY_BLOC": "initPresetValueString",
#    "STRING": "initPresetValueString"};


class ListTreeViewDelegate(QStyledItemDelegate):
    def __init__(self, datagram, parent=None):
        super(ListTreeViewDelegate, self).__init__(parent)
        self.datagram = datagram
        pass

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        value_type = self.datagram.property.format
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
            if value_type == '32BFL':
                editor = QDoubleSpinBox(parent)
                pass
            pass
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
