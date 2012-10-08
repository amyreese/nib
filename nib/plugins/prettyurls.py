from os import path

from nib import Document, Processor, after

apache_redirects = """\
RewriteEngine on
RewriteBase /

RewriteCond %{DOCUMENT_ROOT}/$1/index.html -f
RewriteRule ^(.*)$ /$1/index.html [L]

RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^(.*)$ /$1.html [L]

RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^(.*)/$ /$1 [R]
"""

@after
class PrettyURLProcessor(Processor):
    def process_all(self, documents):
        for document in documents:
            filename = path.basename(document.uri)
            if filename == 'index.html':
                document.uri = path.dirname(document.path)
            elif document.extension == '.html':
                document.uri = document.path

        htaccess = Document(path='.htaccess',
                            uri='.htaccess',
                            content=apache_redirects)
        if 'apache_htaccess_rules' in self.options:
            document.content += self.aptions['apache_htaccess_rules']
        documents.append(htaccess)

        return documents
