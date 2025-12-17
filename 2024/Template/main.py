#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys

# import pdb
# import math
# import traceback
# import logging
# import json
# import functools
# from tqdm import tqdm, trange

# Set recursion limit as needed
# sys.setrecursionlimit(5000)
print(f"Recursion limit is: {sys.getrecursionlimit()}")

DAY = "0"
INPUT = "1"
INPUT_PATH = f"./day{DAY}/input{INPUT}.txt"


class System:
    def __init__(self):
        return

    def __str__(self):
        return f"System"

    def processLine(self, line):
        print(line)
        return

    def process(self):
        self.part1()
        self.part2()

    def part1(self):
        return

    def part2(self):
        return


class Day12:
    def __init__(self):
        return

    def __str__(self):
        return f""


def main():
    print("Start")
    st = time.time()

    f = open(INPUT_PATH, "r")

    s = System()

    for line in f:
        if line == "\n":
            print("Empty line")
        else:
            line = line.strip()
            s.processLine(line)

    s.process()

    elapsed_time = time.time() - st
    print("Execution time:", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print("End")


if __name__ == "__main__":
    main()


def isNumber(var):
    return type(var) == int or type(var) == float
