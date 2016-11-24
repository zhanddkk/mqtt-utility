from PyQt5.QtWidgets import QStyledItemDelegate, QItemEditorFactory, QSpinBox, QLineEdit
from PyQt5.QtCore import Qt, QVariant
from simulator.uiapplication.QUint32SpinBox import QUint32SpinBox
from simulator.core.DatagramAttribute import integer_data_type_info

package_type_list = [
    'uint16_t',
    'uint16_t',
    'uint32_t',
    'uint32_t',
    'uint16_t',
    'uint32_t',
    'uint16_t',
    'uint16_t',
    'bool',
    'uint16_t',
    'uint16_t'
]


class PackageTreeWidgetDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(PackageTreeWidgetDelegate, self).__init__(parent)
        pass

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        try:
            row = index.row()
            value_type = package_type_list[row]
            info = integer_data_type_info[value_type]
            if info[1] > 2147483647:
                editor = QUint32SpinBox(parent)
                pass
            else:
                editor = QSpinBox(parent)
            editor.setRange(info[0], info[1])
            if row == 3:
                editor.setDisplayIntegerBase(16)
            pass
        except IndexError:
            pass
        except KeyError:
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
    pass
