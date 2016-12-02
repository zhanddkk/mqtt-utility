from PyQt5.QtWidgets import QStyledItemDelegate, QItemEditorFactory
from PyQt5.QtCore import Qt, QVariant
from simulator.core.DatagramAttribute import general_data_type, integer_data_type_name
from simulator.uiapplication.InputBox import InputBox

package_type_list = [
    'UInt16',
    'UInt16',
    'UInt32',
    'UInt32',
    'UInt16',
    'UInt32',
    'UInt16',
    'UInt16',
    'Bool',
    'UInt16',
    'UInt16'
]


class PackageTreeWidgetDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(PackageTreeWidgetDelegate, self).__init__(parent)
        pass

    def createEditor(self, parent, option, index):
        editor = InputBox(parent, default_return_val=index.data())
        value_type = package_type_list[index.row()]
        if value_type in general_data_type:
            if value_type in integer_data_type_name:
                if value_type == 'Bool':
                    editor.value_type = 'bool'
                else:
                    editor.value_type = 'integral'
                pass
            else:
                editor.value_type = 'decimals'
                pass
            pass
        else:
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
