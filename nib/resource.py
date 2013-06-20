from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

class Resource(object):
    def __init__(self, path=None, content=None):
        self.path, self.extension = os.path.splitext(path)
        self.content = content

    @classmethod
    def from_file(cls, path, options=None):
        with open(path, 'rb') as f:
            content = f.read()

        if options:
            path = os.path.relpath(path, options['resource_path'])

        return Resource(path=path,
                        content=content,
                        )
