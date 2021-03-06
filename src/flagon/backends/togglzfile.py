import warnings

warnings.warn('TogglzFileBackend is not safe for multi-write environments')

from flagon import errors
from flagon.backends import Backend

try:
    from configobj import ConfigObj
except ImportError, ie:
    print "You must install configobj for TogglzFileBackend"
    print "http://www.voidspace.org.uk/python/configobj.html#installing"
    raise ie


class TogglzFileBackend(Backend):
    """
    Support for using Togglz's FileBasedStateRepository
    (see http://www.togglz.org/documentation/repositories.html).

    Currently only on/off functionality is supported.
    """

    def __init__(self, filename):
        """
        :param filename: File to read/write.
        :type filename: str
        :rtpe: TogglzFileBackend
        """
        self._filename = filename
        self._read_file()

    def _read_file(self):
        """
        Reads a file into memory.
        """
        self._store = ConfigObj(self._filename)

    def _write_file(self):
        """
        Dumps the data in memory to a file.
        """
        self._store.write()

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        return name.upper() in self._store.keys()

    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        name = name.upper()
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        if self._store[name] == 'true':
            return True
        return False

    def _turn(self, name, value):
        """
        Turns a feature to value.

        :param name: name of the feature.
        :param value: Value to turn name to ("true"/"false").
        :raises: UnknownFeatureError
        """
        name = name.upper()
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._store[name] = value
        self._write_file()

    turn_on = lambda s, name: _turn(s, name, 'true')
    turn_off = lambda s, name: _turn(s, name, 'false')
