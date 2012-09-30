import os
from os import path
import sys

cwd = path.abspath(path.dirname(__file__))
sys.path.insert(0, cwd)
sys.path.insert(0, path.join(cwd, 'lib'))
sys.path.insert(0, path.join(cwd, 'lib/sh'))

import hammer

options = hammer.yaml.load(path.join(cwd, 'config.defaults'))
if path.exists('config.local'):
    options.update(hammer.yaml.load('config.local'))

hammer.Build(options).run()
