class DatagramMessageObserver:
    def __init__(self, identification, name='NoDefine'):
        self.__id = identification
        self.__name = name
        pass

    @property
    def identification(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    def on_msg_received(self, msg):
        return msg.is_valid

    def do_msg_received(self, msg):
        pass
    pass
