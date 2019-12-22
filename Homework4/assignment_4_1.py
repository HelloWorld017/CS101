"""Task 4.1.

Complete two functions: task4_1_1, task4_1_2.
Use csv library to read and parse CSV format.
https://docs.python.org/3/library/csv.html

"""

from csv import DictReader
from typing import Optional, Tuple

import csv, re

weather_dicts = []
header_regex = re.compile(r"((?:\([^\)]+\))|(?:[^\(\)a-zA-Z]+))")

with open('data/weather.csv', newline='') as csvfile:
    reader = DictReader(csvfile, delimiter=',', quotechar='|')
    types = {
        'Province': str,
        'City': str,
        'Year': int,
        'Month': int,
        'Day': int,
        'Weather': str,
        'MaxTemperature': float,
        'MinTemperature': float,
        'Rainfall': float,
        'Snowfall': float
    }
    
    for row in reader:
        weather_dict = {}
        
        for (key, value) in row.items():
            key = re.sub(header_regex, "", key)
            value = types[key](value)
            
            weather_dict[key] = value
        
        weather_dicts.append(weather_dict)


def task4_1_1(n: int) -> Optional[Tuple[str, str]]:
    """Task 4.1.1.

    Read the nth  row (exclude header) of the CSV and print its province and
    city, and return them via tuple.

    Args:
        n (int): row number of csv

    Returns:
        Tuple[str, str]: tuple consists of province_name: str and city_name: str
        None: if no records are found.

    """
    
    if n > len(weather_dicts) or n < 1:
        return None
    
    record = weather_dicts[n - 1]
    
    return record['Province'], record['City']


def task4_1_2(year: int, month: int,
              day: int) -> Optional[Tuple[float, float, float]]:
    """Task 4.1.2.

    Print temperatures and rainfall at Daejeon on input date.

    Args:
        year (int): Year
        month (int): Month
        day (int): Day

    Returns:
        Tuple[float, float, float]: tuple consists of
            max_temperature: float,
            min_temperature: float, and
            rainfall: float
        None: if no records are found.

    """
    
    for record in weather_dicts:
        if record['Year'] == year and \
            record['Month'] == month and \
            record['Day'] == day and \
            record['City'] == 'Daejeon':
            
            return record['MaxTemperature'], \
                record['MinTemperature'], \
                record['Rainfall']

print(len(weather_dicts))