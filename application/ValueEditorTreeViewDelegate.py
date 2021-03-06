from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QComboBox, QLineEdit, QStyledItemDelegate
from PyQt5.Qt import Qt


class ValueEditorTreeViewDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ValueEditorTreeViewDelegate, self).__init__(parent)
        pass

    def createEditor(self, parent, option, index):
        _editor = QLineEdit(parent)
        _widget = option.widget
        _model = _widget.model()
        if _model is None:
            return _editor
        _item = _model.get_item(index)
        _current_data = index.data()
        try:
            if _item.hide_data.system_tag == 'EnumType':
                if _item.hide_data.special_data:
                    _editor = QComboBox(parent)
                    _editor.setEditable(True)
                    _item_text_list = []
                    for item in sorted(_item.hide_data.special_data.items(), key=lambda _d: _d[1].value):
                        _item_text_list.append('{value} | {name}'.format(value=item[1].value, name=item[0]))
                    _editor.addItems(_item_text_list)
                    pass
            elif _item.hide_data.system_tag == 'BasicType':
                if _item.hide_data.basic_type == 'Bool':
                    _editor = QComboBox(parent)
                    _editor.setEditable(True)
                    _editor.addItems(('True', 'False'))
        except AttributeError:
            try:
                if _item.hide_data.names:
                    _editor = QComboBox(parent)
                    _editor.setEditable(True)
                    _item_text_list = []
                    for item in sorted(_item.hide_data.names.items(), key=lambda _d: _d[1]):
                        _item_text_list.append('{value} | {name}'.format(value=item[1], name=item[0]))
                    _editor.addItems(_item_text_list)
                    pass
            except AttributeError:
                pass
            pass
        try:
            _current_index = _editor.findText(_current_data, Qt.MatchExactly | Qt.MatchCaseSensitive)
            if _current_index == -1:
                pass
            else:
                _editor.setCurrentIndex(_current_index)
        except AttributeError:
            pass
        return _editor

    def sizeHint(self, option, model):
        size = super(ValueEditorTreeViewDelegate, self).sizeHint(option, model)
        font = option.widget.font()
        font_metrics = QFontMetrics(font)
        font_height = font_metrics.height() + 4
        size.setHeight(font_height)
        return size

    def paint(self, painter, option, index):
        from PyQt5.QtGui import QColor
        x1, y1, x2, y2 = option.rect.getCoords()
        painter.save()
        painter.setPen(QColor(Qt.gray))
        if index.column() > 0:
            _x1 = x1 - 1 if x1 > 1 else x1
            painter.drawLine(_x1, y1, _x1, y2)
            painter.drawLine(x1, y2, x2, y2)
        else:
            painter.drawLine(0, y2, x2, y2)
        painter.restore()

        super(ValueEditorTreeViewDelegate, self).paint(painter, option, index)
