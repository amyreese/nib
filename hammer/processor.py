
preprocessors = []
postprocessors = []
document_processors = {}

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

class Processor(object):
    def __init__(self, options):
        self.options = options

    def process(self, documents):
        return documents

