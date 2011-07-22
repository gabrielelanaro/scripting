from attest import Tests
from scripting import source
import os.path.join as jn
import os

tests = Tests()

DATADIR = 'scripting/tests/data'

@tests.test
def env_test():
    source(jn(DATADIR, "testenv.sh"))
    assert os.env["TESTVAR"] == "TESTVALUE"

if __name__ == '__main__':
    tests.run()