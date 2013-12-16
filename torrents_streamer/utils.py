"""
just bunch of helpful functions
"""
import tempdir
from contextlib import contextmanager


@contextmanager
def data_context_hanler(location_context=None):
    """
    creates location context for libtorrent

    >>> with prepare_torrent() as dir:
    ...     print dir.startswith('/tmp/')
    True

    >>> with prepare_torrent('hello') as dir:
    ...    print dir
    hello
    """
    if location_context:
        # in case if we want save torrent to some location
        yield location_context
    else:
        # in case we want only to stream torrent without keeping it
        with tempdir.TempDir() as location_context:
            yield location_context
