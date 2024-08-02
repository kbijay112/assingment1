#!/usr/bin/env python3

'''
OPS445 Assignment 1 - Fall 2023
Program: assignment1.py 
The python code in this file is original work written by
bijay khatiwada. No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Author: kbijay
Description: This script calculates various date-related functions such as
             determining the next day, validating dates, and counting weekend days
             between two dates. It includes error handling and usage instructions.
'''

import sys
from datetime import datetime, timedelta

def day_of_week(date: str) -> str:
    """
    Determine the day of the week for a given date using the Tomohiko Sakamoto algorithm.
    The date format should be DD/MM/YYYY.
    """
    day, month, year = (int(x) for x in date.split('/'))
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1
    num = (year + year//4 - year//100 + year//400 + offset[month] + day) % 7
    return days[num]

def leap_year(year: int) -> bool:
    """
    Check if a year is a leap year.
    A year is a leap year if it is divisible by 4,
    but not divisible by 100, except if it is also divisible by 400.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def mon_max(month:int, year:int) -> int:
    """
    Return the maximum number of days in a given month of a specific year.
    Adjusts for leap years in February.
    """
    month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                   7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    
    # Check for leap year and adjust February's days
    if month == 2 and leap_year(year):
        return 29
    return month_days.get(month, 0)

def after(date: str) -> str: 
    """
    Return the date for the next day given a date in DD/MM/YYYY format.
    """
    day, mon, year = (int(x) for x in date.split('/'))
    day += 1  # Move to the next day

    leap_flag = False
    if year % 4 == 0:
        leap_flag = True
    if year % 100 == 0:
        leap_flag = False
    if year % 400 == 0:
        leap_flag = True
    
    mon_dict= {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
               7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    
    # Adjust for leap year if February
    if mon == 2 and leap_flag:
        mon_max = 29
    else:
        mon_max = mon_dict[mon]
    
    # If day exceeds the month's maximum days, move to the next month
    if day > mon_max:
        mon += 1
        if mon > 12:
            year += 1
            mon = 1
        day = 1  # Reset to the first day of the next month
    
    return f"{day:02}/{mon:02}/{year}"

def before(date: str) -> str:
    """
    Returns the previous day's date in DD/MM/YYYY format.
    """
    day, mon, year = (int(x) for x in date.split('/'))
    day -= 1  # Move to the previous day
    
    if day == 0:
        mon -= 1
        if mon == 0:
            year -= 1
            mon = 12
        day = mon_max(mon, year)  # Set day to the last day of the previous month
    
    return f"{day:02}/{mon:02}/{year}"

def usage():
    """
    Print a usage message to the user and exit.
    """
    print("Usage: " + str(sys.argv[0]) + " DD/MM/YYYY NN")
    sys.exit()

def valid_date(date: str) -> bool:
    """
    Check if the given date string is valid.
    Date format should be DD/MM/YYYY.
    """
    try:
        day, month, year = (int(x) for x in date.split('/'))
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= mon_max(month, year)):
            return False
        datetime(year, month, day)  # This will raise ValueError if the date is invalid
        return True
    except ValueError:
        return False

def day_iter(start_date: str, num: int) -> str:
    """
    Iterates from the start date by num days to return the end date in DD/MM/YYYY format.
    """
    start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
    end_date_obj = start_date_obj + timedelta(days=num)
    return end_date_obj.strftime("%d/%m/%Y")

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        usage()
    
    start_date = sys.argv[1]
    num_days = sys.argv[2]
    
    # Validate the start date
    if not valid_date(start_date):
        usage()
    
    # Validate and convert the number of days
    try:
        num_days = int(num_days)
    except ValueError:
        usage()
    
    # Calculate the end date
    end_date = day_iter(start_date, num_days)
    print(f'The end date is {day_of_week(end_date)}, {end_date}.')