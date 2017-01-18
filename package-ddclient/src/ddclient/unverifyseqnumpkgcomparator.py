try:
    from .dgpayload import DatagramPayload
    from .bitmapparser import bit_map_parser, command_bit_map_format_type
    from .pkgcomparator import PackageComparator
except SystemError:
    from dgpayload import DatagramPayload
    from bitmapparser import bit_map_parser, command_bit_map_format_type
    from pkgcomparator import PackageComparator


class UnVerifySeqNumPackageComparator(PackageComparator):
    def __init__(self):
        super(UnVerifySeqNumPackageComparator, self).__init__()

    def compare(self, pkg0, pkg1):
        ret = (pkg0 == pkg1)
        if ret:
            return ret
        _payload0 = DatagramPayload()
        _payload0.set_package(pkg0)
        if isinstance(_payload0.value, int):
            _payload0.value &= 0xff0000ff
        _payload1 = DatagramPayload()
        _payload1.set_package(pkg1)
        if isinstance(_payload1.value, int):
            _payload1.value &= 0xff0000ff
        return _payload0.package == _payload1.package
        pass

    pass
