from scripting import source
from os.path import join as jn
import os


DATADIR = 'tests/data'

def env_test():
    source(jn(DATADIR, "testenv.sh"))
    assert os.environ["TESTVAR"] == 'TESTVALUE'

