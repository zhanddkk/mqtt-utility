from PyQt5.QtWidgets import QApplication, QMainWindow
from SimulatorUI import Ui_SimulatorUI


class MainApp(QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.ui = Ui_SimulatorUI()
        self.ui.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
