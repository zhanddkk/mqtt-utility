from PyQt5.QtCore import QThread


class QSimpleThread(QThread):
    def __init__(self, target, args):
        super(QSimpleThread, self).__init__()
        self.__target = target
        self.__args = args

    def run(self):
        self.__target(*self.__args)
    pass
