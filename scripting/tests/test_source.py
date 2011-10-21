from attest import Tests
from scripting import source
from os.path import join as jn
import os

tests = Tests()

DATADIR = 'scripting/tests/data'

@tests.test
def env_test():
    source(jn(DATADIR, "testenv.sh"))
    assert os.environ["TESTVAR"] == 'TESTVALUE'

if __name__ == '__main__':
    from attest.reporters import PlainReporter
    tests.run(PlainReporter)