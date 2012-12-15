from os import path

from nib import Processor, render

@render
class BreadcrumbProcessor(Processor):
    def process(self, documents, resources):
        uris = {d.uri.strip('/'): d for d in documents}

        for doc in documents:
            if 'nocrumbs' in doc:
                continue

            breadcrumbs = []
            segments = doc.uri.strip('/').split('/')
            uri = ''

            for segment in segments:
                uri = path.join(uri, segment).strip('/')
                if uri in uris:
                    page = uris[uri]
                    if 'title' in page and page['title']:
                        breadcrumbs.append(uris[uri])

            doc['breadcrumbs'] = breadcrumbs

        return documents, resources
