import os
from os import path

from hammer import Document
from hammer.processor import preprocessors, postprocessors, document_processors

class Build(object):
    def __init__(self, input_path, output_path, options):
        self.input_path = input_path
        self.output_path = output_path
        self.options = options

    def load_documents(self):
        documents = []

        cwd = os.getcwd()
        os.chdir(self.input_path)

        for root, dirs, files in os.walk('.'):
            for filename in files:
                filepath = path.normpath(path.join(root, filename))

                try:
                    print('Reading document {}'.format(filepath))
                    document = Document.from_file(filepath)
                    documents.append(document)

                except Exception as e:
                    print('Error while reading {}: {}'.format(filepath, e))

        os.chdir(cwd)

        return documents

    def process_documents(self, documents):
        # preprocess all documents
        for p in preprocessors:
            print('Running pre-processor {}'.format(p))
            documents = p(self.options).process(documents)

        # break documents into groups by type
        documents_by_group = {}
        for document in documents:
            group = document.group
            if group not in documents_by_group:
                documents_by_group[group] = []
            documents_by_group[group].append(document)

        # process documents by group
        documents = []
        for group in documents_by_group:
            group_documents = documents_by_group[group]

            if group in document_processors:
                processors = document_processors[group]
                for p in processors:
                    print('Running document processor {}'.format(p))
                    group_documents = p(self.options).process(group_documents)

            documents.extend(group_documents)

        # postprocess all documents
        for p in postprocessors:
            print('Running post-processor {}'.format(p))
            documents = p(self.options).process(documents)

        return documents


    def write_documents(self, documents):
        hierarchy = set([path.join(self.output_path, path.dirname(d.path)) for d in documents])
        hierarchy.discard(self.output_path)
        print('Creating output hierarchy: {}'.format(hierarchy))

        for dir in hierarchy:
            os.makedirs(dir, exist_ok=True)

        for document in documents:
            filepath = path.join(self.output_path, document.path)

            print('Writing document {}'.format(filepath))
            with open(filepath, 'w') as f:
                f.write(document.content)

    def run(self):
        documents = self.load_documents()
        documents = self.process_documents(documents)
        self.write_documents(documents)

