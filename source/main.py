from ics import Calendar
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta
import argparse

# Initialize the ArgumentParser
parser = argparse.ArgumentParser(description='Find common free times in ICS calendars.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Add the path argument
parser.add_argument('path', type=str, nargs='+', help='the paths for the ICS files')

# Add the length argument
parser.add_argument('length', type=int, help='the length in minutes')

# Add the startTime argument
parser.add_argument('--startTime', type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S'), help='the start time in YYYY-MM-DD HH:MM:SS format')

# Add the endTime argument
parser.add_argument('--endTime', type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S'), help='the end time in YYYY-MM-DD HH:MM:SS format')

# Parse the arguments
args = parser.parse_args()

# Access the path, length, startTime, and endTime arguments
paths = args.path
length = args.length
startTime = args.startTime
endTime = args.endTime

def getFreeSlots(calFiles, startTime, endTime):
    # Initialize list of busy time slots for each calendar
    calendarDict = {}
    for calFile in calFiles:
        # Load calendar file
        with open(calFile) as file:
            calData = file.read()

        # Parse calendar data
        newCalendar = Calendar(calData)

        # Find earliest start time among all events
        earliestStart = min([event.begin for event in newCalendar.events])

        # Use earliest start time as starting point for search
        if startTime < earliestStart.datetime:
            startTime = earliestStart.datetime

        # Initialize list of busy time slots
        busySlots = []
        for event in newCalendar.events:
            # Get start and end times of event
            start = event.begin
            end = event.end

            # Convert times to UTC timezone
            startUtc = start.astimezone(pytz.utc)
            endUtc = end.astimezone(pytz.utc)

            # Check if event overlaps with search range
            if startUtc < endTime and endUtc > startTime:
                # Add busy slot to list
                busySlots.append((startUtc, endUtc))

        # Sort the events by their start times
        busySlots.sort()

        # Create a list of free time slots
        freeTimes = []
        lastEndTime = startTime
        for event in busySlots:
            if event[0] > lastEndTime:
                freeTimes.append((lastEndTime, event[0]))
            lastEndTime = max(lastEndTime, event[1])
        if endTime > lastEndTime:
            freeTimes.append((lastEndTime, endTime))
        
        # Filter the free time slots to only include those that fall within the desired time range
        freeTimes = [(start, end) for start, end in freeTimes if start.time() >= startTime.time() and end.time() <= endTime.time()]
        calendarDict[calFile] = freeTimes

    return calendarDict

# Define a function to break down a datetime range into 30-minute intervals
def getFreeTimesIntervals(freeTimesDict):
    intervals = []
    for calendar in freeTimesDict:
        for time in freeTimesDict[calendar]:
            startTime = time[0]
            endTime = time[1]
            currentTime = startTime
            while currentTime < endTime:
                intervals.append((currentTime, currentTime + relativedelta(minutes=5)))
                currentTime += relativedelta(minutes=5)
    return intervals

# Example usage
freeTimesDict = getFreeSlots(args.path, args.startTime, args.endTime)

freeTimesIntervals = getFreeTimesIntervals(freeTimesDict)

# Count the occurrences of each interval
counts = {}
for interval in freeTimesIntervals:
    if interval in counts:
        counts[interval] += 1
    else:
        counts[interval] = 1

# Filter out the intervals that occur for every calendar
result = [interval for interval in freeTimesIntervals if counts[interval] == len(args.path)]

print(result)  