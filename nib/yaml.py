from __future__ import absolute_import, division, print_function, unicode_literals

import re
import yaml

document_marker = re.compile(r'^---\s*$', re.M)

try:
    from yaml import CSafeLoader as SafeLoader
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeLoader, SafeDumper

def load(filename, supplement=False):
    with open(filename) as f:
        content = f.read()

    documents = document_marker.split(content, 2)

    try:
        data_document = documents.pop(0)
        data = yaml.load(data_document, Loader=SafeLoader)

    except yaml.YAMLError:
        if supplement:
            data = {}
            documents.insert(0, data_document)
        else:
            raise

    if supplement:
        return data, documents
    else:
        return data

def save(filename, data, supplement=None):
    output = yaml.dump(dict(data), Dumper=SafeDumper, indent=4,
                       default_flow_style=False)
    with open(filename, 'w') as f:
        f.write(output)

        if supplement:
            f.write('---\n')
            f.write(supplement)

