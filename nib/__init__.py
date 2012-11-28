version = '0.4.1'

from os import path
cwd = path.abspath(path.dirname(__file__))

import nib.yaml as yaml
from nib.config import Config
from nib.document import Document
from nib.resource import Resource
from nib.render import Render, jinja
from nib.processor import Processor
from nib.processor import before, after, document, resource, markup
from nib.build import Build

import nib.plugins
