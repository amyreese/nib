from hammer import yaml

class Document(dict):
    def __init__(self, path=None, type=None, content=None, **kwargs):
        dict.__init__(self, **kwargs)
        self.path = path
        self.type = type
        self.content = content

    def __repr__(self):
        return '<Document({}, {}, {})>'.format(self.path, self.type,
                                               dict.__repr__(self))

    @classmethod
    def from_file(cls, path):
        metadata, content = yaml.load(path, supplement=True)
        t = metadata.setdefault('type', None)

        return Document(path=path,
                        type=t,
                        content=content,
                        **metadata
                        )

