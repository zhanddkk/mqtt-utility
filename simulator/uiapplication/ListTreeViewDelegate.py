from PyQt5.QtWidgets import QStyledItemDelegate, QSpinBox, QDoubleSpinBox, QLineEdit


class ListTreeViewDelegate(QStyledItemDelegate):
    def __init__(self, datagram, parent=None):
        super(ListTreeViewDelegate, self).__init__(parent)
        self.datagram = datagram
        pass

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        if self.datagram.property.format == '16BUS':
            editor = QSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(0xffff)
            pass
        elif self.datagram.property.format == '32BUS':
            editor = QSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(0xffffffff)
            pass
        elif self.datagram.property.format == '32BFL':
            editor = QDoubleSpinBox(parent)
            pass
        elif self.datagram.property.format == 'BOOL':
            editor = QSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(1)
            pass
        else:
            pass
        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
