import datetime
from datetime import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from pydub import AudioSegment
from pydub.playback import play

# We will start counting from this number
the_number = 1

# Set this to the starting date for counting
start_date = datetime(2020, 6, 1)

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

audioElements = {
    '1': 'Cyrus/one.wav', '2': 'Cyrus/two.wav', '3': 'Cyrus/three.wav', '4': 'Cyrus/four.wav', '5': 'Cyrus/five.wav',
    '6': 'Cyrus/six.wav', '7': 'Cyrus/seven.wav', '8': 'Cyrus/eight.wav', '9': 'Cyrus/nine.wav', '10': 'Cyrus/ten.wav',
    '11': 'Cyrus/eleven.wav', '12': 'Cyrus/twelve.wav', '13': 'Cyrus/thirteen.wav', '14': 'Cyrus/fourteen.wav',
    '15': 'Cyrus/fifteen.wav',
    '16': 'Cyrus/sixteen.wav', '17': 'Cyrus/seventeen.wav', '18': 'Cyrus/eighteen.wav', '19': 'Cyrus/nineteen.wav',
    '20': 'Cyrus/twenty.wav', '30': 'Cyrus/thirty.wav', '40': 'Cyrus/fourty.wav', '50': 'Cyrus/fifty.wav',
    '60': 'Cyrus/sixty.wav', '70': 'Cyrus/seventy.wav', '80': 'Cyrus/eighty.wav', '90': 'Cyrus/ninety.wav',
    '100': 'Cyrus/hundred.wav', '1000': 'Cyrus/thousand.wav', '1000000': 'Cyrus/million.wav',
    '1000000000': 'Cyrus/billion.wav', '1000000000000': 'Cyrus/trillion.wav'
}


def split(num):
    # returns a hundreds, tens, teens and units from a three digit number

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
    no_zeros = [i for i in whole_number if i != 0]

    return no_zeros


def read_numbers(num):
    ### build up a string of numbers to speak
    speak = 0
    for i in num:
        speak += AudioSegment.from_file(audioElements[str(i)], format='wav')
    play(speak)


class MyW(FloatLayout):
    global the_number

    def my_callback(self, dt):
        global the_number

        print("read the number here")
        read_numbers(add_placeholders(the_number))
        the_number += 1
        self.ids.label1.text = str(format(the_number, ","))
        # Update the total elapsed time, how to split this to not show zero values?
        self.ids.label3.text = str(getDuration(start_date, interval="seconds"))

    def on_touch_down(self, touch):
        self.ids.label1.text = str(format(the_number, ","))         # set the counting number
        Clock.schedule_interval(self.my_callback, 0.5)              # Document this better 1 is too long
        if touch.is_double_tap:
            self.ids.label1.text = ""
            Clock.unschedule(self.my_callback)
            exit()


class Layout(App):
    def build(self):
        return MyW()


if __name__ == "__main__":
    Layout().run()
