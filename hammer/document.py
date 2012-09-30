import os.path
from hammer import yaml

class Document(dict):
    def __init__(self, path=None, group=None, content=None, **kwargs):
        dict.__init__(self, **kwargs)
        self.path, self.extension = os.path.splitext(path)
        self.group = group
        self.content = content

    def __repr__(self):
        return '<Document({}, {}, {})>'.format(self.path, self.group,
                                               dict.__repr__(self))

    @classmethod
    def from_file(cls, path):
        metadata, content = yaml.load(path, supplement=True)
        group = metadata.setdefault('type', None)

        return Document(path=path,
                        group=group,
                        content=content,
                        **metadata
                        )

