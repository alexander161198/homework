#!/usr/bin/env python

import sys

for line in sys.stdin:
    value, key = line.strip().split(';', 1)
    value = "cityname:" + value

    print ('{key}\t{value}'.format(key=key, value=value))