#!/usr/bin/env python3

#from dtasks.simple_task import SimpleTask, NotImplementedTask, SelfEternityTask
from core.task_manager import ProgramKilled
from core.task import DaemonTask
import time
import inspect

#job = SimpleTask(thread_id = 1, name = "SimpleTask", interval=10)

'''
def call_method(obj, name, *args, **kwargs):
    return getattr(obj, name)(*args, **kwargs)

def methods_with_decorator(cls, decoratorName):
    sourcelines = inspect.getsourcelines(cls)[0]
    for i,line in enumerate(sourcelines):
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decoratorName: # leaving a bit out
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            yield(name)
'''

#print(list(  methods_with_decorator(SimpleTask, 'response_func')  ))

#print(call_method(job, "return_printable", value=1))

"""
import sys, importlib
def retrive_plugins():

    def retrieve_tasks_from_module(module_name):
        task_module = __import__(module_name, fromlist=[''])
        return [t for t in inspect.getmembers(task_module, inspect.isclass) if t[1].__base__ is DaemonTask]

    importlib.invalidate_caches()
    tasks_module = importlib.import_module(TASKS_FOLDER)
    declarated_modules = [ ('%s.%s')%(tasks_module.__name__,f) for f in dir(tasks_module) if f.endswith(TASK_FILE_SUFIX) ]
    tasks_list = list()
    for module_name in declarated_modules:
        tasks_list.extend(retrieve_tasks_from_module(module_name))
    return tasks_list

lst = retrive_plugins()
print(lst)
ob = lst[1][1](1, "name", 0)
print(ob)
print(ob.return_printable())
"""

from core.task_manager import DaemonTaskManager
task_manager = DaemonTaskManager(True)
while(True):
    try:
        time.sleep(10)
        print("Message from main thread")
    except ProgramKilled:
        print ("Program killed: running cleanup code")
        task_manager.stopAll()
        break

'''job.start()
while(True):
    try:
        time.sleep(5)
        print(job.return_response())
    except ProgramKilled:
        print ("Program killed: running cleanup code")
        job.stop()
        break
'''