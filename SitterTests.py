import unittest
from datetime import time

from Sitter import Sitter

class SitterTest(unittest.TestCase):
    def testAlwaysTrue(self):
        self.assertTrue(True)
        
    def testSitterInit(self):
        startTime = time(17,0,0) # 24-hr time in hr, min, sec
        endTime = time(21,0,0) # 24-hr time in hr, min, sec
        bedTime = time(19,0,0) # 24-hr time in hr, min, sec
        sitter = Sitter(startTime = startTime, endTime=endTime, bedTime=bedTime)
        self.assertEqual(sitter.startTime, startTime)
        self.assertEqual(sitter.endTime, endTime)
        self.assertEqual(sitter.bedTime, bedTime)
        
    def testSitterTimesAreValid(self):
        startTime = time(17,0,0) # 24-hr time in hr, min, sec
        endTime = time(21,0,0) # 24-hr time in hr, min, sec
        bedTime = time(19,0,0) # 24-hr time in hr, min, sec
        sitter = Sitter(startTime = startTime, endTime=endTime, bedTime=bedTime)
        self.assertTrue(sitter.validTimes())
        
if __name__ == "__main__":
    unittest.main()