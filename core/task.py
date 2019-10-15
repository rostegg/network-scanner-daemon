import threading, time
from datetime import timedelta

class ExecuteTaskNotImplemented(Exception):
    pass

RESPONSE_DECORATOR_NAME = "response"
PRINTABLE_DECORATOR_NAME = "printable"
REMOTE_EXECUTABLE = [RESPONSE_DECORATOR_NAME, PRINTABLE_DECORATOR_NAME]

def execute_timed(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return { 'execution_result': result, 'execution_time' : (end_time - start_time) }

def response(func):
    def execute_with_metadata(*args, **kwargs):
        result_dict = execute_timed(func, *args, **kwargs)
        result_dict['method_name'] = func.__name__
        result_dict['args'] = args
        result_dict['kwargs'] = kwargs
        # log if need
        return result_dict
    return execute_with_metadata

def printable(func):
    def execute_with_metadata(*args, **kwargs):
        result_dict = execute_timed(func, *args, **kwargs)
        return result_dict['execution_result']
    return execute_with_metadata

class DaemonTask(threading.Thread):
    def __init__(self, thread_id, name, interval:int, *args, **kwargs):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.stopped = threading.Event()
        self.interval = timedelta(seconds=(interval if interval > 0 else 0))
        self.args = args
        self.kwargs = kwargs

    def execute_task(self):
        raise ExecuteTaskNotImplemented

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute_task(*self.args, **self.kwargs)

            