from PyQt5.QtWidgets import QStyledItemDelegate, QSpinBox
# from PyQt5.QtCore import Qt, QSize


class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(SpinBoxDelegate, self).__init__(parent)
        self.max_num = None
        self.min_num = None
        pass

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        if self.max_num is not None:
            editor.setMaximum(self.max_num)
        if self.min_num is not None:
            editor.setMinimum(self.min_num)

        return editor

    # def setEditorData(self, spin_box, index):
    #    value = index.model().data(index, Qt.EditRole)
    #    spin_box.setValue(value)

    # def setModelData(self, spin_box, model, index):
    #    spin_box.interpretText()
    #    value = spin_box.value()

    #    model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    # def sizeHint(self, option, index):
    #     print('sizeHint', index.row(), index.column())
    #     return QSize(64, 64)
