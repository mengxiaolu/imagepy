import wx,os,sys
from skimage.io import imread

from urllib.request import urlopen
from io import BytesIO as StringIO

from imagepy.core import manager
from imagepy.core.engine import Free
from imagepy.core.util import fileio
from imagepy.core.manager import ReaderManager

class OpenFile(fileio.Reader):
    title = 'Open'

    def load(self):
        self.filt = [i for i in sorted(ReaderManager.gets('name'))]
        return True

class OpenUrl(Free):
    title = 'Open Url'
    para = {'url':'http://data.imagepy.org/testdata/yxdragon.jpg'}
    view = [('lab', None, 'Input the URL, eg. http://data.imagepy.org/testdata/yxdragon.jpg'),
            (str, 'url', 'Url:', '')]
    
    def run(self, para = None):
        try:
            fp, fn = os.path.split(para['url'])
            fn, fe = os.path.splitext(fn) 
            response = urlopen(para['url'])
            ## TODO: Fixme!
            stream = StringIO(response.read())
            img = imread(stream)
            self.app.show_img([img], fn)
        except Exception as e:
            print(self.app)
            self.app.show_txt('Open url failed!\tErrof:%s'%sys.exc_info()[1])
        
plgs = [OpenFile, OpenUrl]
    
if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()