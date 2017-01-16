from PyQt5.QtWidgets import QStyledItemDelegate


class DataAttributeTreeWidgetDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(DataAttributeTreeWidgetDelegate, self).__init__(parent)
        pass

    def paint(self, painter, option, index):
        if index.column() > 0:
            from PyQt5.QtGui import QColor
            x1, y1, x2, y2 = option.rect.getCoords()
            painter.save()
            painter.setPen(QColor(0xe8, 0xe8, 0xe8))
            _x1 = x1 - 1 if x1 > 1 else x1
            painter.drawLine(_x1, y1, _x1, y2)
            painter.restore()

        super(DataAttributeTreeWidgetDelegate, self).paint(painter, option, index)
    pass
