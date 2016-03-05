from datetime import time, datetime, date
# A class for the baby sitter 

class Sitter(object):
    def __init__(self, startTime, endTime, bedTime):
        # important attributes
        self.startTime = startTime
        self.endTime   = endTime
        self.bedTime   = bedTime
        # hourly rates for the 3 defined segments of time 
        self.payRates  = { 'startToBed':    12, \
                           'bedToMidnight': 8,  \
                           'midnightToEnd': 16  }
    def validTimes(self):
        '''
        method to determine whether the sitter instance is valid 
        Input: an instance of sitter 
        Output: bool 
        '''
        # as defined in the problem statement
        # starts no earlier than 5pm and leaves no later than 4AM
        earliestStart = time(17,00,00)
        latestEnd     = time(4,00,00)
        
        # do we start too early?
        if self.startTime < earliestStart:
            return False
        # did we end too late?
        if self.endTime < self.startTime and self.endTime > latestEnd:
            return False
        # if nothing failed, the schedule is valid 
        return True
    
    def calcPay(self):
        '''
        method to calculate pay for the evening
        Input: an instance of sitter 
        Output: payment due (float)
        '''
        hours = self.subtractTimes(self.endTime, self.startTime)
        rate  = 12
        due   = hours*rate
        return due
        
    def subtractTimes(self, time1, time2):
        '''
        method to find the difference between two times
        Input: two datetime.time objects
        Output: the difference between them in hours (float)
        '''
        ref = date.today()
        diff = datetime.combine(ref, time1) - datetime.combine(ref, time2)
        return diff.seconds/3600
        
        