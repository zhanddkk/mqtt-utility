from PyQt5.QtWidgets import QStyledItemDelegate, QItemEditorFactory
from PyQt5.QtCore import Qt, QVariant
from simulator.uiapplication.QUint32SpinBox import QUint32SpinBox


class PackageTreeWidgetDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(PackageTreeWidgetDelegate, self).__init__(parent)
        pass

    def createEditor(self, parent, option, index):
        editor = QUint32SpinBox(parent)
        editor.setRange(0, 0xffffffff)
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
