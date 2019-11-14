from time import time 

def timed(func):
    def _timed(*args,**kwargs):
        start = time()
        results = func(*args,**kwargs)
        end = time() - start 
        print("{} took {}".format(func.__name__,end))
        return results
    return _timed

