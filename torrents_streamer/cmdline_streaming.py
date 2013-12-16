"""
Classes for streaming data into console stdout and displaying download
progress.
"""
import sys
import time
import threading


class ConstructStream():
    """ helper class that create output stream to write data,
    use it in case you want to stream into some different than pipes"""
    def __init__(self, stream_cmd=None):
        self.stream = sys.stdout

    def write(self, data):
        """ write data to stream"""
        self.stream.write(data)


class StatusNotifier(threading.Thread):
    """ Class for outputting downloading status"""
    state_str = ['queued', 'checking', 'downloading metadata',
                 'downloading', 'finished', 'seeding', 'allocating',
                 'checking fastresume']
    out = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %s'

    def __init__(self, status):
        super(StatusNotifier, self).__init__()
        self.status = status
        # self.tfile.path = ''

    def run(self):
        while True:
            status = self.status()
            output = self.out % (
                status.progress * 100,
                status.download_rate / 1000,
                status.upload_rate / 1000,
                status.num_peers,
                self.state_str[status.state],
                'file')# self.tfile.path)
            # in case of using pipes the only way to display status
            # information is to use stderr
            sys.stderr.write(output)
            sys.stderr.flush()
            time.sleep(0.5)
