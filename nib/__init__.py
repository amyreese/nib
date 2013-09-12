from __future__ import absolute_import, division, print_function, unicode_literals

version = '0.5.5'

from os import path
cwd = path.abspath(path.dirname(__file__))

_instance = None
def instance(new=None):
    global _instance
    if new:
        _instance = new
    return _instance

from . import yaml
from .config import Config
from .document import Document
from .resource import Resource
from .render import Render, jinja
from .processor import Processor
from .processor import before, after, document, resource, markup, render
from .build import Build

from . import plugins

