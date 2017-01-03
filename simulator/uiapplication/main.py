########################################################################################################################
# Simulation main application
########################################################################################################################
import sys
import os as _os
_path = _os.path.dirname(__file__)
_path_root = _os.path.join(_path, '../../')
_path_application = _os.path.join(_path, '../')
sys.path.append(_path_root)
sys.path.append(_path_application)
########################################################################################################################
except_hook = sys.excepthook


def exception_hook(exc_type, value, traceback):
    except_hook(exc_type, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook
########################################################################################################################
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QStyleFactory
    from MainWin import MainWin

    QApplication.setStyle(QStyleFactory().create("Fusion"))
    app = QApplication(sys.argv)
    window = MainWin()
    window.show()
    ret = app.exec_()
    window.release_resource()
    sys.exit(ret)
    pass
