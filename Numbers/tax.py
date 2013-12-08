#!/usr/bin/env python

TAXES = {
    'WA': 9.5,
    'CA': 7.5,
    'FL': 10.8,
    'OH': 7.8
}

state = raw_input('What\'s your state (WA / CA / FL / OH)?: ')
cost = float(raw_input('And the cost?: '))

tax = TAXES[state] / 100 * cost

print 'Cost: %.02f\nTax: %.02f\n----------\nTotal: %.02f' % (cost, tax, cost + tax)