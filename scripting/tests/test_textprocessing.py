import unittest
from scripting.textprocessing import sections

class TestSection(unittest.TestCase):
    
    def setUp(self):
        self.teststr = '''
        starting stuff
        hello
        baby
        stopping stuff


        starting stuff
        oh my god
        wtf
        stopping stuff
        ''' 
        
    def tearDown(self):
        pass

    def test_section(self):
        a, b = sections(self.teststr, "starting stuff","stopping stuff")
        self.assertEqual(a, "        hello\n        baby")
        self.assertEqual(b, "        oh my god\n        wtf")

if __name__ == '__main__':
    unittest.main()
    
