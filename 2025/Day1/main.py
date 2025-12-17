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


DAY = "1"


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
        # print("\nProcessing line: ", line)
        rotation = line[0]
        amount = int(line[1:])
        self.challenge.processLine(rotation, amount)
        return

    def processFile(self, input_path):
        """Read and process an input file"""
        with open(input_path, "r") as f:
            for line in f:
                if line == "\n":
                    print("Empty line")
                else:
                    line = line.strip()
                    self.processLine(line)

    def getResults(self):
        """Return the results as a tuple (part1, part2)"""
        return (self.part1(), self.part2())

    def part1(self):
        return self.challenge.zeroStops

    def part2(self):
        return self.challenge.zeroCount


"""
left (toward lower numbers) or to the right (toward higher numbers)
The dial starts by pointing at 50.
0 - 99
The actual password is the number of times the dial is left pointing at 0 after any rotation in the sequence.
"""

LEFT = "L"
RIGHT = "R"


class Challenge:

    def __init__(self):
        self.dial = 50
        self.zeroStops = 0
        self.zeroCount = 0
        return

    def __str__(self):
        return f""

    def processLine(self, rotation, amount):
        # print(f"Dial initial: {self.dial}")
        fullRotations = amount // 100
        self.zeroCount += fullRotations
        remainder = amount % 100

        if rotation == LEFT:
            if self.dial == 0:
                self.zeroCount -= 1
            self.dial -= remainder
            if self.dial == 0:
                self.zeroCount += 1
        if rotation == RIGHT:
            self.dial += remainder

        # print(f"Dial before normalization: {self.dial}")
        if self.dial < 0 or self.dial > 99:
            self.zeroCount += 1
            self.dial = self.dial % 100

        if self.dial == 0:
            self.zeroStops += 1

        # print(f"Dial after: {self.dial}")
        # print(f"Zero count: {self.zeroCount}")
        # print(f"Zero stops: {self.zeroStops}")


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

    # Define test cases: (input_num, expected_part1, expected_part2)
    test_cases = [
        (0, 3, 6),
        (
            1,
            1135,
            6558,
        ),
    ]

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
