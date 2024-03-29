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

setup(
    name='Nib',
    description='Static Site Generator',
    version='0.5.7',
    author='Amethyst Reese',
    author_email='amy@noswap.com',
    url='https://github.com/amyreese/nib',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
        'Development Status :: 4 - Beta',
    ],
    license='MIT License',
    install_requires=[
        'sh>=1.0',
        'Jinja2>=2.6',
        'Markdown>=2.2.0',
        'PyYAML>=3.10',
        'pymdown_extensions (>=10.0)',
    ],
    requires=[
        'sh (>=1.1)',
        'Jinja2 (>=2.8)',
        'Markdown (>=2.6.0)',
        'PyYAML (>=3.12)',
        'pymdown_extensions (>=10.0)',
    ],
    packages=['nib', 'nib.plugins'],
    package_data={'nib': ['defaults.nib', 'sample.zip']},
    scripts=['bin/nib'],
)
