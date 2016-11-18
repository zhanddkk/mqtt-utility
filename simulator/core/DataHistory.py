class DataHistory:
    import datetime
    time = datetime.datetime(year=2000, month=1, day=1)
    value = None
    opt = 1  # 0:Send 1:Receive

    @property
    def opt_str(self):
        return 'Send' if self.opt == 0 else 'Receive'

    @property
    def time_str(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S")

    pass

if __name__ == '__main__':
    his = DataHistory()
    print(his.opt_str, his.time_str)
    pass
