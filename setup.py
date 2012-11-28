from setuptools import setup

import os
from os import path
import shutil

if path.isfile('README.md'):
    shutil.copyfile('README.md', 'README')

if path.isdir('sample'):
  if path.exists('sample/site'):
      shutil.rmtree('sample/site')
  if path.exists('sample/config.nib'):
      os.unlink('sample/config.nib')
  shutil.make_archive('nib/sample', 'zip', 'sample')

import nib

setup(name='Nib',
      description='Static Site Generator',
      version=nib.version,
      author='John Reese',
      author_email='john@noswap.com',
      url='https://github.com/jreese/nib',
      classifiers=['License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: Utilities',
                   'Development Status :: 3 - Alpha',
                   ],
      license='MIT License',
      install_requires=['sh>=1.0',
                        'Jinja2>=2.6',
                        'Markdown>=2.2.0',
                        'PyYAML>=3.10',
                        ],
      requires=['sh (>=1.0)',
                'Jinja2 (>=2.6)',
                'Markdown (>=2.2.0)',
                'PyYAML (>=3.10)',
                ],
      packages=['nib', 'nib.plugins'],
      package_data={'nib': ['defaults.nib', 'sample.zip']},
      scripts=['bin/nib'],
      )
