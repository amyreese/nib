
preprocessors = []
postprocessors = []
document_processors = {}
resource_processors = {}
markup_processors = {}

def resource(extensions):
    if type(extensions) != list:
        extensions = [extensions]

    def decorator(cls):
        for extension in extensions:
            resource_processors[extension] = cls
        return cls
    return decorator

def before(cls):
    preprocessors.append(cls)
    return cls

def document(document_type):
    def decorator(cls):
        if document_type not in document_processors:
            document_processors[document_type] = []
        document_processors[document_type].append(cls)
        return cls
    return decorator

def after(cls):
    postprocessors.append(cls)
    return cls

def markup(extensions):
    if type(extensions) != list:
        extensions = [extensions]

    def decorator(cls):
        for extension in extensions:
            if extension not in markup_processors:
                markup_processors[extension] = []
            markup_processors[extension].append(cls)
    return decorator

class Processor(object):
    def __init__(self, options):
        self.options = options

    def process_all(self, documents):
        new_documents = []
        for document in documents:
            result = self.process(document)
            if result:
                new_documents.append(document)

        return new_documents

    def process(self, document):
        return document
