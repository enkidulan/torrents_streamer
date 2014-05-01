Description
===========

torrents_streamer is a tool for streaming torrents content into
standard output.

How to use script?
===================

To stream torrents use tstream script:

::

    $ bin/tstream
    Usage:
      tstream TORRENT
      tstream [options] TORRENT FILEID

A TORRENT can be:
    * a link to torrent file('http://.../data.torrent')
    * torrent file path ('/home/.../data.torrent')
    * a magnet-link stored into file ('/home/.../file_with_magnet_link')

To get list of all files in the torrent:

::

    bin/tstream movie.torrent

To stream torrent file into stdout(into vlc sdtin):

::

    bin/tstream movie.torrent 0 | vlc -

In case if you want keep that movie on your disk after watch it use tstream with -d
option:

::

    bin/tstream -d ~/Movies movie.torrent 0 | vlc -

Requirements
============

You need to have installed python binding for libtorrent.
In Fedora you can install it with following command:

::

    # yum install rb_libtorrent-python

INSTALATION
===========

You can install this package into your python with:

::

    $ python setup.py install

or build buildout:

::

    $ python bootstrap.py
    $ bin/buildout
