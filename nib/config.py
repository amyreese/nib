from os import path

import nib

class Config(dict):
    def __init__(self):
        cwd = path.abspath(path.dirname(__file__))
        defaults = nib.yaml.load(path.join(cwd, 'config.defaults'))

        dict.__init__(self, defaults)

