"""
This module contain classes for getting torrent info(like list of torrents
files) and sequential torrent download and streaming.

"""
import os
import time
import requests
import libtorrent as lt


class BufferedPiecesGetter():
    """ Gets pieces in sequential order, caching non in sequence pieces"""
    cache = {}

    def __init__(self, ses, torrent_handler, tfile, st_stream, timeout=0.1):
        self.ses = ses
        self.torrent_handler = torrent_handler
        self.tfile = tfile
        self.timeout = timeout
        self.st_stream = st_stream

    def __call__(self, i):
        if i in self.cache:
            return self.cache.pop(i)
        # waiting for piece to be downloaded
        while True:
            status = self.torrent_handler.status()
            self.st_stream.update(status, self.tfile)
            if status.pieces[i] is True or not len(status.pieces):
                break
            time.sleep(self.timeout)
        # reading target piece and return it
        self.torrent_handler.read_piece(i)  # triggering read_piece_alert
        while True:
            self.st_stream.update(status, self.tfile)
            piece = self.ses.pop_alert()  # reading triggered piece
            if isinstance(piece, lt.read_piece_alert):
                if piece.piece == i:
                    return piece.buffer
                cache[piece.piece] = piece.buffer
                break
            time.sleep(self.timeout)


def construct_handler(ses, torrent, destination):
    """ helper for handling magnet link, http links and torrent files"""
    tinfo = None
    params = {
        'save_path': destination,
        'storage_mode': lt.storage_mode_t(2),
        'auto_managed': True,
    }
    # if case if ULR was provided download it to file
    # TODO: add nice REGXP URL validator, the 'http' can be a folder name
    if torrent.startswith('http'):
        torrent_body = requests.get(torrent)
        torrent = os.path.join(location_context, 'torrent_file')
        tmp_torrent = torrent+'.tmp'
        with open(tmp_torrent, 'wb') as dist:
            dist.write(torrent_body.text.encode('utf-8'))
        os.rename(tmp_torrent, torrent)

    # check if file contain magnet link
    # XXX: shitty magnet support from file
    torrent_data = open(torrent).read().strip(" \n\t")
    if torrent_data.startswith("magnet:"):
        torrent_handler = lt.add_magnet_uri(ses, torrent_data, params)
    else:
        tinfo = lt.torrent_info(torrent)
        params['ti'] = tinfo
        torrent_handler = ses.add_torrent(params)
    # waiting for metadata to be downloaded
    while (not torrent_handler.has_metadata()):
        time.sleep(0.1)
    return torrent_handler


class TorrentLiveStreamer():
    """ Class that streams torrent in sequential order to given stream"""
    def __init__(self, torrent, destination=None):
        self.torrent = torrent
        self.destination = destination
        self.ses = lt.session()
        self.ses.listen_on(6881, 6891)
        # set notification only for storage events for getting data pieces
        self.ses.set_alert_mask(lt.alert.category_t.storage_notification)
        self._torrent_handler = None
        self._tinfo = None

    @property
    def torrent_handler(self):
        if self._torrent_handler is not None:
            return self._torrent_handler
        return construct_handler(self.ses, self.torrent, self.destination)

    @property
    def tinfo(self):
        if self._tinfo is not None:
            return self._tinfo
        return self.torrent_handler.get_torrent_info()

    def get_torrent_files_list(self):
        """ return all list of all files in torrent"""
        for num, tfile in enumerate(self.tinfo.files()):
            yield num, tfile.path, tfile.size, tfile.offset

    def stream_file(self, fileid, stream, status_stream):
        """ actual file streamer """
        tfile = self.tinfo.files()[fileid]
        piece_length = self.tinfo.piece_length()
        piece_start, piece_start_skip_bytes = \
            divmod(tfile.offset, piece_length)
        piece_end, piece_end_take_bytes = \
            divmod(tfile.offset + tfile.size, piece_length)
        # allowing downloading only desired file pieces
        for piece_num in xrange(self.tinfo.num_pieces()):
            self.torrent_handler.piece_priority(piece_num, 0)
        for piece_num in xrange(piece_start, piece_end + 1):
            self.torrent_handler.piece_priority(piece_num, 7)
        # set sequential download mod
        self.torrent_handler.set_sequential_download(True)
        # downloading pieces
        getpiece = BufferedPiecesGetter(
            self.ses, self.torrent_handler, tfile, status_stream)
        for piece_num in xrange(piece_start, piece_end + 1):
            status_stream.update(self.torrent_handler.status(), tfile)
            buf = getpiece(piece_num)
            if piece_num == piece_start:
                buf = buf[piece_start_skip_bytes:]
            if piece_num == piece_end:
                buf = buf[:piece_end_take_bytes]
            stream.write(buf)
        status_stream.update(self.torrent_handler.status(), tfile)

    def __del__(self):
        self.ses.remove_torrent(self.torrent_handler)
