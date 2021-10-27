from time import time


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


class Timer:
    def __init__(self):
        print("-- Timer started.")
        self.time_start = time()

    def break_lap(self):
        elapsed_duration = time() - self.time_start
        self.time_start = time()
        return round(elapsed_duration, 4)
