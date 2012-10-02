import os
from os import path

from nib import Document, Resource, Render
from nib.processor import preprocessors, postprocessors,\
    document_processors, resource_processors, markup_processors
import nib.plugins

class Build(object):
    def __init__(self, options):
        self.document_path = options['document_path']
        self.resource_path = options['resource_path']
        self.output_path = options['output_path']
        self.options = options

        nib.plugins.load(options)

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
                group = ''

            if group in resource_processors:
                p = resource_processors[group]
                print('Running resource processor {}'.format(p))
                group_resources = p(self.options).process_all(group_resources)

            completed_resources = []
            chained_resources = []
            for resource in group_resources:
                if group is '' or resource.extension == group:
                    completed_resources.append(resource)
                else:
                    chained_resources.append(resource)

            if len(chained_resources):
                chained_resources = self.process_resources(chained_resources)
                resources.extend(chained_resources)

            resources.extend(completed_resources)

        return resources

    def write_resources(self, resources):
        for resource in resources:
            filepath = path.join(self.output_path,
                                 self.options['resource_output_path_prefix'],
                                 resource.path)
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
                    document = Document.from_file(filepath,
                                                  self.options['defaults'])
                    documents.append(document)

                except Exception as e:
                    print('Error while reading {}: {}'.format(filepath, e))

        return documents

    def process_documents(self, documents):
        # preprocess all documents
        for p in preprocessors:
            print('Running pre-processor {}'.format(p))
            documents = p(self.options).process_all(documents)

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
                    group_documents = p(self.options).process_all(group_documents)

            completed_documents = []
            chained_documents = []
            for document in group_documents:
                if group is '' or document.group == group:
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
            documents = p(self.options).process_all(documents)

        return documents


    def write_documents(self, documents):
        final_documents = []
        for document in documents:
            extension = document.extension
            if extension not in markup_processors:
                extension = ''

            if extension in markup_processors:
                processors = markup_processors[extension]
                for p in processors:
                    print('Running markup processor for {}: {}'.format(document.path, p))
                    document = p(self.options).process(document)

            final_documents.append(document)

        render = Render(self.options, final_documents)

        for document in final_documents:
            filepath = path.join(self.output_path, document.path)
            filepath += document.extension

            print('Rendering document {}'.format(filepath))
            with open(filepath, 'w') as f:
                f.write(render.render(document))

    def create_output_hierarchy(self, resources, documents):
        hierarchy = set()

        for resource in resources:
            dirname = path.dirname(resource.path)
            hierarchy.add(path.join(self.output_path,
                          self.options['resource_output_path_prefix'],
                          dirname))

        for document in documents:
            dirname = path.dirname(document.path)
            hierarchy.add(path.join(self.output_path, dirname))

        print('Creating output hierarchy: {}'.format(hierarchy))

        for dir in hierarchy:
            os.makedirs(dir, exist_ok=True)

    def run(self):
        cwd = os.getcwd()
        os.chdir(self.resource_path)
        resources = self.load_resources()
        resources = self.process_resources(resources)
        os.chdir(cwd)

        cwd = os.getcwd()
        os.chdir(self.document_path)
        documents = self.load_documents()
        documents = self.process_documents(documents)
        os.chdir(cwd)

        self.create_output_hierarchy(resources, documents)
        self.write_resources(resources)
        self.write_documents(documents)
