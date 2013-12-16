"""
tstream - tool which download a torrent file from the network and output its
contents to the standard output. tstream is reincarnation of
http://jordic.com/btcat/

Usage:
  slidelint TORRENT
  slidelint [options] TORRENT FILEID

Arguments:
  TORRENT  torrent URL or torrent file
  FILEID   id of of file to download

Options:
  -h --help              show this help message and exit
  -d <destination> --destination=<destination>  save torrent to <destination>
"""

from docopt import docopt

from torrents_streamer.torrent_streaming import TorrentLiveStreamer
from torrents_streamer.utils import data_context_hanler
from torrents_streamer.cmdline_streaming import ConstructStream, StatusNotifier


def cli():
    """
    Command line interface - parse user arg and print torrent files list
    or starts choose torrent file download
    """
    args = docopt(__doc__)
    torrent = args['TORRENT']
    fileid = args['FILEID'] and int(args['FILEID'])
    destination = args['--destination']
    with data_context_hanler(destination) as location_context:
        live_streamear = TorrentLiveStreamer(torrent, location_context)
        if fileid is not None:
            status_stream = StatusNotifier(live_streamear.torrent_handler.status)
            status_stream.start()
            stream = ConstructStream()
            return live_streamear.stream_file(fileid, stream)
        for i in live_streamear.get_torrent_files_list():
            print "%5s: %25s, %.2fMB" % (i[0], i[1], i[2]/1048576)
