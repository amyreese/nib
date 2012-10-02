import importlib
import os
from os import path

cwd = path.abspath(path.dirname(__file__))
files = os.listdir(cwd)

def load(options):
    load_plugins = options['load_plugins']
    ignore_plugins = options['ignore_plugins']

    for filename in files:
        name, ext = path.splitext(filename)

        if ext == '.py':
            if name in ignore_plugins:
                continue

            if name in load_plugins or '*' in load_plugins:
                importlib.import_module('nib.plugins.' + name)
