from inspect import getmembers
from rich import inspect

# dump and die
def dd(*args):
    for arg in args:
        inspect(arg, methods=True, value=True)
    exit()