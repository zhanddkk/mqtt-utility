try:
    from .dgpayload import DatagramPayload
except SystemError:
    from dgpayload import DatagramPayload


class MessageMatcher:
    E_COMP_PKG_ALL_MISMATCH = 0
    E_COMP_PKG_DATA_MISMATCH = 1
    E_COMP_PKG_EQUAL = 2

    def __init__(self, packages=()):
        self._packages = list(packages)
        self._is_passed = False
        pass

    @property
    def is_passed(self):
        return self._is_passed

    @classmethod
    def compare_package(cls, pkg0, pkg1):
        ret = (pkg0 == pkg1)
        if ret:
            return cls.E_COMP_PKG_EQUAL

        _payload0 = DatagramPayload()
        _payload0.set_package(pkg0)
        _payload1 = DatagramPayload()
        _payload1.set_package(pkg1)

        if (_payload0.hash_id == _payload1.hash_id) and \
                (_payload0.device_instance_index == _payload1.device_instance_index) and \
                (_payload0.action == _payload1.action):
            return cls.E_COMP_PKG_DATA_MISMATCH
        else:
            return cls.E_COMP_PKG_ALL_MISMATCH
            pass
        pass

    def verify(self, package):
        ret = False
        return ret
        pass

    pass
