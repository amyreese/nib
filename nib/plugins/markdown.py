import markdown
from nib import Processor, markup

@markup(['.md', '.mkdn'])
class MarkdownProcessor(Processor):
    def __init__(self, options):
        self.options = options
        self.markdown = markdown.Markdown(output_format='html5')

    def document(self, document):
        document.short = self.markdown.convert(document.short)
        document.content = self.markdown.convert(document.content)
        document.extension = '.html'
        return document
