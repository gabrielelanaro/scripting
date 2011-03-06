import argparse
parser = argparse.ArgumentParser()

def command(f):
    """Decorator used to define the commands launched by the
    commandline.

    """
    sub = parser.add_subparsers()
    cmdparser = sub.add_parser(f.__name__, help=f.__doc__)
    cmdparser.set_defaults(func=f)

def main():
    args = parser.parse_args()
    args.func()
