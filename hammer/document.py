import os.path
from hammer import yaml

class Document(dict):
    def __init__(self, path=None, group=None, content=None, short=None, **kwargs):
        dict.__init__(self, **kwargs)
        self.path, self.extension = os.path.splitext(path)
        self.group = group
        self.content = content
        self.short = short or content

    def __repr__(self):
        return '<Document({}, {}, {})>'.format(self.path, self.group,
                                               dict.__repr__(self))

    @classmethod
    def from_file(cls, path):
        metadata, sections = yaml.load(path, supplement=True)
        group = metadata.setdefault('type', None)

        content = sections.pop(0)
        short = None
        if len(sections):
            short = content
            content += sections.pop(0)

        return Document(path=path,
                        group=group,
                        content=content,
                        short=short,
                        **metadata
                        )

