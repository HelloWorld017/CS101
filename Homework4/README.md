## Homework 4

### Homework 4-1
> Parsing weather data

Load and process weather.csv file.

**1. Load `weather.csv` file into a list named `weather_tuples`. The list contains a series of tuples below.**  
a. Use csv library to read and parse CSV format.

b. https://docs.python.org/3/library/csv.html
(Province, City, Year, Month, Day, Weather, Max Temperature (°C), Min Temperature (°C), Rainfall (mm), Snowfall (cm))

c. `csv_load_example()` is given to help you!

**2. (Task 4.1.1) Read the nth row (exclude header) of the CSV and print its province and city, and return the result as a tuple.**  
a. Return None if no records are found

b. Tuple format: `Tuple[province_name: str, city_name: str]`

**3. (Task 4.1.2) Print temperatures and rainfall at Daejeon on input date.**  
a. Return None if no records are found

b. Input format: year: int month: int day: int

c. Output format: `Tuple[max_temperature: float, min_temperature: float, rainfall: float]`


----

### Homework 4-2
> Province/City/Weather object

Convert previously parsed data into a list named `weather_objects`. The list contains a series of `Province` objects.

A province object has its name field and a list of its city objects.

**Province**
* name: `str`
* cities: `List[City]`
\* cities sorted by its name.

A city object has its name field and a list of its weather objects.

**City**
* name: `str`
* cities: `List[Weather]`
\* weather sorted by its date


A weather object has its date, description, temperature_max, temperature_min, rainfall, and snowfall fields.  
a. You must use the datetime.date class to store the date of each weather.

b. datetime.date​: https://docs.python.org/3/library/datetime.html#date-objects

c. `datetime_example()` is given to help you!

**Weather**
* date: `datetime.date`
* description: `str`
* temperature_max: `float`
* temperature_min: `float`
* rainfall: `float`
* snowfall: `float`

----

### Homework 4-3
> Get average temperature

Convert previously parsed data into a list named `weather_objects`. The list contains a series of `Province` objects.

Finding the average temperature is a major concern of meteorology.
Complete the method get_average_temperature(Year, Month)​ in both​Province​ class and City class with the following requirements.

**1. It should return an average temperature in a given month of the province.**

**2. The average temperature should be Celsius and rounded to one decimal place, such as 29.8.**

**3. The monthly average temperature in a province is the arithmetic mean of the monthly average temperature of each city in the province.**  
Important: The result should be rounded to one decimal place. Also the monthly average temperature of city is also rounded.

**4. The monthly average temperature in a city is the arithmetic mean of daily average temperature in that month. The result should be rounded to one decimal place.**

**5. The daily average temperature in a city is the arithmetic mean of max temperature and min temperature in that day.**

**6. The rounding should be done just before returning the average temperature in each method.**

**7. It should return an error string ‘Please check the year and month.’ if the arguments are out of the scope. (ex, 2017, 8)**  
Hint: Implement get_average_temperature in City class first, and implement Province’s method latter.  
**Caution** The Elice grader strictly checks your error message such as “Please check the year and month.” even dot(“.”).

----

### Homework 4-4
> Get monsoon season

In Korea, rainfall over a few days is called monsoon season. Complete the method get_monsoon_season()​ in ​City ​class with the following requirements.

**1. In this assignment, monsoon season is at least five consecutive days whose description ​is ‘rainy’.**

**2. If there is more than one monsoon season, choose the longest one.**

**3. If there is more than one monsoon season of the same length, choose the earliest one.**

**4. It should return a tuple containing the start date and end date of the monsoon season. Those dates are ​date.datetime​ object.**

**5. It should return an error string ‘There is no monsoon season.’ if there is no monsoon season for the city.**
