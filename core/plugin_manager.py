from core.utils.singleton import Singleton
from core.task import DaemonTask
import sys, importlib
import inspect

class PluginManager(metaclass=Singleton):

    def __init__(self, tasks_folder, tasks_sufix):
        self.tasks_folder = tasks_folder
        self.tasks_sufix = tasks_sufix
        self.plugins_list = []
    
    def scan(self):
        result_list = self.__retrive_plugins()
        # compare to exist plugins later
        return result_list

    def __retrive_plugins(self):
        def retrieve_tasks_from_module(module_name):
            task_module = __import__(module_name, fromlist=[''])
            return [t for t in inspect.getmembers(task_module, inspect.isclass) if t[1].__base__ is DaemonTask]

        importlib.invalidate_caches()
        tasks_module = importlib.import_module(self.tasks_folder)
        declarated_modules = [ ('%s.%s')%(tasks_module.__name__,f) for f in dir(tasks_module) if f.endswith(self.tasks_sufix) ]
        tasks_list = list()
        for module_name in declarated_modules:
            tasks_list.extend(retrieve_tasks_from_module(module_name))
        return tasks_list