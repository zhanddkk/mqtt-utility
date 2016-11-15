from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtGui import QRegExpValidator, QValidator
from PyQt5.QtCore import QRegExp, Qt


class QUint32SpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(QUint32SpinBox, self).__init__(parent)
        regex = QRegExp("[0-9]{1,10}")
        regex.setCaseSensitivity(Qt.CaseInsensitive)
        self.validator = QRegExpValidator(regex, self)
        self.setDecimals(0)

    def validate(self, p_str, p_int):
        ret = self.validator.validate(p_str, p_int)
        if ret[0] == QValidator.Acceptable:
            text_input = self.lineEdit().text()
            val = int(text_input)
            if(val > self.maximum()) or (val < self.minimum()):
                ret = (QValidator.Invalid, text_input, len(text_input))
                pass
            pass
        return ret

    def property(self, name):
        if name == 'value':
            return int(self.value())
        return None
        pass

    pass
