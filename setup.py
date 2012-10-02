from setuptools import setup

from os import path
import shutil
if path.isfile('README.md'):
    shutil.copyfile('README.md', 'README')

setup(name='Nib',
      description='Static Site Generator',
      version='0.2.4',
      author='John Reese',
      author_email='john@noswap.com',
      url='https://github.com/jreese/nib',
      classifiers=['License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: Utilities',
                   'Development Status :: 2 - Pre-Alpha',
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
      package_data={'nib': ['config.defaults']},
      scripts=['bin/nib'],
      )
