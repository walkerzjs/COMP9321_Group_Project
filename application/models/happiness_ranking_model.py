import requests


# year is str type
# year must be in [2015, 2016, 2017]
# returns the data dict which can be directly converted back to DataFrame.
def get_happiness_by_year(year):
    url = 'http://localhost:5000/api/world_happiness/' + year
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None


# Must change the url port to 5000 upon system integration!
# year is str type
# year must be in [1990, 1995, 2000, 2005, 2010-2016]
# returns a dict {'country_name': pm25_value, ...}
def get_pm25_by_year(year):
    url = 'http://localhost:50000/api/air_pollution/' + year
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

