import sh
from nib import Processor, resource

@resource('.less')
class LessCSSProcessor(Processor):
    def process(self, resource):
        resource.content = bytes(str(sh.lessc(resource.path + resource.extension)), 'utf-8')
        resource.extension = '.css'

        return resource
