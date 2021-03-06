from datetime import time, datetime, date
import math
import argparse
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
    def __str__(self):
        # method to pretty print the sitter object
        outstr = ""
        outstr += "Start Time:\t{0}\n".format(self.startTime)
        outstr += "Bed   Time:\t{0}\n".format(self.bedTime)
        outstr += "End   Time:\t{0}\n\n".format(self.endTime)
        outstr += "${0}/hr from start to bed\n".format(self.payRates['startToBed'])
        outstr += "${0}/hr from bed to midnight\n".format(self.payRates['bedToMidnight'])
        outstr += "${0}/hr from midnight to end\n".format(self.payRates['midnightToEnd'])
        return outstr
        
    def validTimes(self):
        '''
        method to determine whether the sitter instance is valid 
        Input: an instance of sitter 
        Output: bool 
        Note: could throw specific errors here if user needs to know what
              aspect of the time is invalid 
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
        # is the input start time later than the end time? 
        if self.startTime >= self.endTime and self.endTime >= earliestStart:
            return False
        if self.bedTime > time(00,0,0) and self.bedTime < earliestStart:
            return False
        # if nothing failed, the schedule is valid 
        return True
    
    def calcPay(self):
        '''
        method to calculate pay for the evening
        Input: an instance of sitter 
        Output: payment due (float)
        '''
        # create a sorted list of times and subset it to start-through-end 
        times = sorted([ self.startTime, self.endTime, self.bedTime, time(00,0,0) ])
        # re-sort the list to be in a meaningful order for the problem, 
        # i.e. start, bed, midnight, with end somewhere in between 
        times = times[times.index(self.startTime):] + times[:times.index(self.startTime)] 
        indexOfStart = times.index(self.startTime)
        indexOfEnd   = times.index(self.endTime)
        due = 0
        for timesIndex in range(indexOfStart, indexOfEnd):
            hours = self.subtractTimes(times[timesIndex+1], times[timesIndex])
            rate  = self.getPayRate(times[timesIndex], times[timesIndex+1])
            due  += hours*rate
        return due
        
    def subtractTimes(self, time1, time2):
        '''
        method to find the difference between two times
        Input: two datetime.time objects
        Output: the difference between them in hours (int)
        '''
        ref = date.today()
        diff = datetime.combine(ref, time1) - datetime.combine(ref, time2)
        # round up to whole hours, as per problem definition 
        return math.ceil(diff.seconds/3600)
        
    def getPayRate(self,time1,time2):
        '''
        method to get the pay rate for the given input times.
        note that times must be adjacent
            i.e. start=5pm, bed=9pm, midnight=12am, end=1am
            must execute as getPayRate(5pm, 9pm), getPayRate(9pm,12am), getPayRate(12am,1am)
            and NOT as getPayRate(5pm,1am), since that block of time spans multiple pay rates.
        Input: two datetime.time objects
        Output: the pay rate for the time between (float)
        '''
        midnight = time(00,0,0)
        # canonical cases, where sitter arrives, kids go to bed, and midnight comes, in that order.
        # end time may occur any time after arrival.  
        if time1 == self.startTime and (time2 == self.bedTime or time2 == self.endTime):
            return self.payRates['startToBed'] 
        elif time1 == self.bedTime and (time2 == self.endTime or time2 == midnight):
            if self.bedTime != midnight:
                # did the kids go to bed before midnight?
                return self.payRates['bedToMidnight']
            else:
                # the kids must have gone to bed at midnight 
                # since bedtime after midnight is invalid 
                return self.payRates['midnightToEnd']
        elif time1 == midnight and time2 == self.endTime:
            return self.payRates['midnightToEnd']
        # non-canonical cases 
        elif time1 == self.startTime and self.startTime > self.bedTime :
            # sitter arrives after kids are in bed 
            return self.payRates['bedToMidnight']
        else:
            # an unexpected set of adjacent times 
            print("unable to determine pay rate from {0} to {1}".format(time1, time2 ))
            exit()
            
def main():
    parser = argparse.ArgumentParser(description='Calculate pay for an evening of baby sitting.')
    parser.add_argument('--s', '--startTime', required=True, help='start time in 24hr format, e.g. 1700 ')
    parser.add_argument('--e', '--endTime', required=True, help='end time in 24hr format, e.g. 0100 ')
    parser.add_argument('--b', '--bedTime', required=True, help='bed time in 24hr format, e.g. 1900 ')
    args = parser.parse_args()

    # verify that args are valid
    for arg in [args.s, args.e, args.b]:
        if len(list(str(arg))) != 4:
            # check for hours and minutes present 
            print("invalid time {0}".format(arg))
            exit()
        elif not int(str(arg)[0:2]) < 24 or not int(str(arg)[0:2])>=0:
            # check that hours are between 0 and 24
            print("invalid hour {0}".format(arg))
            exit()
        elif not int(str(arg)[2:4]) < 60 :
            # check that minutes are less than 60
            print("invalid minute {0}".format(arg))
            exit()

    sitter = Sitter(startTime = time(int(args.s[0:2]), int(args.s[2:])), \
                    endTime = time(int(args.e[0:2]), int(args.e[2:])),   \
                    bedTime = time(int(args.b[0:2]),int(args.b[2:])) )
    if not sitter.validTimes():
        print("invalid times selected")
        exit()
    paymentDue = sitter.calcPay()
    print(str(sitter))
    print("Total Due: ${0}".format(paymentDue))
    
if __name__ == "__main__":
    main()