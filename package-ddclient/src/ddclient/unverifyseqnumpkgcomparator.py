try:
    from .dgpayload import DatagramPayload
    from .bitmapparser import BitMapParser, command_bit_map
    from .pkgcomparator import PackageComparator
except SystemError:
    from dgpayload import DatagramPayload
    from bitmapparser import BitMapParser, command_bit_map
    from pkgcomparator import PackageComparator


class UnVerifySeqNumPackageComparator(PackageComparator):
    def __init__(self):
        super(UnVerifySeqNumPackageComparator, self).__init__()
        self.__cmd_bit_map_parser = BitMapParser(command_bit_map)

    def compare(self, pkg0, pkg1):
        ret = (pkg0 == pkg1)
        if ret:
            return ret
        _payload0 = DatagramPayload()
        _payload0.set_package(pkg0)
        if isinstance(_payload0.value, int):
            command_value = self.__cmd_bit_map_parser.decode(_payload0.value)
            _payload0.value = self.__cmd_bit_map_parser.encode(cmd_code=command_value.cmd_code.value,
                                                               sequence=0,
                                                               producer=command_value.producer.value)
        _payload0.time_stamp_second = 0
        _payload0.time_stamp_ms = 0

        _payload1 = DatagramPayload()
        _payload1.set_package(pkg1)
        if isinstance(_payload1.value, int):
            command_value = self.__cmd_bit_map_parser.decode(_payload1.value)
            _payload1.value = self.__cmd_bit_map_parser.encode(cmd_code=command_value.cmd_code.value,
                                                               sequence=0,
                                                               producer=command_value.producer.value)
        _payload1.time_stamp_second = 0
        _payload1.time_stamp_ms = 0

        return _payload0.package == _payload1.package
        pass

    pass
