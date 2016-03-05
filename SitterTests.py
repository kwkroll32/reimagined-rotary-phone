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
        
    def testTimeSubtractionFunction(self):
        self.assertEqual(1.0,self.sitter.subtractTimes(time(9),time(8)))
        self.assertEqual(3.0,self.sitter.subtractTimes(time(20),time(17)))
        self.assertEqual(1.0,self.sitter.subtractTimes(time(00),time(23)))
        self.assertEqual(1.0,self.sitter.subtractTimes(time(1),time(00)))
        
    def testSitterPayCalcNoBedTime(self):
        startTime = time(17,0,0) 
        endTime = time(21,0,0) 
        bedTime = time(22,0,0) 
        # sitter works for 4 hrs 
        # note that kids never go to bed and end time is before midnight 
        sitter = Sitter(startTime=startTime, endTime=endTime, bedTime=bedTime)
        calculatedPay = sitter.calcPay()
        expectedPay = sitter.payRates['startToBed']*4
        self.assertEqual(calculatedPay, expectedPay)
        
if __name__ == "__main__":
    unittest.main()