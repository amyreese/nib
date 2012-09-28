import os
from os import path
import sys

cwd = path.abspath(path.dirname(__file__))
sys.path.insert(0, cwd)
sys.path.insert(0, path.join(cwd, 'lib'))

