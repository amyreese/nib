import os.path

class Resource(object):
    def __init__(self, path=None, extension=None, content=None):
        self.path = path
        self.extension = extension
        self.content = content

    @classmethod
    def from_file(cls, path):
        name, extension = os.path.splitext(path)
        if extension == '':
            extension = None

        with open(path) as f:
            content = f.read()

        return Resource(path=name,
                        extension=extension,
                        content=content,
                        )
