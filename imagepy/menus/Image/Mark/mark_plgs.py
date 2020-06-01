from imagepy.core.engine import Simple, Free
from sciapp import Source
from sciapp.object.shape import default_style
from sciapp.util import mark2shp
import json

class Clear(Simple):
    title = 'Clear Mark'
    note = ['all']

    def run(self, ips, imgs, para = None):
        ips.mark = None

class Save(Simple):
    title = 'Save Mark'
    note = ['all']
    para={'path':''}

    def load(self, ips):
        if ips.mark is None:
            return self.app.alert('no mark found!')
        return True

    def show(self):
        self.para['path'] = self.app.getpath('Save..', ['mrk'], 'save')
        return not self.para['path'] is None

    def run(self, ips, imgs, para = None):
        with open(para['path'], 'w') as f:
            f.write(json.dumps(ips.mark.to_mark()))

class Open(Simple):
    title = 'Open Mark'
    note = ['all']
    para = {'path':''}

    def show(self):
        self.para['path'] = self.app.getpath('Open..', ['mrk'], 'open')
        return not self.para['path'] is None

    def run(self, ips, imgs, para = None):
        with open(para['path']) as f:
            ips.mark = mark2shp(json.loads(f.read()))

class Setting(Free):
    title = 'Mark Setting'
    para = default_style.copy()
    view = [('color', 'color', 'line', 'color'),
            ('color', 'fcolor', 'face', 'color'),
            ('color', 'tcolor', 'text', 'color'),
            (int, 'lw', (1,10), 0, 'width', 'pix'),
            (int, 'size', (1,30), 0, 'text', 'size'),
            (bool, 'fill', 'solid fill')]

    def run(self, para=None):
        for i in para: default_style[i] = para[i]
        Source.manager('config').add('mark_style', para)

plgs = [Open, Save, Clear, '-', Setting]