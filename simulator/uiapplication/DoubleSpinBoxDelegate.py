from PyQt5.QtWidgets import QStyledItemDelegate, QDoubleSpinBox


class DoubleSpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(DoubleSpinBoxDelegate, self).__init__(parent)
        self.max_num = None
        self.min_num = None
        self.decimals = None
        pass

    def createEditor(self, parent, option, index):
        editor = QDoubleSpinBox(parent)
        if self.max_num is not None:
            editor.setMaximum(self.max_num)
        if self.min_num is not None:
            editor.setMinimum(self.min_num)
        if self.decimals is not None:
            editor.setDecimals(self.decimals)

        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
