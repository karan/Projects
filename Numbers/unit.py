"""
Unit Converter (temp, currency, volume, mass and more) - Converts
various units between one another. The user enters the type of unit
being entered, the type of unit they want to convert to and then
the value. The program will then make the conversion.
"""

from __future__ import division
from urllib2 import urlopen
import json

# 1 (std unit) = these many units
MULTIPLIERS_TO_STD = {
    'length': {
        'cm': 0.01,
        'm': 1, # std unit
        'km': 1000,
        'mi': 1609.34,
        'ft': 0.3048
        },
    'temp': {
        'C': 1, # std unit
        'F': 33.8
        }
}

# These many units = 1 (std unit)
MULTIPLIERS_FROM_STD = {
    'length': {
        'cm': 100,
        'm': 1, # std unit
        'km': 0.001,
        'mi': 0.000621371,
        'ft': 3.28084
        },
    'temp': {
        'C': 1, # std unit
        'F': -17.2222
        }
}


def get_user_input(choice):
    units = ', '.join(MULTIPLIERS_TO_STD[choice].keys())
    source_unit = raw_input('\nEnter source unit (%s): ' % units)
    source_val = float(raw_input('How many %s\'s? ' % source_unit))
    convert_to = raw_input('Convert to? (%s): ' % units)
    return source_unit, source_val, convert_to

def get_currency(source_unit, source_val, convert_to):
    url = 'http://rate-exchange.appspot.com/currency?from=%s&to=%s&q=%s' % (
        source_unit, convert_to, str(source_val))
    content = urlopen(url).read()
    return json.loads(content)['v']

def main():
    print """Unit Converter
    1. Length
    2. Temperature
    3. Currency"""

    choice = int(raw_input('What do you want to convert: '))

    if choice == 1:
        source_unit, source_val, convert_to = get_user_input('length')
        print '%f%s = %f%s' % (source_val, source_unit,
                               source_val * \
                               MULTIPLIERS_TO_STD['length'][source_unit] * \
                               MULTIPLIERS_FROM_STD['length'][convert_to], \
                               convert_to)
    elif choice == 2:
        source_unit, source_val, convert_to = get_user_input('temp')
        if (source_unit, convert_to) == ('F', 'C'): # F -> C
            value = (source_val - 32) * (5/9)
        elif (source_unit, convert_to) == ('C', 'F'): # C -> F
            value = (source_val * (9/5)) + 32
        else:
            value = source_val
        print '%f%s = %f%s' % (source_val, source_unit,
                               value, convert_to)

    elif choice == 3:
        source_unit = raw_input('\nEnter source currency (eg USD, INR etc): ')
        source_val = float(raw_input('How many %s\'s? ' % source_unit))
        convert_to = raw_input('Convert to? (eg USD, INR etc): ')
        print '%f%s = %f%s' % (source_val, source_unit,
                               get_currency(source_unit, source_val, convert_to),
                               convert_to)
        
if __name__ == '__main__':
    main()
