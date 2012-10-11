from os import path
import sh
from nib import Processor, resource

@resource('.less')
class LessCSSProcessor(Processor):
    def resource(self, resource):
        filepath = path.join(self.options['resource_path'],
                             resource.path + resource.extension)
        resource.content = bytes(str(sh.lessc(filepath)), 'utf-8')
        resource.extension = '.css'

        return resource
