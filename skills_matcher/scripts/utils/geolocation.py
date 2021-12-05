#function for finding country by the city

#!pip install geopy
from geopy.geocoders import Nominatim

def geo(loc):
    geolocator = Nominatim(user_agent = "geoapiExercises")
    location = geolocator.geocode(loc,language="en")
    return str(location[:][0]).split(",")[-1].strip()
