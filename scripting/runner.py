import argparse
import inspect

parser = argparse.ArgumentParser()
sub = parser.add_subparsers()

def command(f):
    """Decorator used to define the commands launched by the
    commandline.

    """
    args = inspect.getargspec(f)
    cmdparser = sub.add_parser(f.__name__, help=f.__doc__)
    
    for name in args[0]:
        cmdparser.add_argument(name)
    
    # unpacking args from the namespace
    def wrapped(ns):
        f(*(getattr(ns, name) for name in args[0]))
    
    cmdparser.set_defaults(func=wrapped)
    
    return f

def run():
    args = parser.parse_args()
    args.func(args)
