import sh
from hammer import Processor, resource

@resource('.less')
class LessCSSProcessor(Processor):
    def process(self, resources):
        for r in resources:
            r.content = str(sh.lessc(r.path + r.extension))
            r.extension = '.css'

        return resources
