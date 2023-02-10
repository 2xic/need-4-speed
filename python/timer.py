import time
from collections import defaultdict
times = defaultdict(int)

def timer(func):
    def wrapper(*args):
        start = time.time()
        results = func(*args)
        times[func.__name__] += time.time() - start
        return results
    return wrapper
