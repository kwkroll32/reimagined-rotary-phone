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
        
        # copy the sitter so it can be modified 
        thisSitter = copy.copy(self.sitter)
        # arrival is too early 
        thisSitter.startTime = time(14,0,0)
        self.assertFalse(thisSitter.validTimes())
        
        thisSitter = copy.copy(self.sitter)
        # ending is too late
        thisSitter.endTime = time(5,0,0)
        self.assertFalse(thisSitter.validTimes())
        
        thisSitter = copy.copy(self.sitter)
        # start time is equal to leave time
        thisSitter.endTime = thisSitter.startTime
        self.assertFalse(thisSitter.validTimes())
        
        thisSitter = copy.copy(self.sitter)
        # leaving after midnight 
        thisSitter.endTime = time(1,0,0)
        self.assertTrue(thisSitter.validTimes())
        
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
        
    def testSitterCalcWithFractionalHours(self):
        # sitter watches the kids for the evening 
        #   includes post-bedtime pay, but no midnight pay 
        
        # copy the sitter so it can be modified 
        thisSitter = copy.copy(self.sitter)
        thisSitter.startTime = time(17,15,0)
        thisSitter.endTime = time(20,15,0)
        # sitter works 1.25 hours with the kids awake, rounding up to 2
        # sitter works 2 hours with the kids asleep 
        calculatedPay = thisSitter.calcPay()
        expectedPay   = self.sitter.calcPay()
        # the sitter should earn the same pay whether they show up at 5 or 5:15, due to rounding up. 
        self.assertEqual(calculatedPay, expectedPay)
        
    def testSitterPayCalcNoBedTime(self):
        # sitter watches the kids for the evening. 
        #   no bedtime pay and no midnight pay
        
        # copy the sitter so it can be modified 
        thisSitter = copy.copy(self.sitter)
        thisSitter.bedTime = time(22,0,0) 
        # sitter works for 4 hrs, from 1700 to 2100
        # note that kids never go to bed and end time is before midnight 
        calculatedPay = thisSitter.calcPay()
        expectedPay = thisSitter.payRates['startToBed']*4
        self.assertEqual(calculatedPay, expectedPay)
    
    def testSitterPayCalcWithBedTimeBeforeMidnight(self):
        # sitter watches the kids and they go to bed 
        #   includes post-bedtime pay, but no midnight pay 
        
        # use the existing sitter object
        # works from 1700 to 1900 with kids awake
        # works from 1900 to 2100 with kids asleep 
        calculatedPay = self.sitter.calcPay()
        expectedPay   = self.sitter.payRates['startToBed']*2
        expectedPay  += self.sitter.payRates['bedToMidnight']*2
        self.assertEqual(calculatedPay, expectedPay)
        
    def testSitterPayCalcWithBedTimeBeforeMidnightAndEndAfterMidnight(self):
        # sitter watches the kids and they go to bed. sitter stays past midnight 
        #   includes post-bedtime pay and post-midnight pay 
        
        # copy the sitter so it can be modified 
        thisSitter = copy.copy(self.sitter)
        thisSitter.endTime = time(1,0,0) 
        # works from 1700 to 1900 with kids awake
        # works from 1900 to 0100 with kids asleep
        calculatedPay = thisSitter.calcPay()
        expectedPay = thisSitter.payRates['startToBed']*2 
        expectedPay += thisSitter.payRates['bedToMidnight']*5
        expectedPay += thisSitter.payRates['midnightToEnd']*1
        self.assertEqual(calculatedPay, expectedPay)
        
    def testSitterPayCalcWithBedTimeBeforeArrivalTime(self):
        # sitter arrives after kids are in bed 
        #   doesn't include pre-bedtime pay, but includes post-midnight
        
        # copy the sitter so it can be modified 
        thisSitter = copy.copy(self.sitter)
        thisSitter.bedTime = time(18,0,0)
        thisSitter.startTime = time(20,0,0) 
        thisSitter.endTime = time(1,0,0)
        # works from 1900 to 0100 with kids asleep 
        calculatedPay = thisSitter.calcPay()
        expectedPay   = thisSitter.payRates['bedToMidnight']*4
        expectedPay  += thisSitter.payRates['midnightToEnd']*1 
        self.assertEqual(calculatedPay, expectedPay)
        
    def testSitterPayCalcWithBedTimeEqualsArrivalTime(self):
        # sitter arrives the instant kids go to bed 
        #   doesn't include pre-bedtime pay, but includes post-midnight
        
        # copy the sitter so it can be modified 
        thisSitter = copy.copy(self.sitter)
        thisSitter.bedTime = time(18,0,0)
        thisSitter.startTime = time(18,0,0) 
        thisSitter.endTime = time(1,0,0)
        # works from 1800 to 0100 with kids asleep 
        calculatedPay = thisSitter.calcPay()
        expectedPay   = thisSitter.payRates['bedToMidnight']*6
        expectedPay  += thisSitter.payRates['midnightToEnd']*1 
        self.assertEqual(calculatedPay, expectedPay)
    
    def testSitterPayCalcMostExpensiveConfiguration(self):
        # sitter arrives at 5pm, kids up until midnight, sitter leaves at 4am 
        #   doesn't include post-bedtime pay, but includes post-midnight
        
        # copy the sitter so it can be modified 
        thisSitter = copy.copy(self.sitter)
        thisSitter.bedTime = time(00,0,0)
        thisSitter.endTime = time(4,0,0)
        calculatedPay = thisSitter.calcPay()
        # works from 1700 to 0000 with kids awake 
        expectedPay   = thisSitter.payRates['startToBed']*7
        # works from 0000 to 0400 with kids asleep
        expectedPay  += thisSitter.payRates['midnightToEnd']*4
        self.assertEqual(calculatedPay, expectedPay)
        

        
if __name__ == "__main__":
    unittest.main()