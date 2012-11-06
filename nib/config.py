from os import path

import nib

def merge(dest, source):
    """In-place, recursive merge of two dictionaries."""
    for key in source:
        if key in dest:
            if isinstance(dest[key], dict) and isinstance(source[key], dict):
                merge(dest[key], source[key])
                continue

        dest[key] = source[key]

    return dest

class Config(dict):
    def __init__(self, filename=None):
        cwd = path.abspath(path.dirname(__file__))
        values = nib.yaml.load(path.join(cwd, 'config.defaults'))

        if filename is None and path.isfile('config.nib'):
            filename = 'config.nib'

        if filename is not None:
            overrides = nib.yaml.load(filename)
            merge(values, overrides)

        dict.__init__(self, values)
