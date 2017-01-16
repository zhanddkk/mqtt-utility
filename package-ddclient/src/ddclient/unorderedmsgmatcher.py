try:
    from .msgmatcher import MessageMatcher
except SystemError:
    from msgmatcher import MessageMatcher


class UnorderedMessageMatcher(MessageMatcher):
    def __init__(self, packages=()):
        super(UnorderedMessageMatcher, self).__init__(packages)
        pass

    @property
    def is_passed(self):
        return self._is_passed

    def verify(self, package):
        """
        unordered check
        :param package:
        :return:
        """
        ret = False
        try:
            self._packages.remove(package)
            if not self._packages:
                self._is_passed = True
            ret = True
        except ValueError:
            pass
        return ret
        pass

    def add_package(self, package):
        self._packages.append(package)
        pass

    pass
