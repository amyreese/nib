import jinja2
from jinja2 import Environment, FileSystemLoader, Template
from os import path
import time

jinja_filters = {}

def jinja(name):
    def decorator(f):
        jinja_filters[name] = f
        return f
    return decorator

class Render(object):
    def __init__(self, options, documents):
        self.options = options
        self.documents = documents

        self.loader = FileSystemLoader(path.abspath(options['template_path']))
        self.env = Environment(loader=self.loader)
        for name in jinja_filters:
            self.env.filters[name] = jinja_filters[name]

        self.site = dict(options['site'], documents=documents)
        self.now = time.time()

    def render_content(self, document):
        params = {
            'now': self.now,
            'site': self.site,
            'page': document,
        }
        params.update(document)

        document.short = self.env.from_string(document.short).render(**params)
        document.content = self.env.from_string(document.content).render(**params)

    def render_template(self, document):
        if 'template' in document:
            template = self.env.get_template(document['template'])

            params = {
                'now': self.now,
                'site': self.options['site'],
                'page': document,
                'content': document.content,
                'short': document.short,
            }
            params.update(document)

            return template.render(**params)

        else:
            return document.content
