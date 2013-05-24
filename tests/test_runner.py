from scripting.runner import command, parser

foocalled = False
fooargcalled = False

@command
def foo():
    """No args at all!"""
    global foocalled
    foocalled = True

@command
def fooarg(pos1):
    global fooargcalled
    fooargcalled = True

def test_dec():
    args = parser.parse_args(['foo'])
    args.func(args)
    assert foocalled
    
    args = parser.parse_args(['fooarg', 'pos1'])
    args.func(args)
    assert fooargcalled

if __name__ == '__main__':
    test_dec()
