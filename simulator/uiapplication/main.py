from PyQt5.QtWidgets import QApplication, QMainWindow
from simulator.uiform.SimulatorUI import Ui_SimulatorUI
from simulator.datadictionary.DatagramManager import DatagramManager

class MainApp(QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.ui = Ui_SimulatorUI()
        self.ui.setupUi(self)

if __name__ == "__main__":
    import sys
    b = DatagramManager()
    b.import_datagram()
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
