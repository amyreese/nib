import jinja2
from jinja2 import Environment, FileSystemLoader, Template
from os import path

class Render(object):
    def __init__(self, options, documents):
        self.options = options
        self.documents = documents
        self.loader = FileSystemLoader(path.abspath(options['template_path']))
        self.env = Environment(loader=self.loader)
        self.site = dict(options['site'], documents=documents)

        for document in documents:
            params = {
                'site': self.site,
                'page': document,
            }
            params.update(document)

            document.short = Template(document.short).render(**params)
            document.content = Template(document.content).render(**params)

    def render(self, document):
        if 'template' in document:
            template = self.env.get_template(document['template'])

            params = {
                'site': self.options['site'],
                'page': document,
                'content': document.content,
                'short': document.short,
            }
            params.update(document)

            return template.render(**params)

        else:
            return document.content
