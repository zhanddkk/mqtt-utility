import socket
from queue import Queue
from PyQt5.QtCore import QSocketNotifier


class SafeConnector(object):
    """Share between Python thread and a Qt thread.

    Qt thread calls :method:'connect' and the python thread calls :method:'emit'.
    The slot corresponding to the emitted signal will be called in Qt's
    thread.
    """
    def __init__(self):
        self.__r_socket, self.__w_socket = socket.socketpair()
        self.__queue = Queue()
        self.__notifier = QSocketNotifier(self.__r_socket.fileno(), QSocketNotifier.Read)
        getattr(self.__notifier, 'activated').connect(self.__receive)

    @staticmethod
    def connect(signal, receiver):
        """Connect the signal to the specified receiver slot.

        :param signal: The signal to connected.
        :param receiver: The receiver slot for the signal.
        """
        signal.connect(receiver)

    def emit(self, signal, *args):
        """Emit a Qt signal from a python thread.

        All remaining args are passed to the signal.

        :param signal: The Qt signal to emit.
        """
        self.__queue.put((signal, args))
        self.__w_socket.send(b'!')

    def __receive(self):
        """Receive the signal from the Queue in Qt's main thread."""
        self.__r_socket.recv(1)
        signal, args = self.__queue.get()
        signal.emit(*args)
