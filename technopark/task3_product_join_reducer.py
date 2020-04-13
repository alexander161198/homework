#!/usr/bin/env python

import sys

previous_key = None
name = ""
need = 0
input_value = []
value = []
city_price = {}

for line in sys.stdin:
    key, input_value = line.strip().split('\t')

    value = []
    input_value = input_value.split(';', 1)
    for i in input_value:
        value.extend(i.split(':', 1))

    if key == previous_key:
        if value[0] == 'need':
            need = 1
        if value[0] == 'name':
            name = value[1]
        if value[0] == 'city':
            if value[3]:
                city_price[int(value[1])] = float(value[3])

    else:
        if previous_key and need:
            if len(city_price) > 0:
                avg_price = round(sum(city_price.values())/len(city_price), 2)
                min_price = (min(zip((city_price[k] for k in city_price),
                                    (i for i in city_price))))
                print('{min_price_city}\t{name};{avg_price};{min_price}'
                    .format(name=name, avg_price=avg_price, min_price=min_price[0], min_price_city=min_price[1]))
        previous_key = key
        name = ""
        need = 0
        city_price = {}
        avg_price = 0
        min_price = [0, 0]
        if value[0] == 'need':
            need = 1
        if value[0] == 'name':
            name = value[1]
        if value[0] == 'city':
            if value[3]:
                city_price[int(value[1])] = float(value[3])

if previous_key and need:
    if len(city_price) > 0:
        avg_price = round(sum(city_price.values())/len(city_price), 2)
        min_price = (min(zip((city_price[k] for k in city_price),
                            (i for i in city_price))))
        print('{min_price_city}\t{name};{avg_price};{min_price}'
            .format(name=name, avg_price=avg_price, min_price=min_price[0], min_price_city=min_price[1]))