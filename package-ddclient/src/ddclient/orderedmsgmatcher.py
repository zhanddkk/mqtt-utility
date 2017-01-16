try:
    from .msgmatcher import MessageMatcher
except SystemError:
    from msgmatcher import MessageMatcher


class OrderedMessageMatcher(MessageMatcher):

    def __init__(self, packages=()):
        super(OrderedMessageMatcher, self).__init__(packages)
        self.__package_index = 0
        pass

    def verify(self, package):
        """
        ordered check
        :param package:
        :return:
        """
        ret = False
        try:
            try:
                _package = self._packages[self.__package_index]
                if package == _package:
                    self.__package_index += 1
                    if self.__package_index == len(self._packages):
                        self._is_passed = True
                        pass
                    pass
                    ret = True
                else:
                    pass
            except IndexError:
                pass
        except ValueError:
            pass
        return ret
        pass

    def first_package(self, package):
        self._packages = [package]
        pass

    def then_package(self, package):
        self._packages.append(package)

    pass
