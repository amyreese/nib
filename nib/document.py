import os.path
from nib import yaml

class Document(dict):
    def __init__(self, path=None, uri=None, group=None, content=None, short=None, **kwargs):
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
            defaults = options['defaults']
            for key in defaults:
                metadata.setdefault(key, defaults[key])

        content = sections.pop(0)
        short = content
        if len(sections):
            content += sections.pop(0)

        return Document(path=path,
                        content=content,
                        short=short,
                        **metadata
                        )
