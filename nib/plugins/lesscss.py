import sh
from nib import Processor, resource

@resource('.less')
class LessCSSProcessor(Processor):
    def process(self, resource):
        resource.content = str(sh.lessc(resource.path + resource.extension))
        resource.extension = '.css'

        return resource
