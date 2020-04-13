#!/usr/bin/env python

import sys
import re

for line in sys.stdin:
    value = line.strip().split(';')

    #price
    if len(value) == 3:
        key = value[1]
        city = "city:" + value[0]
        price = "price:" + value[2].replace(',', '.')
        print ('{key}\t{city};{price}'.format(key=key, city=city, price=price))

    #product.csv
    elif len(value) == 2:
        key = value[1]
        name = "name:" + value[0]
        print('{key}\t{value}'.format(key=key, value=name))

    #product_for_stat.csv
    elif len(value) == 1:
        key = value[0]
        need = "need:" + '1'
        print('{key}\t{value}'.format(key=key, value=need))
