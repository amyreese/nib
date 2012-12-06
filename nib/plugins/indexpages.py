from nib import Document, Processor, after

@after
class IndexPages(Processor):
    def process(self, documents, resources):
        indexes = {}

        for document in documents:
            if 'parent' in document:
                index = document['parent']

                if index not in indexes:
                    indexes[index] = list()

                indexes[index].append(document)

        for document in documents:
            if document.path in indexes:
                document['pages'] = indexes[document.path]
                if document['template'] == self.options['defaults']['template']:
                    document['template'] = 'list.html'
                del indexes[document.path]

        for index_path in indexes:
            title = ' '.join(index_path.split('/')).title()
            document = Document(path=index_path,
                                uri=index_path,
                                title=title,
                                content='',
                                short='',
                                template='list.html',
                                pages=indexes[index_path])
            print(document.uri)
            documents.append(document)

        return documents, resources
