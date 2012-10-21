from nib import Processor, after

@after
class IndexPages(Processor):
    def process(self, documents, resources):
        indexes = {}

        for document in documents:
            if 'index' in document:
                index = document['index']

                if index not in indexes:
                    indexes[index] = list()

                indexes[index].append(document)

        for document in documents:
            if document.path in indexes:
                document['pages'] = indexes[document.path]

        return documents, resources
