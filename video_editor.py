import magic
import os
from datetime import datetime
from os import environ, path
import subprocess
from ranger.api.commands import Command


def time_s(time):
    times = [float(t) for t in time.split(':')]
    if len(times) == 1:
        times = [0.00] + times

    return float(times[0]) * 60 + times[1]


def set_start(start_time):
    environ['VID_START'] = str(time_s(start_time))


def set_end(end_time):
    environ['VID_END'] = str(time_s(end_time))


def end_cut(p):
    if 'VID_START' not in environ:
        raise ValueError('using the cut_start cmd specify start time of format mm:ss:ms')

    if 'VID_END' not in environ:
        raise ValueError('using the cut_start cmd specify start time of format mm:ss:ms')

    if 'video' not in magic.from_file(p, mime=True):
        raise ValueError('{} is not a video file and cannot be cut!'.format(p))

    end_s = time_s(environ['VID_END'])

    if not path.isdir('./clips'):
        os.mkdir('clips')

    ext = '.' + p.split('.')[-1]

    output_p = './clips/' + datetime.now().strftime('%Y%m%d_%H%M%S') + ext

    # unfortunately output must be silenced (logelevel -8). ffmpeg will lock ranger up with its output
    # i could probably just write this to a file for troubleshooting
    subprocess.run(['ffmpeg',
                    '-loglevel', '-8',
                    '-ss', environ['VID_START'],
                    '-t', str(end_s - float(environ['VID_START'])),
                    '-i', p,
                    output_p])

    return 'clip done writing'


class clip_start(Command):
    """:cut_start sets the environment variable VID_START at the specified time parsed mm:ss:ms
    """

    def execute(self):
        if not self.arg(1):
            self.fm.notify('specify start time of format mm:ss:ms')
            return

        try:
            set_start(self.arg(1))
        except ValueError:
            self.fm.notify('specify start time of format mm:ss.ms')


class clip_end(Command):
    """:cut_end cuts the video clip from VID_START to the speciefied time in seconds and puts it in a dir name clip_cut in the current dir
    """

    def execute(self):
        paths = [f.path for f in self.fm.thistab.get_selection()]
        if len(paths) > 1:
            self.fm.notify('Do not use this command with more than one selected file')
            return

        p = paths[0]

        self.fm.notify('starting to cut clip')
        set_end(self.arg(1))

        try:
            self.fm.notify(end_cut(p))
        except Exception as e:
            self.fm.notify(str(e))


class clip_cut(Command):
    """:clip_cut cuts the video from arg[0] to arg[1]
    """

    def execute(self):
        if not self.arg(1):
            self.fm.notify('specify start time of format mm:ss:ms')
            return

        if not self.arg(2):
            self.fm.notify('specify end time of format mm:ss:ms')
            return

        try:
            set_start(self.arg(1))
        except ValueError:
            self.fm.notify('specify start time of format mm:ss.ms')

        paths = [f.path for f in self.fm.thistab.get_selection()]
        if len(paths) > 1:
            self.fm.notify('Do not use this command with more than one selected file')
            return

        p = paths[0]

        self.fm.notify('starting to cut clip')
        set_end(self.arg(2))

        try:
            self.fm.notify(end_cut(p))
        except Exception as e:
            self.fm.notify(str(e))


class clip_join(Command):

    def execute(self):
        if not self.arg(1):
            self.fm.notify('pass a filename with a video mimetype extension')
            return

        with open('/tmp/tmpfnames.txt', 'w+') as tempfile:
            for f in self.fm.thistab.get_selection():
                tempfile.write('file \'{}\'\n'.format(f.path))

        # unfortunately output must be silenced (logelevel -8). ffmpeg will lock ranger up with its output
        # i could probably just write this to a file for troubleshooting
        subprocess.run(['ffmpeg',
                        '-loglevel', '-8',
                        '-f', 'concat',
                        '-safe', '0',
                        '-i', '/tmp/tmpfnames.txt',
                        '-c', 'copy',
                        self.arg(1)])

        self.fm.notify('joined clip done writing')
