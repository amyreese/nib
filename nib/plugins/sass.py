from __future__ import absolute_import, division, print_function, unicode_literals

from os import path
import sh
from nib import Processor, resource

@resource(['.sass', '.scss'])
class SassProcessor(Processor):
    def resource(self, resource):
        filepath = path.join(self.options['resource_path'],
                             resource.path + resource.extension)
        resource.content = bytearray(str(sh.sass(filepath)), 'utf-8')
        resource.extension = '.css'

        return resource
