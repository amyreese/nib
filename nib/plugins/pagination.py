from __future__ import absolute_import, division, print_function, unicode_literals

from os import path
try:
    from urllib.parse import urlparse, urlunparse, ParseResult
except ImportError:
    from urlparse import urlparse, urlunparse, ParseResult

from nib import Processor, after, Document

@after
class PaginationProcessor(Processor):
    def process(self, documents, resources):
        new_documents = list()
        for document in documents:
            if document.get('paginate', False) and 'pages' in document:
                if isinstance(document['pages'], list):
                    per_page = document['per_page']
                    sort_by = document['sort_by']
                    reverse = document['reverse']

                    unknowns = filter(lambda d: sort_by not in d,
                                      document['pages'])
                    knowns = filter(lambda d: sort_by in d,
                                    document['pages'])

                    pages = sorted(knowns,
                                   key=lambda d: d[sort_by],
                                   reverse=reverse)
                    pages.extend(unknowns)

                    document['pages'] = pages[:per_page]
                    pages = pages[per_page:]

                    last = document
                    counter = 1
                    while len(pages):
                        doc = document.clone()
                        doc.path += str(counter)

                        p, e = path.splitext(doc.uri)
                        doc.uri = p + str(counter) + e

                        doc['pages'] = pages[:per_page]
                        pages = pages[per_page:]

                        last['next'] = doc
                        doc['previous'] = last
                        doc.pop('next', None)

                        new_documents.append(doc)

                        last = doc
                        counter += 1

        documents.extend(new_documents)

        return documents, resources

