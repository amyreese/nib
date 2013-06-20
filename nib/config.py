from __future__ import absolute_import, division, print_function, unicode_literals

from os import path
import sys

import nib

default_config = path.join(nib.cwd, 'defaults.nib')

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
        values = nib.yaml.load(default_config)

        if filename is not None:
            if path.isfile(filename):
                overrides = nib.yaml.load(filename)
                merge(values, overrides)
            else:
                sys.stderr.write('Warning: no site config found at "{}"\n'.format(filename))

        dict.__init__(self, values)
