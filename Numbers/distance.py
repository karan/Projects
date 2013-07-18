#!/usr/bin/env python

"""
Distance Between Two Cities - Calculates the distance between
two cities and allows the user to specify a unit of distance.
This program may require finding coordinates for the cities
like latitude and longitude.

Uses the Haversine formula
(http://www.movable-type.co.uk/scripts/latlong.html)

Dependencies:
geopy
    pip install geopy
"""

from geopy import geocoders # to find lat/lon for the city
import math

R = 6373 # km

city1 = raw_input('Enter city 1: ')
city2 = raw_input('Enter city 2: ')
unit = raw_input('Enter unit of distance (K = KM, M = MI): ').lower()

if unit in 'km':

    g = geocoders.GoogleV3()
    
    try:
        city1, (lat1, lon1) = g.geocode(city1)
        city2, (lat2, lon2) = g.geocode(city2)
    except:
        raise Exception('Unable to locate the citites. Check the city names.')
    
    # convert decimal locations to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # start haversne formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat/2) ** 2) + math.cos(lat1) * math.cos(lat2) * \
    (math.sin(dlon/2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    
    if unit == 'k':
        print 'Distance between %s and %s is %.04f km' % (city1, city2, d)
    else:
        print 'Distance between %s and %s is %.04f mi' % (city1, city2, d / 1.60934)
else:
    print 'Invalid unit input!'