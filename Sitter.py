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
