try:
    from .dgpayload import DatagramPayload
except SystemError:
    from dgpayload import DatagramPayload


class PackageComparator:
    def __init__(self):
        pass

    def compare(self, pkg0, pkg1):
        _payload0 = DatagramPayload()
        _payload0.set_package(pkg0)
        _payload0.time_stamp_second = 0
        _payload0.time_stamp_ms = 0

        _payload1 = DatagramPayload()
        _payload1.set_package(pkg1)
        _payload1.time_stamp_second = 0
        _payload1.time_stamp_ms = 0

        return _payload0.package == _payload1.package
    pass



