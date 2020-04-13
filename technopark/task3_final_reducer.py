#!/usr/bin/python

import sys

previous_key = None
city_name = ""
product_name = []
avg_price = []
min_price = []

for line in sys.stdin:
    key, value = line.strip().split('\t')

    value = value.split(':')

    if key == previous_key:
        if value[0] == 'cityname':
            city_name = value[1]
        else:
            value = value[0].split(';')
            product_name.append(value[0])
            avg_price.append(value[1])
            min_price.append(value[2])

    else:
        if previous_key:
            for i in range(len(product_name)):
                print('{product};{avg_price};{min_price};{min_price_city}'
                  .format(product=product_name[i], avg_price=avg_price[i], min_price=min_price[i], min_price_city = city_name))

        previous_key = key
        city_name = ""
        product_name = []
        avg_price = []
        min_price = []

        if value[0] == 'cityname':
            city_name = value[1]
        else:
            value = value[0].split(';')
            product_name.append(value[0])
            avg_price.append(value[1])
            min_price.append(value[2])

if previous_key:
    for i in range(len(product_name)):
        print('{product};{avg_price};{min_price};{min_price_city}'
            .format(product=product_name[i], avg_price=avg_price[i], min_price=min_price[i], min_price_city = city_name))
