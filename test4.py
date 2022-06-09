import inspect


def foo():
    frame = inspect.stack()[1]
    print(frame[0].f_code.co_filename)
