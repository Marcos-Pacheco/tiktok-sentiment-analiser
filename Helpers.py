from pprint import pprint
from inspect import getmembers

# dump and die
def dd(args):
    pprint(getmembers(args))
    exit