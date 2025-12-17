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
from tqdm import tqdm, trange
from collections import deque

DAY = "7"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (1, 21, 40),
    (2, 1615, 43560947406326),
]

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
        with open(input_path, "r") as f:
            for line in f:
                if line == "\n":
                    log("Empty line")
                else:
                    line = line.strip()
                    self.challenge.processLine(line)

    def getResults(self):
        """Return the results as a tuple (part1, part2)"""
        return (self.part1(), self.part2())

    def part1(self):
        return self.challenge.beamSplitCount

    def part2(self):
        return self.challenge.processPart2()


class Challenge:

    def __init__(self):
        self.beams = set()
        self.beamSplitCount = 0
        self.splitLocations = []
        self.map = []
        self.rowCount = 0
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        # log("\nProcessing line: ", line)
        self.map.append(line)
        for index, char in enumerate(line):
            if char == "S":
                self.beams.add(index)
            elif char == "^" and index in self.beams:
                self.splitLocations.append((self.rowCount, index, 0))
                self.beamSplitCount += 1
                self.beams.remove(index)
                self.beams.add(index + 1)
                self.beams.add(index - 1)
        self.rowCount += 1

        return

    def processPart2(self):
        # Find start
        start = None
        for index, char in enumerate(self.map[0]):
            if char == "S":
                start = (0, index)
                break

        log(f"Height: {self.rowCount}")
        log(f"Start: {start}")
        for line in self.map:
            log(f"Line: {line}")

        # for splitLocation in self.splitLocations:
        #     log(f"Split at {splitLocation}")

        for index, splitLocation in reversed(list(enumerate(self.splitLocations))):
            # log(f"{'='*60}")
            # log(f"Index: {index}")
            # log(f"Split at {splitLocation}")
            y, x, timelines = splitLocation
            # Check x-1, x + 1 for y -> self.rowCount

            currentTimelines = 0
            foundRight = False
            foundLeft = False
            for previousIndex in range(index + 1, len(self.splitLocations)):
                # log(f"{'~'*60}")
                # log(f"Previous Index: {previousIndex}")
                previousY, previousX, previousTimelines = self.splitLocations[
                    previousIndex
                ]
                if not foundLeft and previousX == x - 1:
                    currentTimelines += previousTimelines
                    foundLeft = True
                if not foundRight and previousX == x + 1:
                    currentTimelines += previousTimelines
                    foundRight = True

                if foundRight and foundLeft:
                    break

            if not foundRight:
                # log(f"No right found, adding 1 timeline")
                currentTimelines += 1
            if not foundLeft:
                # log(f"No left found, adding 1 timeline")
                currentTimelines += 1

            self.splitLocations[index] = (y, x, currentTimelines)
            # log(f"Updated Split at {y}, {x}, {currentTimelines}")

        for splitLocation in self.splitLocations:
            y, x, timelines = splitLocation
            if x == start[1]:
                return timelines
        return 1


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
