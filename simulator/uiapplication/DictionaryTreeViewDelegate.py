from PyQt5.QtWidgets import QComboBox, QLineEdit, QStyledItemDelegate, QItemEditorFactory
from PyQt5.QtCore import Qt, QVariant
from simulator.uiapplication.InputBox import InputBox


class DictionaryTreeViewDelegate(QStyledItemDelegate):
    def __init__(self, datagram, parent=None):
        super(DictionaryTreeViewDelegate, self).__init__(parent)
        self.datagram = datagram
        pass

    def createEditor(self, parent, option, index):
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
            editor = InputBox(parent, default_return_val=index.data())
            editor.value_type = 'integral'
        else:
            editor = QLineEdit(parent)
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
