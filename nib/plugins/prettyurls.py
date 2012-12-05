from os import path

from nib import Resource, Processor, after

apache_redirects = b"""
RewriteCond %{DOCUMENT_ROOT}/$1/index.html -f
RewriteRule ^(.*)$ /$1/index.html [L]

RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^(.*)$ /$1.html [L]

RewriteCond %{DOCUMENT_ROOT}/$1/index.html -f
RewriteRule ^(.*)/$ /$1 [L,R]

RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^(.*)/$ /$1 [L,R]
"""

apache_redirects_base = b"""
RewriteEngine on
RewriteBase /
"""

@after
class PrettyURLProcessor(Processor):
    def process(self, documents, resources):
        for document in documents:
            filename = path.basename(document.uri)
            if filename == 'index.html':
                document.uri = path.dirname(document.path)
            elif document.extension == '.html':
                document.uri = document.path

        htaccess = None
        for resource in resources:
            if resource.path == '.htaccess':
                htaccess = resource

        if not htaccess:
            htaccess = Resource(path='.htaccess',
                                content=apache_redirects_base)
            resources.append(htaccess)

        htaccess.content += apache_redirects

        return documents, resources
