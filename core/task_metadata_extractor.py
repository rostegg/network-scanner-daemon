from core.task import REMOTE_EXECUTABLE
import inspect

class MetadataExtractor(object):

    def __init__(self, task):
        self.task = task
        
    def exctract_methods_metadata(self):
        metadata = {}
        for decorator in REMOTE_EXECUTABLE:
            decorated_methods = list(self.__methods_with_decorator(self.task, decorator))
            metadata[decorator] = decorated_methods    
        return metadata
    
    def __methods_with_decorator(self, cls, decorator_name):
        sourcelines = inspect.getsourcelines(cls)[0]
        for i,line in enumerate(sourcelines):
            line = line.strip()
            if line.split('(')[0].strip() == '@'+decorator_name:
                nextLine = sourcelines[i+1]
                name = nextLine.split('def')[1].split('(')[0].strip()
                yield(name)