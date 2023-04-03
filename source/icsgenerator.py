import random
from ics import Calendar, Event
from datetime import datetime, timedelta

# Define start and end times for the schedule
startDate = datetime(2023, 3, 11)  # Change the date as necessary
endDate = datetime(2023, 3, 17)  # Change the date as necessary

# Define duration of each lesson and breaks
lessonDuration = timedelta(minutes=45)
shortBreakDuration = timedelta(minutes=5)
longBreakDuration = timedelta(minutes=30)

# Define list of lessons
lessons = ['Math', 'Science', 'History', 'English', 'Art']

# Define number of calendars you want to generate
numberOfList = 2

# Define function to create events
def createEvent(startTime, lesson):
    event = Event()
    event.name = lesson
    event.begin = startTime
    event.end = startTime + lessonDuration
    return event

def generateCalendar():
    # Create calendar
    cal = Calendar()

    # Generate schedule for each day
    currentDate = startDate
    while currentDate <= endDate:
        # Define start and end times for the day's schedule
        startTime = currentDate.replace(hour=8, minute=0, second=0)
        endTime = currentDate.replace(hour=15, minute=0, second=0)

        # Schedule each lesson
        currentTime = startTime
        while currentTime < endTime:
            # Randomly generate number of lessons for the day
            numLessons = random.randint(1, 6)

            # Schedule each lesson
            for j in range(numLessons):
                # Randomly select lesson
                lesson = random.choice(lessons)

                # Check if previous lesson was the same, if so, insert a short break
                if j > 0 and lesson == previousLesson:
                    currentTime += shortBreakDuration

                # Create event for lesson and add to calendar
                event = createEvent(currentTime, lesson)
                cal.events.add(event)

                # Update current time for next lesson
                currentTime += lessonDuration

                # Store previous lesson
                previousLesson = lesson

                # Insert short break
                if j < numLessons - 1:
                    currentTime += shortBreakDuration

            # Insert long break
            currentTime += longBreakDuration

        # Update current date to next day
        currentDate += timedelta(days=1)
    return cal

if __name__ == '__main__':
    for i in range(numberOfList):
        # Write calendar to file
        with open(f'schedule_{i}.ics', 'w') as f:
            f.write(str(generateCalendar()))