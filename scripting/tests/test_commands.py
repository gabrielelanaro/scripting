from __future__ import generators
import os
import unittest

from scripting.commands import (cp, rm, touch, mkdir,
                                basename, archive, find,
                                unpack, sh)
from scripting.commands import take_str_or_list


def make_test_file():
    """Make and return the test file, finally it removes it.

    """
    
    touch("stuff.txt")
    return "stuff.txt"
    
def rm_test_file():
    rm_silent("stuff.txt")

    
class CpTest(unittest.TestCase):
    def setUp(self):
        self.src = make_test_file()
    def tearDown(self):
        rm_test_file()


    def test_cp_f_f(self):
        """Copy a file to another file.

        """
        src = self.src
        try:
            cp(src, "/tmp/test.txt")
            assert (os.path.exists("/tmp/test.txt"))
        finally:
            rm_silent("/tmp/test.txt")

    def test_cp_f_d(self):
        """Copy a file to a directory.

        """
        src = self.src
        try:
            cp(src, "/tmp")
            assert (os.path.exists(os.path.join("/tmp", basename(src))))
        finally:
            rm_silent("/tmp/test.txt")

def rm_silent(src):
    """Remove if the file exists.

    """
    if os.path.exists(src):
            rm(src)
        
class CpDirTest(unittest.TestCase):
    def setUp(self):
        make_dir_structure()
    def tearDown(self):
        rm_silent("testdir")
        
    def test_cp_d_d(self):
        try:
            cp('testdir', '/tmp')
            assert_dir_structure()
        finally:
            rm_silent('/tmp/testdir')

    def test_cp_d_d_nonexistent(self):
        try:
            cp("testdir","/tmp/testdir")
            assert_dir_structure()
        finally:
            rm_silent('/tmp/testdir')

def make_dir_structure():
    mkdir("testdir")
    touch("testdir/stuff.txt")
    mkdir("testdir/testdir2")
    touch("testdir/testdir2/stuff2.txt")


def assertfile(src, descriptor):
    ret = True
    if "d" in descriptor:
        ret = ret and os.path.isdir(src)
    if "e" in descriptor:
        ret = ret and os.path.exists(src)
    if "f" in descriptor:
        ret = ret and os.path.isfile(src)
    assert ret


def assert_dir_structure():
    assertfile("/tmp/testdir", "d")
    assertfile("/tmp/testdir/stuff.txt", "f")
    assertfile("/tmp/testdir/testdir2", "d")
    assertfile("/tmp/testdir/testdir2/stuff2.txt", "f")

DATADIR = 'scripting/tests/data'


class TestArchive(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        rm_silent("/tmp/testarc")

    def test_unpack_tgz(self):
        unpack(os.path.join(DATADIR, 'testarc.tar.gz'), '/tmp')
        #assertfile("/tmp/testarc/file1.txt", "f") # Maybe the other are present, anyway

    def test_unpack_zip(self):
        unpack(os.path.join(DATADIR, 'testarc.zip'), "/tmp")
        #assertfile("/tmp/testarc/file1.txt", "f") # Maybe the other are present, anyway


class TestRm(unittest.TestCase):
    def test_dir(self):
        """Testing the directory removal
        """
        mkdir("testdir")
        rm("testdir")
        self.assertFalse(os.path.exists("testdir"))

    def test_file(self):
        """Testing the file removal"""
        touch("test.txt")
        self.assert_(os.path.exists("test.txt"))
        rm("test.txt")
        

    def tearDown(self):
        if os.path.exists("testdir"):
            rm("testdir")
        
    def test_dir_nested(self):
        """
        """
        make_dir_structure()
        rm("testdir")
        self.assertFalse(os.path.exists("testdir"))

class TestBasename(unittest.TestCase):
    def test_dir(self):
        """
        """
        name = "/hello/world/"
        self.assertEqual(basename(name), "world")
    def test_file(self):
        name = "/hello/baby"
        self.assertEqual(basename(name),"baby")
        
class TestTar(unittest.TestCase):
    def setUp(self):
        make_dir_structure()
        
    def test_archive(self):
        archive("testdir","testdir.tar")
        self.assert_(os.path.exists("testdir.tar"))
    
    def tearDown(self):
        rm("testdir")
        rm("testdir.tar")

class TestFind(unittest.TestCase):
    def setUp(self, ):
        make_dir_structure()

    def test_find(self):
        files = list(find("*.txt", "./testdir"))
        self.assertEqual(files,['./testdir/stuff.txt', './testdir/testdir2/stuff2.txt'])

    def tearDown(self):
        rm("testdir")

class TestUtils(unittest.TestCase):
    def test_take_list_text(self):
        @take_str_or_list
        def function(arg):
            return 1
        assert function("Hello") == 1
        assert function([1,2,3]) == [1,1,1]

class TestSh(unittest.TestCase):
    def test_sh(self):
        ex, out, err = sh("ls -l")
        assert out
if __name__ == '__main__':
    unittest.main()
