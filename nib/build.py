from __future__ import absolute_import, division, print_function, unicode_literals

import os
from os import path
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import nib
from nib import Document, Resource, Render
from nib.processor import preprocessors, postprocessors,\
    document_processors, resource_processors, markup_processors,\
    render_processors
import nib.plugins

class Build(object):
    def __init__(self, options):
        self.document_path = options['document_path']
        self.resource_path = options['resource_path']
        self.output_path = options['output_path']
        self.options = options

        nib.plugins.load(options)
        nib.instance(self)

    def load(self):
        documents = []

        for root, dirs, files in os.walk(self.document_path):
            for filename in files:
                filepath = path.join(root, filename)

                try:
                    print('Reading {}'.format(filepath))
                    document = Document.from_file(filepath, self.options)
                    documents.append(document)

                except Exception as e:
                    print('Error while reading {}: {}'.format(filepath, e))

        resources = []

        for root, dirs, files in os.walk(self.resource_path):
            for filename in files:
                filepath = path.join(root, filename)

                try:
                    print('Reading {}'.format(filepath))
                    resource = Resource.from_file(filepath, self.options)
                    resources.append(resource)

                except Exception as e:
                    print('Error while reading {}: {}'.format(filepath, e))

        return documents, resources

    def process_documents(self, documents, resources):
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
                    group_documents, resources = p(self.options).process(group_documents, resources)

            completed_documents = []
            chained_documents = []
            for document in group_documents:
                if group is '' or document.group == group:
                    completed_documents.append(document)
                else:
                    chained_documents.append(document)

            if len(chained_documents):
                chained_documents, resources = self.process_documents(chained_documents, resources)
                documents.extend(chained_documents)

            documents.extend(completed_documents)

        return documents, resources

    def process_resources(self, documents, resources):
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
                documents, group_resources = p(self.options).process(documents, group_resources)

            completed_resources = []
            chained_resources = []
            for resource in group_resources:
                if group is '' or resource.extension == group:
                    completed_resources.append(resource)
                else:
                    chained_resources.append(resource)

            if len(chained_resources):
                documents, chained_resources = self.process_resources(documents, chained_resources)
                resources.extend(chained_resources)

            resources.extend(completed_resources)

        return documents, resources

    def process(self, documents, resources):
        # preprocess everything
        for p in preprocessors:
            print('Running pre-processor {}'.format(p))
            documents, resources = p(self.options).process(documents, resources)

        documents, resources = self.process_documents(documents, resources)
        documents, resources = self.process_resources(documents, resources)

        # break documents into groups by extension
        documents_by_group = {}
        for document in documents:
            group = document.extension
            if group not in documents_by_group:
                documents_by_group[group] = []
            documents_by_group[group].append(document)

        # render markup for all documents
        documents = []
        for extension in documents_by_group:
            group_documents = documents_by_group[extension]

            if extension not in markup_processors:
                extension = ''

            if extension in markup_processors:
                processors = markup_processors[extension]
                for p in processors:
                    print('Running markup processor {}'.format(p))
                    group_documents, resources = p(self.options).process(group_documents, resources)

            documents.extend(group_documents)

        # set default document uris
        for document in documents:
            if document.uri is None:
                document.uri = document.path + document.extension

        # postprocess everything
        for p in postprocessors:
            print('Running post-processor {}'.format(p))
            documents, resources = p(self.options).process(documents, resources)

        # finalize document uris
        for document in documents:
            document.uri = urljoin(urljoin(self.options['site']['uri'],
                                           self.options['site']['root']),
                                   document.uri)
            if not document.get('link'):
                document['link'] = document.uri

        return documents, resources

    def write(self, documents, resources):
        render = Render(self.options, documents)

        for document in documents:
            print('Rendering content {}'.format(document.path))
            render.render_content(document)

        # pre-render final processing
        for p in render_processors:
            print('Running render processor {}'.format(p))
            documents, resources = p(self.options).process(documents, resources)

        for document in documents:
            filepath = path.join(self.output_path, document.path)
            filepath += document.extension

            print('Rendering document {}'.format(filepath))
            with open(filepath, 'w') as f:
                f.write(render.render_template(document))

        for resource in resources:
            filepath = path.join(self.output_path, resource.path)
            filepath += resource.extension

            print('Writing resource {}'.format(filepath))
            with open(filepath, 'wb') as f:
                f.write(resource.content)

    def create_output_hierarchy(self, documents, resources):
        hierarchy = set()

        for document in documents:
            dirname = path.dirname(document.path)
            hierarchy.add(path.join(self.output_path, dirname))

        for resource in resources:
            dirname = path.dirname(resource.path)
            hierarchy.add(path.join(self.output_path, dirname))

        print('Creating output hierarchy: {}'.format(hierarchy))

        for dir in hierarchy:
            try:
                os.makedirs(dir)
            except os.error:
                pass

    def run(self):
        documents, resources = self.load()
        documents, resources = self.process(documents, resources)

        self.create_output_hierarchy(documents, resources)
        self.write(documents, resources)
