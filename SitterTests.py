import unittest
from datetime import time

from Sitter import Sitter

class SitterTest(unittest.TestCase):
    def setUp(self):
        self.startTime = time(17,0,0) # 24-hr time in hr, min, sec
        self.endTime = time(21,0,0) # 24-hr time in hr, min, sec
        self.bedTime = time(19,0,0) # 24-hr time in hr, min, sec
        self.sitter = Sitter(startTime=self.startTime, endTime=self.endTime, bedTime=self.bedTime)

    def testAlwaysTrue(self):
        self.assertTrue(True)
        
    def testSitterInit(self):
        self.assertEqual(self.sitter.startTime, self.startTime)
        self.assertEqual(self.sitter.endTime, self.endTime)
        self.assertEqual(self.sitter.bedTime, self.bedTime)
        
    def testSitterTimesAreValid(self):
        self.assertTrue(self.sitter.validTimes())
        
if __name__ == "__main__":
    unittest.main()