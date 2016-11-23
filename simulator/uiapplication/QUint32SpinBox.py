from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtGui import QRegExpValidator, QValidator
from PyQt5.QtCore import QRegExp, Qt
exp_str_map = {
    10: "[0-9]{1,10}",
    16: "[0-9A-Fa-f]{1,8}"
}


class QUint32SpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(QUint32SpinBox, self).__init__(parent)
        self._display_integer_base = 10
        regex = QRegExp(exp_str_map[self._display_integer_base])
        regex.setCaseSensitivity(Qt.CaseInsensitive)
        self.validator = QRegExpValidator(regex, self)
        self.setDecimals(0)

    def validate(self, p_str, p_int):
        ret = self.validator.validate(p_str, p_int)
        if ret[0] == QValidator.Acceptable:
            text_input = self.lineEdit().text()
            val = int(text_input, self._display_integer_base)
            if(val > self.maximum()) or (val < self.minimum()):
                ret = (QValidator.Invalid, text_input, len(text_input))
                pass
            pass
        return ret

    @property
    def displayIntegerBase(self):
        return self._display_integer_base

    def property(self, name):
        if name == 'value':
            return int(self.value())
        return None
        pass

    def setDisplayIntegerBase(self, base):
        if (base == 10) or (base == 16):
            self._display_integer_base = base
        else:
            print('ERROR:', base, 'is invalid integer base')
            self._display_integer_base = 10
        regex = QRegExp(exp_str_map[self._display_integer_base])
        regex.setCaseSensitivity(Qt.CaseInsensitive)
        self.validator = QRegExpValidator(regex, self)
        pass

    def textFromValue(self, val):
        val = int(val)
        if self._display_integer_base == 10:
            text = str(val)
            pass
        elif self._display_integer_base == 16:
            text = hex(val)[2:]
            pass
        else:
            text = str(val)
            pass
        return text
        pass

    def valueFromText(self, p_str):
        return int(p_str, self._display_integer_base)
        pass
    pass
