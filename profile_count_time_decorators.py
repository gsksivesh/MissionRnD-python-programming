import functools
import time


class MutableInt(object):
    def __init__(self, value):
        self.value = value


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
        top_call = MutableBoolean()  # mutable because it must be changed in the inner function
        if skip_recursion:
            @functools.wraps(func)
            def operating_function_count(*args, **kwargs):
                if top_call:  # top_call tells us whether it is a top call(True) or recursive call(False)
                    top_call.value = False
                    operating_function_count.count.value += 1
                    return_value = func(*args, **kwargs)
                    top_call.value = True
                    return return_value
                else:
                    return func(*args, **kwargs)
        else:
            @functools.wraps(func)
            def operating_function_count(*args, **kwargs):
                operating_function_count.count.value += 1
                return func(*args, **kwargs)

        operating_function_count.count = MutableInt(0)
        return operating_function_count

    return log_function_count


def profile_time(skip_recursion=True):
    def log_function_count(func):
        top_call = MutableBoolean()  # mutable because it must be changed in the inner function
        if skip_recursion:
            @functools.wraps(func)
            def operating_function_time(*args, **kwargs):
                if top_call:  # top_call tells us whether it is a top call(True) or recursive call(False)
                    top_call.value = False
                    before_time = time.clock()
                    return_value = func(*args, **kwargs)
                    after_time = time.clock()
                    top_call.value = True
                    operating_function_time.time_elapsed.value += after_time - before_time
                    return return_value
                else:
                    return func(*args, **kwargs)
        else:
            @functools.wraps(func)
            def operating_function_time(*args, **kwargs):
                before_time = time.clock()
                return_value = func(*args, **kwargs)
                after_time = time.clock()
                operating_function_time.time_elapsed.value += after_time - before_time
                return return_value
        operating_function_time.time_elapsed = MutableInt(0)
        return operating_function_time

    return log_function_count


@profile_count(False)
@profile_time(False)
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ncount recursion=false and time recursion =false")

fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)


@profile_count(True)
@profile_time(False)
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ncount recursion=true and time recursion =false")

fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)


@profile_count(False)
@profile_time(True)
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ncount recursion=false and time recursion =true")

fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)


@profile_count(True)
@profile_time(True)
def fib(n):
    if n <= 0:
        raise ValueError("n <= 0")
    if n == 1 or n == 2:
        return 1

    return fib(n - 1) + fib(n - 2)


print ("\ncount recursion=true and time recursion =true")

fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
fib(5)
print (fib.time_elapsed.value * 10000)
print (fib.count.value)
