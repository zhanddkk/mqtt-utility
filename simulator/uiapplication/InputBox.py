from PyQt5.QtWidgets import QLineEdit


class InputBox(QLineEdit):
    def __init__(self, parent=None, default_return_val=''):
        super(InputBox, self).__init__(parent)
        self.value_type = 'text'
        self.default_ret_val = default_return_val

    def property(self, name):
        val = self.default_ret_val
        text = self.text()
        if self.value_type == 'decimals':
            try:
                val = float(text)
            except ValueError:
                print('ERROR:', 'input value error')
                pass
            pass
        elif self.value_type == 'integral':
            try:
                text = text.upper()
                if text.startswith('0X'):
                    val = int(text, base=16)
                else:
                    val = int(text)
            except ValueError:
                print('ERROR:', 'input value error')
                pass
            pass
        elif self.value_type == 'bool':
            text = text.upper()
            try:
                if text.startswith('0X'):
                    val = int(text, base=16)
                else:
                    val = int(text)
                val = True if val != 0 else False
            except ValueError:
                if text == 'FALSE':
                    val = False
                elif text == 'TRUE':
                    val = True
                else:
                    print('ERROR:', 'input value error')
                    pass
                pass
        else:
            val = text
            pass
        return val
        pass
    pass

if __name__ == '__main__':
    pass
