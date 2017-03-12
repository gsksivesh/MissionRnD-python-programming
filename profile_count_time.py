import functools
import time


class MutableBoolean(object):
    def __init__(self, value=True):
        self.value = value

    def __nonzero__(self):
        """To check if it's True or False"""
        if self.value:
            return 1
        return 0


def profile_count(skip_recursion=True):
    def log_function_count(func):
        if skip_recursion:
            top_call = MutableBoolean()  # mutable because it must be changed in the inner function

            @functools.wraps(func)
            def operating_function_count(*args, **kwargs):
                if top_call:  # top_call tells us whether it is a top call(True) or recursive call(False)
                    top_call.value = False
                    operating_function_count.count += 1
                    return_value = func(*args, **kwargs)
                    top_call.value = True
                    return return_value
                return func(*args, **kwargs)
        else:
            @functools.wraps(func)
            def operating_function_count(*args, **kwargs):
                operating_function_count.count += 1
                return func(*args, **kwargs)

        operating_function_count.count = 0
        return operating_function_count

    return log_function_count


def profile_time(func):
    top_call = MutableBoolean()

    @functools.wraps(func)
    def operating_function_time(*args, **kwargs):
        if top_call:
            top_call.value = False
            before_time = time.clock()
            return_value = func(*args, **kwargs)
            after_time = time.clock()
            top_call.value = True
            operating_function_time.time_elapsed += after_time - before_time
            return return_value
        return func(*args, **kwargs)

    operating_function_time.time_elapsed = 0
    return operating_function_time


@profile_count(False)
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ncount recursion=false")

fib(5)
print (fib.count)
fib(5)
print (fib.count)
fib(5)
print (fib.count)


@profile_count(True)
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ncount recursion=true")

fib(5)
print (fib.count)
fib(5)
print (fib.count)
fib(5)
print (fib.count)


@profile_time
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ntime")

fib(5)
print (fib.time_elapsed * 10000)
fib(5)
print (fib.time_elapsed * 10000)
fib(5)
print (fib.time_elapsed * 10000)


@profile_count(False)
@profile_time
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ncount recursion=false and time")

fib(5)
print (fib.time_elapsed * 10000)
print (fib.count)
fib(5)
print (fib.time_elapsed * 10000)
print (fib.count)
fib(5)
print (fib.time_elapsed * 10000)
print (fib.count)


@profile_count(True)
@profile_time
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ncount recursion=true and time")

fib(5)
print (fib.time_elapsed * 10000)
print (fib.count)
fib(5)
print (fib.time_elapsed * 10000)
print (fib.count)
fib(5)
print (fib.time_elapsed * 10000)
print (fib.count)
