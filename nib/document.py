from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import nib
from nib import yaml

class Document(dict):
    def __init__(self, path=None, uri=None, group=None, content=None, short=None, **kwargs):
        options = nib.instance().options

        defaults = options['defaults']
        for key in defaults:
            kwargs.setdefault(key, defaults[key])

        dict.__init__(self, **kwargs)
        self.path, self.extension = os.path.splitext(path)
        self.uri = uri
        self.group = group
        self.content = content
        self.short = short or content

    def __repr__(self):
        return '<Document({}, {}, {})>'.format(self.path, self.group,
                                               dict.__repr__(self))

    @classmethod
    def from_file(cls, path, options=None):
        metadata, sections = yaml.load(path, supplement=True)
        group = metadata.setdefault('group', None)

        if options:
            path = os.path.relpath(path, options['document_path'])

        content = sections.pop(0)
        short = content
        if len(sections):
            content += sections.pop(0)

        return Document(path=path,
                        content=content,
                        short=short,
                        **metadata
                        )

    def clone(self):
        new_doc = Document(path=self.path + self.extension,
                           uri=self.uri,
                           group=self.group,
                           content=self.content,
                           short=self.short,
                           **self)
        return new_doc
