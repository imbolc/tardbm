'''
tardbm
======
Dict-style DBM based on tarball.

    >>> import tardbm
    >>> db = tardbm.open('./test.tar.gz')
    >>> db['foo'] = 'bar'
    >>> db['foo']
    'bar'
    >>> del db['foo']
    >>> len(db)
    0
'''
import os
import tarfile
from UserDict import DictMixin
from StringIO import StringIO


__version__ = '1.0.0'


class TarDBM(DictMixin):
    def __init__(self, filename):
        self.filename = filename

    def __getitem__(self, key):
        try:
            with tarfile.open(self.filename, 'r') as tar:
                return tar.extractfile(key).read()
        except IOError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if not isinstance(value, str):
            raise ValueError('%s value must be a string')
        if key in self:
            del self[key]
        tarinfo = tarfile.TarInfo(key)
        tarinfo.size = len(value)
        with tarfile.open(self.filename, 'a') as tar:
            tar.addfile(tarinfo, StringIO(value))

    def __delitem__(self, key):
        code = os.system('tar --delete -f %s %s 2>/dev/null' % (
            self.filename, key))
        if code == 512:
            raise KeyError(key)
        if code:
            raise OSError('tar delete failed with code: %s' % code)

    def keys(self):
        try:
            with tarfile.open(self.filename, 'r') as tar:
                return tar.getnames()
        except IOError:
            return []


def open(filename):
    return TarDBM(filename)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
