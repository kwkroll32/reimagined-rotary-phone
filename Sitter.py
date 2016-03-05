from datetime import time
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