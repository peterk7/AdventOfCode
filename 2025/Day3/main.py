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


DAY = "3"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (
        0,
        33 + 34 + 34 + 43 + 31,
        111111113123 + 111111111334 + 111111111314 + 111111113143 + 311111111111,
    ),
    (1, 98 + 89 + 78 + 92, 3121910778619),
    (2, 16854, 167526011932478),
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

    def processLine(self, line):
        # log("\nProcessing line: ", line)
        self.challenge.processLine(line)
        return

    def processFile(self, input_path):
        """Read and process an input file"""
        with open(input_path, "r") as f:
            for line in f:
                if line == "\n":
                    log("Empty line")
                else:
                    line = line.strip()
                    self.processLine(line)

    def getResults(self):
        """Return the results as a tuple (part1, part2)"""
        return (self.part1(), self.part2())

    def part1(self):
        return self.challenge.voltSum

    def part2(self):
        return self.challenge.highVoltsSum


class Challenge:

    def __init__(self):
        self.volts = []
        self.voltSum = 0
        self.highVolts = []
        self.highVoltsSum = 0
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        voltTempContainer = line[0:12]
        # log(f"Volt temp container: {voltTempContainer}")

        # Part 1
        firstIndex = 0
        secondIndex = 1
        for index, digit in enumerate(line):
            if index == 0 or index == 1:
                continue

            if int(line[secondIndex]) > int(line[firstIndex]):
                firstIndex = secondIndex
                secondIndex = index
            elif int(line[secondIndex]) < int(digit):
                secondIndex = index

        volt = int(line[firstIndex]) * 10 + int(line[secondIndex])
        self.volts.append(volt)
        self.voltSum += volt

        # Part 2
        for index in range(12, len(line)):
            nextDigit = int(line[index])
            popIndex = -1
            for i in range(0, 11):
                if int(voltTempContainer[i]) < int(voltTempContainer[i + 1]):
                    popIndex = i
                    break
            if popIndex == -1 and int(voltTempContainer[-1]) < nextDigit:
                popIndex = 11

            if popIndex != -1:
                voltTempContainer = (
                    voltTempContainer[:popIndex] + voltTempContainer[popIndex + 1 :]
                )
                voltTempContainer += str(nextDigit)
        log(f"Volt temp container: {voltTempContainer}")
        highVolt = int(voltTempContainer)
        self.highVolts.append(highVolt)
        self.highVoltsSum += highVolt
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
