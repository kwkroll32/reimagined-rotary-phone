# A class for the baby sitter 

class Sitter(object):
    def __init__(self):
        # important attributes
        self.startTime = 0
        self.endTime   = 0
        self.bedTime   = 0
        self.payRates  = { 'startToBed':    0, \
                           'bedToMidnight': 0, \
                           'midnightToEnd': 0  }
