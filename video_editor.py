import magic
import os
from datetime import datetime
from os import environ, path
import subprocess
from ranger.api.commands import Command


def time_s(time):
    times = [float(t) for t in time.split(':')]

    return float(times[0]) * 60 + float(times[1])


class clip_start(Command):
    """:cut_start sets the environment variable VID_START at the specified time parsed mm:ss:ms
    """

    def execute(self):

        if not self.arg(1):
            self.fm.notify('specify start time of format mm:ss:ms')

        try:
            environ['VID_START'] = str(time_s(self.arg(1)))
        except ValueError:
            self.fm.notify('specify start time of format mm:ss.ms')


class clip_end(Command):
    """:cut_end cuts the video clip from VID_START to the speciefied time in seconds and puts it in a dir name clip_cut in the current dir
    """

    def execute(self):
        if 'VID_START' not in environ:
            self.fm.notify('using the cut_start cmd specify start time of format mm:ss:ms')
            return

        if not self.arg(1):
            self.fm.notify('specify the end time of format mm:ss:ms')
            return

        if not path.isdir('./clips'):
            os.mkdir('clips')

        paths = [f.path for f in self.fm.thistab.get_selection()]
        if len(paths) > 1:
            self.fm.notify('Do not use this command with more than one selected file')
            return

        p = paths[0]
        self.fm
        ext = '.' + paths[0].split('.')[-1]

        if 'video' not in magic.from_file(p, mime=True):
            self.fm.notify('{} is not a video file and cannot be cut!'.format(p))
            return

        output_p = './clips/' + datetime.now().strftime('%Y%m%d_%H%M%S') + ext
        end_s = time_s(self.arg(1))

        # unfortunately output must be silenced (logelevel -8). ffmpeg will lock ranger up with its output
        # i could probably just write this to a file for troubleshooting
        subprocess.run(['ffmpeg',
                        '-loglevel', '-8',
                        '-ss', environ['VID_START'],
                        '-t', str(end_s - float(environ['VID_START'])),
                        '-i', p,
                        output_p])

        self.fm.notify('clip done writing')


class clip_join(Command):
    """:join_clips joins multiple clips into one clip.

    name(str): the name to output the joined clip to. defaults to the YYYYMMDDhhmmss.mp4 if not given
    """

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
