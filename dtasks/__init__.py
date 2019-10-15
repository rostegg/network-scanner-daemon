import os
from core.task_manager import TASK_FILE_SUFIX, TASKS_FOLDER
print(TASK_FILE_SUFIX)
print(TASKS_FOLDER)
for module in os.listdir(os.path.dirname(__file__)):
    if module.endswith(('%s.%s')%(TASK_FILE_SUFIX, 'py')):
        __import__(('%s.%s')%(TASKS_FOLDER, module[:-3]), locals(), globals())
del module