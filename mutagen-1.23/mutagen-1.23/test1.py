from mutagen.mp4 import MP4
import sys

# sys.getdefaultencoding()

cyg_path = "/cygdrive/c/Users/daniel/Dropbox/iTunes/iTunes Media/Music/Jonny Greenwood/Bodysong/Convergence.m4a"
win_path = "C:\Users\daniel\Dropbox\iTunes\iTunes Media\Music\Jonny Greenwood\Bodysong\Convergence.m4a"
audio = MP4(win_path)
audio.pprint()
