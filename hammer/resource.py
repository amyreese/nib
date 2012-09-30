import os.path

class Resource(object):
    def __init__(self, path=None, content=None):
        self.path, self.extension = os.path.splitext(path)
        self.content = content

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            content = f.read()

        return Resource(path=path,
                        content=content,
                        )
