from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n:int) -> int:
    if (n < 0):
       raise Exception("[NegativeIntegerException]: Negative Integer. Cannot Parse!")
    elif (n == 0): 
        return 0 
    elif (n == 1 or n == 2):
        return 1
    elif n > 2:
        return fib(n-1) + fib(n-2)


