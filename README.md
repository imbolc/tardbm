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