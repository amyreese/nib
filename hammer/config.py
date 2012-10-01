from os import path

import hammer

class Config(dict):
    def __init__(self):
        cwd = path.abspath(path.dirname(__file__))
        defaults = hammer.yaml.load(path.join(cwd, 'config.defaults'))

        dict.__init__(self, defaults)

