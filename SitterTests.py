import unittest
from datetime import time
import copy

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
        # 9am from 8am
        self.assertEqual(1.0,self.sitter.subtractTimes(time(9),time(8)))
        # 8pm from 5pm 
        self.assertEqual(3.0,self.sitter.subtractTimes(time(20),time(17)))
        # midnight from 11pm
        self.assertEqual(1.0,self.sitter.subtractTimes(time(00),time(23)))
        # 1am from midnight 
        self.assertEqual(1.0,self.sitter.subtractTimes(time(1),time(00)))
        # 1am from 11pm
        self.assertEqual(2.0,self.sitter.subtractTimes(time(1),time(23)))
        # 4am from 5pm
        self.assertEqual(11.0,self.sitter.subtractTimes(time(4),time(17)))
        self.assertFalse(11.0==self.sitter.subtractTimes(time(3),time(17)))
        
    def testSitterPayCalcNoBedTime(self):
        # copy the sitter so it can be modified 
        thisSitter = copy.copy(self.sitter)
        thisSitter.bedTime = time(22,0,0) 
        # sitter works for 4 hrs, from 1700 to 2100
        # note that kids never go to bed and end time is before midnight 
        calculatedPay = thisSitter.calcPay()
        expectedPay = thisSitter.payRates['startToBed']*4
        self.assertEqual(calculatedPay, expectedPay)
    
    def testSitterPayCalcWithBedTimeBeforeMidnight(self):
        # use the existing sitter object
        # works from 1700 to 1900 with kids awake
        # works from 1900 to 2100 with kids asleep 
        calculatedPay = self.sitter.calcPay()
        expectedPay   = self.sitter.payRates['startToBed']*2
        expectedPay  += self.sitter.payRates['bedToMidnight']*2
        self.assertEqual(calculatedPay, expectedPay)
        
if __name__ == "__main__":
    unittest.main()