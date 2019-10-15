import threading, signal
from core.utils.singleton import Singleton
from core.plugin_manager import PluginManager
from core.task_metadata_extractor import MetadataExtractor

class ProgramKilled(Exception):
    pass
    
def signal_handler(signum, frame):
    raise ProgramKilled

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# global values for init in modules
TASK_FILE_SUFIX = "_task"
TASKS_FOLDER = "dtasks"

class DaemonTaskManager(metaclass=Singleton):

    def __init__(self, execute_on_start = False):
        self.plugin_manager = PluginManager(TASKS_FOLDER, TASK_FILE_SUFIX)
        self.tasks_list = self.plugin_manager.scan()
        print(self.tasks_list)
        self.__retrive_metadata(self.tasks_list)
        self.__init_tasks()
        if (execute_on_start):
            self.runAll()

    def __retrive_metadata(self, tasks_list):
        metadata = {}
        for task in tasks_list:
            task_name = task[0]
            metadata[task_name] = {}
            task_obj = task[1]
            methods_metadata = MetadataExtractor(task_obj).exctract_methods_metadata()
            metadata[task_name]['methods_metadata'] = methods_metadata
        self.metadata = metadata
        print(self.metadata)
    
    def __init_tasks(self):
        tasks_object_list = []
        id_counter = 1
        for task in self.tasks_list:
            interval = 10 if id_counter == 2 else 0
            print("Create task with %s and id %s, name %s"%(str(interval),str(id_counter), task[0]))
            inited_task = task[1](id_counter,task[0], interval)
            tasks_object_list.append(inited_task)
            id_counter += 1
        self.tasks_object_list = tasks_object_list

    def runAll(self):
        for obj in self.tasks_object_list:
            print("Executing task!!!")
            obj.start()

    def getTasksList(self):
        for obj in self.tasks_object_list:
            obj.stop()

    def stopAll(self):
        pass
    
    def runByName(self, taskName):
        pass

    def stopByName(self, taskName):
        pass