import datetime
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
import csv
from os import path
import sys

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
path_to_data = path.abspath(path.join(bundle_dir, 'saved_count.csv'))

print(path_to_data)


# We will start counting from this number
def read_saved_number(csvfilename):
    file_data = []
    with open(csvfilename, "r") as number_list:
        reader = csv.reader(number_list, delimiter=',', quotechar='"')
        for row in reader:
            if row:  # avoid blank lines
                columns = [row[0], row[1]]
                file_data.append(columns)
    return file_data


def save_current_number(csv_file_name, number, time):
    with open(csv_file_name, mode='a') as number_file:
        number_writer = csv.writer(number_file, delimiter=',', quotechar='"')
        number_writer.writerow([number, time])
    return


print(f'Starting up ......')

# read the last saved number
global the_number

# data = read_saved_number('saved_count.csv')
data = read_saved_number(path_to_data)

# grab last row of csv file
last_row = data[-1]
print(f'current number is {last_row[0]} and time was {last_row[1]}')
the_number = int(last_row[0])

# Set this to the starting date for counting
start_date = datetime(2020, 6, 4)


# Function to calculate the time delta between two dates
# Sure seems like there could be a easier way to do this
def getDuration(then, now=datetime.now(), interval="default"):
    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]
    now = datetime.now()
    duration = now - then  # For build-in functions
    duration_in_s = duration.total_seconds()

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 86400)  # Seconds in a day = 86400

    def hours(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 3600)  # Seconds in an hour = 3600

    def minutes(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 60)  # Seconds in a minute = 60

    def seconds(seconds=None):
        if seconds != None:
            return divmod(seconds, 1)
        return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "{} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]), int(d[0]), int(h[0]),
                                                                               int(m[0]), int(s[0]))

    # this returns a dictionary, we choose the key to return value
    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]


'''Calculate the time delta between two dates'''

# print(getDuration(then))  # E.g. Time between dates: 7 years, 208 days, 21 hours, 19 minutes and 15 seconds
# print(getDuration(then, now, 'years'))  # Prints duration in years
# print(getDuration(then, now, 'days'))  # days
# print(getDuration(then, now, 'hours'))  # hours
# time.sleep(2)
# print(getDuration(then, now, 'minutes'))  # minutes
# print(getDuration(then, now, 'seconds'))  # seconds

# Define the dictionary for audio files that will speak the numbers

 # kkkk
audioElements = {
    '1': 'Cyrus/one.wav', '2': 'Cyrus/two.wav', '3': 'Cyrus/three.wav', '4': 'Cyrus/four.wav', '5': 'Cyrus/five.wav',
    '6': 'Cyrus/six.wav', '7': 'Cyrus/seven.wav', '8': 'Cyrus/eight.wav', '9': 'Cyrus/nine.wav', '10': 'Cyrus/ten.wav',
    '11': 'Cyrus/eleven.wav', '12': 'Cyrus/twelve.wav', '13': 'Cyrus/thirteen.wav', '14': 'Cyrus/fourteen.wav',
    '15': 'Cyrus/fifteen.wav',
    '16': 'Cyrus/sixteen.wav', '17': 'Cyrus/seventeen.wav', '18': 'Cyrus/eighteen.wav', '19': 'Cyrus/nineteen.wav',
    '20': 'Cyrus/twenty.wav', '30': 'Cyrus/thirty.wav', '40': 'Cyrus/forty.wav', '50': 'Cyrus/fifty.wav',
    '60': 'Cyrus/sixty.wav', '70': 'Cyrus/seventy.wav', '80': 'Cyrus/eighty.wav', '90': 'Cyrus/ninety.wav',
    '100': 'Cyrus/hundred.wav', '1000': 'Cyrus/thousand.wav', '1000000': 'Cyrus/million.wav',
    '1000000000': 'Cyrus/billion.wav', '1000000000000': 'Cyrus/trillion.wav'
}


def split(num):
    # returns a hundreds, tens, teens and units from a three digit number
    # maybe this should be in the find_units function?

    teens = 0
    hundreds = num // 100
    tens = (num - (100 * hundreds)) // 10
    units = (num - (100 * hundreds) - (tens * 10))

    if tens < 2:
        teens = num - (100 * hundreds)
        tens = 0
        units = 0

    return hundreds, tens * 10, teens, units


def find_units(num):
    # given a number, return a tuple of values split by millions, billions, etc
    # as well as the hundreds, tens, teens and units using the split function
    # add an example here to better explain

    trillions = num // 1000000000000

    num -= trillions * 1000000000000
    billions = num // 1000000000

    num -= billions * 1000000000
    millions = num // 1000000

    num -= millions * 1000000
    thousands = num // 1000

    num -= thousands * 1000
    hundreds = num

    return split(trillions), split(billions), split(millions), split(thousands), split(hundreds)


def add_placeholders(x):
    # what exactly does this do again? Get rid of the blob variable name

    blob = find_units(x)
    trillions = list(blob[0])
    billions = list(blob[1])
    millions = list(blob[2])
    thousands = list(blob[3])
    hundreds = list(blob[4])

    if sum(trillions) != 0:
        if trillions[0] != 0:
            trillions.insert(1, 100)
        trillions.insert(5, 1000000000000)

    if sum(billions) != 0:
        if billions[0] != 0:
            billions.insert(1, 100)
        billions.insert(5, 1000000000)

    if sum(millions) != 0:
        if millions[0] != 0:
            millions.insert(1, 100)
        millions.insert(5, 1000000)

    if sum(thousands) != 0:
        if thousands[0] != 0:
            thousands.insert(1, 100)
        thousands.insert(5, 1000)

    if sum(hundreds) != 0:
        if hundreds[0] != 0:
            hundreds.insert(1, 100)
    whole_number = trillions + billions + millions + thousands + hundreds
    no_zeros = [i for i in whole_number if i != 0] # and this does what again?

    return no_zeros


def read_numbers(num):
    # build up a string of numbers to speak
    speak = 0
    for i in num:
        speak += AudioSegment.from_file(audioElements[str(i)], format='wav')
    play(speak)


if __name__ == "__main__":
    # global the_number
    while (True):
        print(f'current number is {the_number} and time was {datetime.now()}')
        read_numbers(add_placeholders(the_number))
        the_number += 1

        # only save every 10 numbers to cvs
        if the_number % 10 == 0:
            save_current_number(path_to_data, the_number, datetime.now())
