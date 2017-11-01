#!/usr/bin/env python3.6

import csv
import matplotlib
import numpy as np
import sys
import time

matplotlib.use('GTKAgg')

from matplotlib import pyplot as plt
from number_line import AnimatedNumberLine



EXAMPLE_FILE = 'example.csv'

def print_usage():
    print(f'{sys.argv[0]} [file_name]')

def main(target):
    numline = AnimatedNumberLine(radius=1, tickmarks=10)
    numline.graph('x=0')

    with open(target, newline='') as f:
        gen = csv.reader(f)
        option1, option2 = next(gen)

        total = 0
        n = 0
        for row in gen:
            label, value, weight = row
            value, weight = float(value), float(weight)
            total += value * weight
            n += 1
            final = total / n
            print(final)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        target = EXAMPLE_FILE
    elif len(sys.argv) == 2:
        target = sys.argv[1]
    else:
        print_usage()
        sys.exit()
    main(target)
