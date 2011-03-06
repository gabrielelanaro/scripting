import os
import unittest
from attest import Tests, Assert

from scripting.commands import cp, rm, touch, mkdir, basename, archive, find
from scripting.commands import take_str_or_list

cptest = Tests()


@cptest.context
def make_test_file():
    """Make and return the test file, finally it removes it.

    """
    try:
        touch("stuff.txt")
        yield "stuff.txt"
    finally:
        rm_silent("stuff.txt")


def rm_silent(src):
    """Remove if the file exists.

    """
    if os.path.exists(src):
            rm(src)


@cptest.test
def cp_f_f(src):
    """Copy a file to another file.

    """
    try:
        cp(src, "/tmp/test.txt")
        Assert(os.path.exists("/tmp/test.txt"))
    finally:
        rm_silent("/tmp/test.txt")


@cptest.test
def cp_f_d(src):
    """Copy a file to a directory.

    """
    try:
        cp(src, "/tmp")
        Assert(os.path.exists(os.path.join("/tmp", basename(src))))
    finally:
        rm_silent("/tmp/test.txt")


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


class TestCp(unittest.TestCase):

    def test_dir_dir(self, ):
        """
        Create a directory structure and copy it
        """
        make_dir_structure()
        cp("testdir","/tmp")
        assert_dir_structure()

    def test_dir_dir_nonexistent(self):
        make_dir_structure()
        cp("testdir","/tmp/testdir")
        assert_dir_structure()

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
        
    
    # def test_error(self):
    #     mkdir("testdir")
    #     with self.assertRaises(Exception):
    #         rm("testdir")

    def tearDown(self):
        if os.path.exists("testdir"):
            rm("testdir")
        
    def test_dir_nested(self, ):
        """
        """
        make_dir_structure()
        rm("testdir")
        self.assertFalse(os.path.exists("testdir"))

class TestBasename(unittest.TestCase):
    def test_dir(self, ):
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

    def test_find(self, ):
        files = list(find("*.txt"))
        self.assertEqual(files,['./testdir/stuff.txt', './testdir/testdir2/stuff2.txt'])

    def tearDown(self):
        rm("testdir")

class TestTakeList(unittest.TestCase):
    def test_list(self, ):
        @take_str_or_list
        def function(arg):
            return 1
        self.assertEqual(function("Hello"), 1)
        self.assertEqual(function([1,2,3]),[1,1,1])


if __name__ == '__main__':
    cptest.run()
