import datetime
import re
from csv import DictReader
from datetime import date
from typing import List


class Weather:
    """Weather class."""

    date: datetime.date
    description: str
    temperature_max: float
    temperature_min: float
    rainfall: float
    snowfall: float

    def __init__(self, date: datetime.date, description: str,
                 temperature_max: float, temperature_min: float,
                 rainfall: float, snowfall: float):
        """
        Initialize new Weather

        Args:
            date (datetime.date): date of weather
            description (str): description of weather
            temperature_max: max temperature of day
            temperature_min: min temperature of day
            rainfall: rainfall of day
            snowfall: snowfall of day

        """
        
        self.date = date
        self.description = description
        self.temperature_max = temperature_max
        self.temperature_min = temperature_min
        self.rainfall = rainfall
        self.snowfall = snowfall

    @property
    def temperature_avg(self):
        return (self.temperature_max + self.temperature_min) / 2

    def __repr__(self):
        return "<Weather %s>" % self.date


class City:
    """City class."""

    name: str
    weathers: List[Weather]

    def __init__(self, city_name: str):
        """
        Initialize new City named <city_name>.

        Args:
            city_name(str): name of city

        """
        self.name = city_name
        self.weathers = []
	
    def get_average_temperature(self, year, month):
        """
        Return an average temperature in a given month of the City.
        Details are in the document.
        
        Input arguments:
            year (int)
            month (int)
        Return:
            average temperature (float)
        """
        weather_picked = [
            weather.temperature_avg
            for weather in self.weathers
            if weather.date.year == year and weather.date.month == month
        ]
        
        if len(weather_picked) == 0:
            return "Please check the year and month."
		
        return round(sum(weather_picked) / len(weather_picked), 1)

    def __repr__(self):
        return "<City %s>" % self.name


class Province:
    """Province class."""

    name: str
    cities: List[City]

    def __init__(self, province_name: str):
        """
        Initialize new Province named <province_name>.

        Args:
            province_name(str): name of province

        """
        self.name = province_name
        self.cities = []
	
    def get_average_temperature(self, year, month):
        """
        Return an average temperature in a given month of the Province.
        Details are in the document.
        
        Input arguments:
            year (int)
            month (int)
        Return:
            average temperature (float)
        """
        avg_temps = [
            city.get_average_temperature(year, month)
            for city in self.cities
        ]
        
        for avg_temp in avg_temps:
            if type(avg_temp) == str:
                return "Please check the year and month."
        
        return round(sum(avg_temps) / len(avg_temps), 1)

    def __repr__(self):
        return "<Province %s>" % self.name


def task4_2_1() -> List[Province]:
    """Task 4.2.1.

    Read the CSV file and return list of parsed Province objects

    Returns:
        List[Province]: a list of parsed Province objects

    """
    header_regex = re.compile(r"((?:\([^\)]+\))|(?:[^\(\)a-zA-Z]+))")
    weather_dicts = []
    csvfile = open('data/weather.csv', newline='')
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
    
    provinces = {}
    cities = {}
    
    for row in reader:
        weather_dict = {}
        
        for (key, value) in row.items():
            key = re.sub(header_regex, "", key)
            value = types[key](value)
            
            weather_dict[key] = value
        
        weather_dicts.append(weather_dict)

    for w in weather_dicts:
        province_str = w['Province']
        city_str = w['City']
        
        if province_str not in provinces:
            provinces[province_str] = Province(province_str)
        
        province = provinces[province_str]
        
        if (province_str, city_str) not in cities:
            cities[province_str, city_str] = City(city_str)
            province.cities.append(cities[province_str, city_str])
        
        city = cities[province_str, city_str]
        
        city.weathers.append(Weather(
            date = date(w['Year'], w['Month'], w['Day']),
            description = w['Weather'],
            temperature_max = w['MaxTemperature'],
            temperature_min = w['MinTemperature'],
            rainfall = w['Rainfall'],
            snowfall = w['Snowfall']
        ))
    
    csvfile.close()
    
    provinces = list(provinces.values())
    
    # This code has very bad time complexity
    # But botherness >>>>>> desire to optimize is always true
    # ¯\_(ツ)_/¯
    
    for province in provinces:
        province.cities.sort(key=lambda city: city.name)
        
        for city in province.cities:
            city.weathers.sort(key=lambda weather: weather.date)
    
    return provinces

"""
provinces = task4_2_1()
print(provinces)
print(provinces[0].get_average_temperature(2018, 12))
print(provinces[0].cities[0].get_average_temperature(2018, 12))
print(provinces[0].get_average_temperature(2017, 12))
print(provinces[0].cities[0].get_average_temperature(2017, 12))
"""
