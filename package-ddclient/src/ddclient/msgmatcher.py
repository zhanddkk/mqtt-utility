try:
    from .dgpayload import DatagramPayload
    from .pkgcomparator import PackageComparator
except SystemError:
    from dgpayload import DatagramPayload
    from pkgcomparator import PackageComparator


class MessageMatcher:
    E_COMP_PKG_ALL_MISMATCH = 0
    E_COMP_PKG_DATA_MISMATCH = 1
    E_COMP_PKG_EQUAL = 2

    def __init__(self, packages=()):
        self._packages = list(packages)
        self._is_passed = False
        self.__pkg_comparator = PackageComparator()
        pass

    @property
    def is_passed(self):
        return self._is_passed

    def set_comparator(self, comparator):
        self.__pkg_comparator = comparator

    def compare_package(self, pkg0, pkg1):
        return self.__pkg_comparator.compare(pkg0, pkg1)
        pass

    def verify(self, package):
        ret = False
        return ret
        pass

    pass
