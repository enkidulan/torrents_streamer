Project Description
===================

I need a small python script that can efficiently read a file chunk by
chunk and serve it over http, the file itself will be continuously added
to(as it's been progressively downloaded) but we can provide the content
length.

Additional Project Description
==============================

So far I have something like

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File

root = Resource()
root.putChild("stream", File("/test/test.mkv"))

factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()

which works but in our case test.mkv is not a complete file,
I have the final content length and I'd like to continuing serving the
http stream and have a long timeout while to file is completed to
continue serving.

 i am using libtorrent python bindings to download a video sequentially
 and i'd like to stream it over http as it downloads

INSTALATION
===========

You can install this package into your python with:

::

    $ python setup.py install

or build buildout:

::

    $ python bootstrap.py
    $ bin/buildout

How to use script?
===================

::

  $ bin/static_file_server /path/to/video.mkv -p 9000
