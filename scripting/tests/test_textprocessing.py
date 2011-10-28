import unittest
from scripting.textprocessing import sections, grep_split

class TestSection(unittest.TestCase):

    def test_section(self):
        teststr = '''
        starting stuff
        hello
        baby
        stopping stuff


        starting stuff
        oh my god
        wtf
        stopping stuff
        ''' 
        a, b = sections(teststr, "starting stuff","stopping stuff")
        self.assertEqual(a, "        hello\n        baby")
        self.assertEqual(b, "        oh my god\n        wtf")
    def test_section_recursive(self):
        teststr = '''
        starting stuff
        hello
        baby
        starting stuff
        hi
        stopping stuff
        '''
        a = sections(teststr, "starting stuff", "stopping stuff")
        check = '''        hello
        baby
        starting stuff
        hi'''
        self.assertEqual(a[0], check)

    def test_section_endnone(self):
        teststr = '''
        starting stuff
        hello
        baby
        starting stuff
        hello
        world'''
        a, b, c = grep_split("starting stuff", teststr)
        self.assertEqual(a, '')
        self.assertEqual(b, "        starting stuff\n        hello\n        baby")
        self.assertEqual(c, "        starting stuff\n        hello\n        world")

if __name__ == '__main__':
    unittest.main()
    
