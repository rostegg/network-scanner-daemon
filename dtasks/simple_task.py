from core.task import DaemonTask, response, printable
from core.task_manager import ProgramKilled
import time

class SimpleTask(DaemonTask):
    return_str = "Its a me, taskio" 
    
    @response
    def return_response(self, *args, **kwargs):
        return self.return_str

    @printable
    def return_printable(self, *args, **kwargs):
        return "Heya"
    
    def execute_task(self):
        try:
            print(time.ctime())
        except ProgramKilled:
            print("I get it!!!!")

class SelfEternityTask(DaemonTask):
    def execute_task(self):
        try:
            while(True):
                print("Hi self entity")
                time.sleep(15)
        except ProgramKilled:
            print("I get it!")
