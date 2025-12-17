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


DAY = "4"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (1, 13, 43),
    (2, 1560, 9609),
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
        self.challenge.processPart1()
        return self.challenge.accessableRollCount

    def part2(self):
        self.challenge.processPart2()
        return self.challenge.recursiveAccessableRollCount


class Challenge:

    def __init__(self):
        self.grid = []
        self.rows = 0
        self.cols = 0
        self.accessableRollCount = 0
        self.recursiveAccessableRollCount = 0
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        row = []
        for index, char in enumerate(line):
            if char == "@":
                row.append(1)
            elif char == ".":
                row.append(0)
        self.grid.append(row)
        self.rows += 1
        self.cols = len(row)
        return

    def processPart1(self):
        self.accessableRollCount, _ = self.processGrid()
        return

    def processPart2(self):
        while True:
            rollsToRemove, removableIndexes = self.processGrid()
            if rollsToRemove == 0:
                break

            for index in removableIndexes:
                self.grid[index[0]][index[1]] = 0
            self.recursiveAccessableRollCount += rollsToRemove
        return

    def processGrid(self):
        # for row in self.grid:
        #     log(f"Row: {row}")
        # log(f"Rows: {self.rows}")
        # log(f"Cols: {self.cols}")

        removableIndexes = []
        accessableRollCount = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 0:
                    continue

                count = 0
                if i - 1 >= 0 and j - 1 >= 0 and self.grid[i - 1][j - 1] == 1:
                    count += 1
                if i - 1 >= 0 and self.grid[i - 1][j] == 1:
                    count += 1
                if i - 1 >= 0 and j + 1 < self.cols and self.grid[i - 1][j + 1] == 1:
                    count += 1
                if j - 1 >= 0 and self.grid[i][j - 1] == 1:
                    count += 1
                if j + 1 < self.cols and self.grid[i][j + 1] == 1:
                    count += 1
                if i + 1 < self.rows and j - 1 >= 0 and self.grid[i + 1][j - 1] == 1:
                    count += 1
                if i + 1 < self.rows and self.grid[i + 1][j] == 1:
                    count += 1
                if (
                    i + 1 < self.rows
                    and j + 1 < self.cols
                    and self.grid[i + 1][j + 1] == 1
                ):
                    count += 1

                if count < 4:
                    removableIndexes.append((i, j))
                    accessableRollCount += 1
        return accessableRollCount, removableIndexes


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
