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

    def print_same_hash_id_package(self, received_package, expect_package):
        received_payload = DatagramPayload()
        received_payload.set_package(received_package)
        expect_payload = DatagramPayload()
        expect_payload.set_package(expect_package)
        result = False
        if received_payload.hash_id == expect_payload.hash_id:
            print("Received:", received_package)
            print("expected", expect_package)

    def compare_package(self, pkg0, pkg1):
        equal = self.__pkg_comparator.compare(pkg0, pkg1)
        self.print_same_hash_id_package(pkg0, pkg1)
        if equal:
            print("Packages are equal.")
        return equal

    def verify(self, package):
        raise Exception("MessageMatcher should not be used directly.")
