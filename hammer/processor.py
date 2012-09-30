
preprocessors = []
postprocessors = []
document_processors = {}
resource_processors = {}

def before(cls):
    preprocessors.append(cls)
    return cls

def after(cls):
    postprocessors.append(cls)
    return cls

def document(document_type):
    def decorator(cls):
        if document_type not in document_processors:
            document_processors[document_type] = []
        document_processors[document_type].append(cls)
        return cls
    return decorator

def resource(extension):
    def decorator(cls):
        resource_processors[extension] = cls
        return cls
    return decorator

class Processor(object):
    def __init__(self, options):
        self.options = options

    def process_all(self, documents):
        return [self.process(d) for d in documents]

    def process(self, document):
        return document
