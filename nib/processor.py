
preprocessors = []
postprocessors = []
document_processors = {}
resource_processors = {}
markup_processors = {}
render_processors = []

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

def render(cls):
    render_processors.append(cls)
    return cls

class Processor(object):
    def __init__(self, options):
        self.options = options

    def process(self, documents, resources):
        new_documents = []
        for document in documents:
            result = self.document(document)
            if result:
                new_documents.append(document)

        new_resources = []
        for resource in resources:
            result = self.resource(resource)
            if result:
                new_resources.append(resource)

        return new_documents, new_resources

    def document(self, document):
        return document

    def resource(self, resource):
        return resource
