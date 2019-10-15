from core.task import DaemonTask, response, printable
import time

class SelfEternityTask2(DaemonTask):
    def execute_task(self):
        while (True):
            print("Hi from another file task")
            time.sleep(3)