import importlib
import os
from os import path

cwd = path.abspath(path.dirname(__file__))
files = os.listdir(cwd)

for filename in files:
    name, ext = path.splitext(filename)
    if ext == '.py':
        importlib.import_module('hammer.plugins.' + name)
