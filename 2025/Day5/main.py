#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
from collections import defaultdict

# import math
# import pdb
# import traceback
# import logging
# import json
# import functools
# from tqdm import tqdm, trange


# Set recursion limit as needed
# sys.setrecursionlimit(5000)
print(f"Recursion limit is: {sys.getrecursionlimit()}")

# Enable ANSI color codes on Windows
if os.name == "nt":
    os.system("")


# ANSI color codes
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


DAY = "5"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (1, 3, 14),
    (2, 661, 359526404143208),
]


def log(*args, **kwargs):
    """Log output only if DEV mode is enabled"""
    if DEV:
        print(*args, **kwargs)


class System:
    def __init__(self):
        self.challenge = Challenge()
        return

    def __str__(self):
        return f"System"

    def reset(self):
        """Reset the system state for a new test run"""
        self.challenge = Challenge()

    def processFile(self, input_path):
        """Read and process an input file"""
        processRanges = True
        with open(input_path, "r") as f:
            for line in f:
                if line == "\n":
                    log("Empty line")
                    processRanges = False
                else:
                    line = line.strip()
                    if processRanges:
                        self.challenge.processRange(line)
                    else:
                        self.challenge.processLine(line)

    def getResults(self):
        """Return the results as a tuple (part1, part2)"""
        return (self.part1(), self.part2())

    def part1(self):
        # log(f"Ranges: {self.challenge.ranges}")
        return self.challenge.freshCount

    def part2(self):
        self.challenge.countTotalFreshIdCount()
        return self.challenge.totalFreshIdCount


class Challenge:

    def __init__(self):
        self.ranges = []
        self.ids = []
        self.freshCount = 0
        self.totalFreshIdCount = 0
        return

    def __str__(self):
        return f""

    def processRange(self, line):
        # log(f"Processing range: {line}")
        start, end = line.split("-")
        start = int(start)
        end = int(end)
        startInRange, startIndex = self.inRanges(start)
        endInRange, endIndex = self.inRanges(end)

        if startInRange and endInRange and startIndex != endIndex:
            # Merge two ranges
            self.mergeRanges(startIndex, endIndex)
        elif startInRange and endInRange and startIndex == endIndex:
            # log(f"Range already exists: {line}")
            """Do nothing"""
        elif startInRange:
            # Add to start range
            self.ranges[startIndex] = (self.ranges[startIndex][0], end)
        elif endInRange:
            # Add to end range
            self.ranges[endIndex] = (start, self.ranges[endIndex][1])
        else:
            # Create new range
            newRange = (start, end)
            self.ranges.append(newRange)

            # New range may cover existing range fully
            for index, range in enumerate(self.ranges):
                if index == len(self.ranges) - 1:
                    break
                if self.rangesIntersect(newRange, range):
                    log(f"Ranges intersect: {newRange} and {range}")
                    self.mergeRanges(index, self.ranges.index(newRange))

        return

    def processLine(self, line):
        id = int(line)
        self.ids.append(id)
        if self.inRanges(id)[0]:
            self.freshCount += 1
        return

    def rangesIntersect(self, firstRange, secondRange):
        return (
            self.inRange(firstRange[0], secondRange)
            or self.inRange(firstRange[1], secondRange)
            or self.inRange(secondRange[0], firstRange)
            or self.inRange(secondRange[1], firstRange)
        )

    def inRange(self, id, range):
        return id >= range[0] and id <= range[1]

    def inRanges(self, id):
        for index, range in enumerate(self.ranges):
            if self.inRange(id, range):
                return True, index
        return False, None

    def mergeRanges(self, firstIndex, secondIndex):
        firstRange = self.ranges[firstIndex]
        secondRange = self.ranges[secondIndex]
        newRangeStart = min(firstRange[0], secondRange[0])
        newRangeEnd = max(firstRange[1], secondRange[1])
        newRange = (newRangeStart, newRangeEnd)
        self.ranges[firstIndex] = newRange
        self.ranges.pop(secondIndex)
        return

    def countTotalFreshIdCount(self):
        for range in self.ranges:
            self.totalFreshIdCount += range[1] - range[0] + 1
        return


def validatePart(part_name, result, expected):
    if expected is not None:
        passed = result == expected
        if passed:
            status = f"{Colors.GREEN}✓ PASS{Colors.RESET}"
            print(
                f"{part_name}: {Colors.GREEN}{result}{Colors.RESET} (expected {expected}) {status}"
            )
        else:
            status = f"{Colors.RED}✗ FAIL{Colors.RESET}"
            print(
                f"{part_name}: {Colors.RED}{result}{Colors.RESET} (expected {expected}) {status}"
            )
        return passed
    else:
        print(f"{part_name}: {Colors.YELLOW}{result}{Colors.RESET}")
        return True


def runTest(system, input_num, expected_part1=None, expected_part2=None):
    input_path = f"./day{DAY}/input{input_num}.txt"

    print(f"\n{'='*60}")
    print(f"Running test for Input {input_num}")
    print(f"{'='*60}")

    system.reset()
    system.processFile(input_path)
    part1_result, part2_result = system.getResults()

    part1_passed = validatePart("Part 1", part1_result, expected_part1)
    part2_passed = validatePart("Part 2", part2_result, expected_part2)

    return part1_passed and part2_passed


def main():
    print("Start")
    st = time.time()

    system = System()
    all_passed = True

    for input_num, expected_part1, expected_part2 in test_cases:
        passed = runTest(system, input_num, expected_part1, expected_part2)
        if not passed:
            all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}All tests PASSED ✓{Colors.RESET}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}Some tests FAILED ✗{Colors.RESET}")
    print(f"{'='*60}")

    elapsed_time = time.time() - st
    print("Execution time:", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print("End")


if __name__ == "__main__":
    main()


def isNumber(var):
    return type(var) == int or type(var) == float
