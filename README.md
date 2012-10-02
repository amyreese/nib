Nib
===

Nib is a static site generator, written in Python, geared toward creating a
simple site or blog, with the ability to generate metadata pages based on
content attributes.  It understands concepts like tags, archives, and paging
series of individual entries into larger blocks of content.  It is designed to
be easily extended to create new content types with customized behaviors.


Concept
-------

Nib reads in hierarchical directory of Markdown-formatted documents that
contain YAML-formatted headers with attributes and metadata.  The metadata
includes a document type, which maps back to a series of predefined document
processors, as well as arbitrary attributes.

Document processors are then given a list of all documents that match the
processor's document type, then returns a modified list of documents.
Processors can modify existing documents, or optionally generate a set of
"virtual" pages to include in its return value, allowing processors to create
archives, tag pages, and more.

Once all document processors have been run, document bodies are run through
the Markdown processor, and then passed to the appropriate templates for final
rendering and output to static files.

Static resources, such as CSS, Javascript, and images, are then matched to
configurable resource processors and merged with the document output. This
step allows for use of pre-processors or generators for static resources,
such as LessCSS, JS minifiers, or image optimizers.


Requirements
------------

- Python 3


License
-------

Nib is licensed under the MIT license.  See the `LICENSE` file for details.
Libraries are licensed separately; see `lib/*/LICENSE*` files for details.


Credits
-------

Nib is developed by [John Reese](http://noswap.com) as a labor of love.
It builds on top of many fine projects from the open source community, such as:

- [Jinja2](http://jinja.pocoo.org)
- [Markdown](http://pypi.python.org/pypi/Markdown/)
- [PyYAML](http://pyyaml.org)
- [sh](https://github.com/amoffat/sh)

