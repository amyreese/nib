from __future__ import absolute_import, division, print_function, unicode_literals

from os import path
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from nib import Processor, render

@render
class BreadcrumbProcessor(Processor):
    def process(self, documents, resources):
        uris = {urlparse(d.uri).path.strip('/'): d for d in documents}

        for doc in documents:
            if 'nocrumbs' in doc:
                continue

            breadcrumbs = []
            segments = urlparse(doc.uri).path.strip('/').split('/')
            uri = ''

            for segment in segments:
                uri = path.join(uri, segment).strip('/')
                if uri in uris:
                    page = uris[uri]
                    if 'title' in page and page['title']:
                        breadcrumbs.append(uris[uri])

            doc['breadcrumbs'] = breadcrumbs

        return documents, resources
