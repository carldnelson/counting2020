import csv
from datetime import date, time, datetime


def import_csv(csvfilename):
    file_data = []
    with open(csvfilename, "r") as number_list:
        reader = csv.reader(number_list, delimiter=',', quotechar='"')
        for row in reader:
            if row:  # avoid blank lines
                columns = [row[0], row[1]]
                file_data.append(columns)
    return file_data


data = import_csv('saved_count.csv')  # read the last saved number
last_row = data[-1]  # grab last row of csv file
print(f'current number is {last_row[0]} and time was {last_row[1]}')

# number = int(last_row[0])
# print(f'number is {number}')  # just some debugging checking here, make sure it's a number


# for counting computer
# On program start, read the last number
# Load number as start number
# Every 100 numbers save the number and datetime to the number file


# How to write number to the data file

def export_csv(csv_file_name, number, time):
    with open(csv_file_name, mode='a') as number_file:
        number_writer = csv.writer(number_file, delimiter=',', quotechar='"')
        number_writer.writerow([number, time])
    return


number = 56
time = datetime.now()
export_csv('saved_count.csv', number, time)
