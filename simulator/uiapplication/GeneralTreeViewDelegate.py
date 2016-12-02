from PyQt5.QtWidgets import QStyledItemDelegate, QItemEditorFactory
from PyQt5.QtCore import Qt, QVariant
from simulator.core.DatagramAttribute import general_data_type, integer_data_type_name
from simulator.uiapplication.InputBox import InputBox


class GeneralTreeViewDelegate(QStyledItemDelegate):
    def __init__(self, datagram, parent=None):
        super(GeneralTreeViewDelegate, self).__init__(parent)
        self.datagram = datagram
        pass

    def createEditor(self, parent, option, index):
        editor = InputBox(parent, default_return_val=index.data())
        value_type = self.datagram.attribute.format
        if value_type in general_data_type:
            if value_type in integer_data_type_name:
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

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
