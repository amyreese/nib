import os
from os import path

from hammer import Document, Resource
from hammer.processor import preprocessors, postprocessors,\
    document_processors, resource_processors

class Build(object):
    def __init__(self, resource_path, document_path, output_path, options):
        self.document_path = document_path
        self.resource_path = resource_path
        self.output_path = output_path
        self.options = options

    def load_resources(self):
        resources = []

        for root, dirs, files in os.walk('.'):
            for filename in files:
                filepath = path.normpath(path.join(root, filename))

                try:
                    print('Reading resource {}'.format(filepath))
                    resource = Resource.from_file(filepath)
                    resources.append(resource)

                except Exception as e:
                    print('Error while reading {}: {}'.format(filepath, e))

        return resources

    def process_resources(self, resources):
        # break resources into groups by extension
        resources_by_group = {}
        for resource in resources:
            group = resource.extension
            if group not in resources_by_group:
                resources_by_group[group] = []
            resources_by_group[group].append(resource)

        # process resources by extension
        resources = []
        for group in resources_by_group:
            group_resources = resources_by_group[group]

            if group not in resource_processors:
                group = None

            if group in resource_processors:
                p = resource_processors[group]
                print('Running resource processor {}'.format(p))
                group_resources = p(self.options).process(group_resources)

            completed_resources = []
            chained_resources = []
            for resource in group_resources:
                if group is None or resource.extension == group:
                    completed_resources.append(resource)
                else:
                    chained_resources.append(resource)

            if len(chained_resources):
                chained_resources = self.process_resources(chained_resources)
                resources.extend(chained_resources)

            resources.extend(completed_resources)

        return resources

    def write_resources(self, resources):
        hierarchy = set([path.join(self.output_path, path.dirname(r.path)) for r in resources])
        hierarchy.discard(self.output_path)
        print('Creating output hierarchy: {}'.format(hierarchy))

        for dir in hierarchy:
            os.makedirs(dir, exist_ok=True)

        for resource in resources:
            filepath = path.join(self.output_path, resource.path)
            filepath += resource.extension

            print('Writing resource {}'.format(filepath))
            with open(filepath, 'w') as f:
                f.write(resource.content)

    def load_documents(self):
        documents = []

        for root, dirs, files in os.walk('.'):
            for filename in files:
                filepath = path.normpath(path.join(root, filename))

                try:
                    print('Reading document {}'.format(filepath))
                    document = Document.from_file(filepath)
                    documents.append(document)

                except Exception as e:
                    print('Error while reading {}: {}'.format(filepath, e))

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

            completed_documents = []
            chained_documents = []
            for document in group_documents:
                if group is None or document.group == group:
                    completed_documents.append(document)
                else:
                    chained_documents.append(document)

            if len(chained_documents):
                chained_documents = self.process_documents(chained_documents)
                documents.extend(chained_documents)

            documents.extend(completed_documents)

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
        cwd = os.getcwd()
        os.chdir(self.resource_path)

        resources = self.load_resources()
        resources = self.process_resources(resources)

        os.chdir(cwd)
        self.write_resources(resources)

        cwd = os.getcwd()
        os.chdir(self.document_path)

        documents = self.load_documents()
        documents = self.process_documents(documents)

        os.chdir(cwd)
        self.write_documents(documents)
