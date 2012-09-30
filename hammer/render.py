import jinja2
from jinja2 import Environment, FileSystemLoader
from os import path

class Render(object):
    def __init__(self, options, documents):
        self.options = options
        self.documents = documents
        self.loader = FileSystemLoader(path.abspath(options['template_path']))
        self.env = Environment(loader=self.loader)

    def render(self, document):
        template = self.env.get_template(document['template'])
        return template.render(site=self.options['site'],
                               documents=self.documents,
                               document=document,
                               content=document.content,
                               **document)
