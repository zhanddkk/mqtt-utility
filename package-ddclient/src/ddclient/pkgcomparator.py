try:
    from .dgpayload import DatagramPayload
except SystemError:
    from dgpayload import DatagramPayload


class PackageComparator:
    def __init__(self):
        pass

    @staticmethod
    def clear_time_stamp(payload0, payload1):
        setattr(payload0, 'time_stamp_second', 0)
        setattr(payload0, 'time_stamp_ms', 0)
        setattr(payload1, 'time_stamp_second', 0)
        setattr(payload1, 'time_stamp_ms', 0)

    def compare(self, pkg0, pkg1):
        _payload0 = DatagramPayload()
        _payload0.set_package(pkg0)

        _payload1 = DatagramPayload()
        _payload1.set_package(pkg1)

        self.clear_time_stamp(_payload0, _payload1)
        return _payload0.package == _payload1.package
    pass
