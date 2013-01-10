version = '0.4.13'

from os import path
cwd = path.abspath(path.dirname(__file__))

try:
    import nib.yaml as yaml
    from nib.config import Config
    from nib.document import Document
    from nib.resource import Resource
    from nib.render import Render, jinja
    from nib.processor import Processor
    from nib.processor import before, after, document, resource, markup, render
    from nib.build import Build

    import nib.plugins

except ImportError:
    # let's hope this only happens in setup.py until I find a better way
    pass
