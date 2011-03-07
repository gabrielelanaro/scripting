from attest import Tests, capture_output
from scripting.runner import command, parser

tests = Tests()

@command
def foo():
    """No args at all!"""
    print 'foo called'

@command
def fooarg(pos1):
    print pos1

@tests.test
def test_dec():
    with capture_output() as (out, err):
        args = parser.parse_args(['foo'])
        args.func()
    assert out == ['foo called']
    
    with capture_output() as (out, err):
        args = parser.parse_args(['fooarg', 'pos1'])
    assert out == ['pos1']

if __name__ == '__main__':
    tests.run()
