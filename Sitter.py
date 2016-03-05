from datetime import time
# A class for the baby sitter 

class Sitter(object):
    def __init__(self, startTime, endTime, bedTime):
        # important attributes
        self.startTime = startTime
        self.endTime   = endTime
        self.bedTime   = bedTime
        self.payRates  = { 'startToBed':    0, \
                           'bedToMidnight': 0, \
                           'midnightToEnd': 0  }
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