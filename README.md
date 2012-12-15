Nib
===

Nib is a static site generator, written in Python, geared toward creating a
simple site or blog.  Nib uses a pluggable content pipeline that differentiates
between "resources" like CSS or Javascript, and "documents" such as static pages
or blog posts. The two pipelines are similar, are executed in parallel, and
define multiple hooks where plugins can process a subset of entities, and even
remove entities or generate new ones at runtime.

An example site generated from the default wizard and templates is available at
http://nib.noswap.com


Requirements
------------

- Python 3.2


Installation
------------

To install the latest official release:

    $ pip3 install nib

or to install the version currently checked out from source:

    $ python3 setup.py install


Getting Started
---------------

Once Nib is installed, you can generate basic configuration and site using the
built-in wizard:

    $ mkdir somesite && cd somesite
    $ nib wizard
    ...

Once the wizard is complete, you should have a site configuration file, some
example documents (a page and two blog posts), and a minimal site theme
consisting of resources (favicon, CSS, and robots.txt), and templates:

    $ ls
    config.nib  documents/  resources/  templates/

    $ ls documents
    about.md  links/  posts/

    $ ls resources
    favicon.ico  main.less  robots.txt

    $ ls templates
    feed.xml  list.html  macros.html  page.html  post.html  posts.html

To build the site:

    $ nib
    ...
    Done

The resulting HTML and resources will be in the `site/` directory:

    $ ls
    config.nib  documents/  resources/  site/  templates/

    $ ls site
    2012/  about.html  archive.html  favicon.ico  feed.xml  index.html  links/  main.css  posts/  robots.txt  tags/

To test the resulting site, Nib can run a simple HTTP server, as well as open
the local server in your preferred web browser:

    $ nib serve
    Serving site on port 8000... press Ctrl-C to terminate.
    ^C
    Done

or:

    $ nib serve --port 9000 --browse
    Serving site on port 9000... press Ctrl-C to terminate.
    Opening http://localhost:9000 in web browser...
    ^C
    Done


License
-------

Nib is licensed under the MIT license.  See the `LICENSE` file for details.


Credits
-------

Nib is developed by [John Reese](http://noswap.com) as a labor of love.
It builds on top of many fine projects from the open source community, such as:

- [Jinja2](http://jinja.pocoo.org)
- [Markdown](http://pypi.python.org/pypi/Markdown/)
- [PyYAML](http://pyyaml.org)
- [sh](https://github.com/amoffat/sh)

Inspiration for Nib its design is thanks to
[Oben Sonne](http://obensonne.bitbucket.org/) and his project
[Poole](http://bitbucket.org/obensonne/poole).
