from nib import Processor, render

@render
class PagesProcessor(Processor):
    def process(self, documents, resources):
        for document in documents:
            if 'pages' in document:
                if type(document['pages']) == str:
                    code = compile(document['pages'], '<string>', 'eval')
                    func = lambda page: eval(code)

                    subpages = list(filter(func, documents))
                    document['pages'] = subpages

        return documents, resources
