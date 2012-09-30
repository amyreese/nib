import re
import yaml

document_marker = re.compile(r'^---\s*$', re.M)

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

def load(filename, supplement=False):
    with open(filename) as f:
        content = f.read()

    documents = document_marker.split(content, 2)
    data = yaml.load(documents.pop(0), Loader=SafeLoader)

    if supplement:
        return data, documents
    else:
        return data

