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


DAY = "6"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (1, 4277556, 3263827),
    (2, 5784380717354, 7996218225744),
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
        with open(input_path, "r") as f:
            for line in f:
                if line == "\n":
                    log("Empty line")
                else:
                    # line = line.strip()
                    self.challenge.processLine(line)

    def getResults(self):
        """Return the results as a tuple (part1, part2)"""
        return (self.part1(), self.part2())

    def part1(self):
        return self.challenge.calculatePart1()

    def part2(self):
        return self.challenge.calculatePart2()


class Challenge:

    def __init__(self):
        self.numberRows = []
        self.operators = []
        self.fullNumberRows = []
        self.fullOperators = []
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        log(f"Processing line: {line[:-1]}")
        if line[-1] == "\n":
            line = line[:-1]
        if line[0] == "*" or line[0] == "+":
            self.processOperators(line)
        else:
            self.processNumbers(line)
        return

    def processOperators(self, line):
        self.fullOperators = line

        split = line.strip().split(" ")
        for operator in split:
            if operator == "":
                continue
            self.operators.append(operator)
        return

    def processNumbers(self, line):
        self.fullNumberRows.append(line)

        split = line.strip().split(" ")
        numbers = []
        for number in split:
            if number == "":
                continue
            numbers.append(int(number))
        self.numberRows.append(numbers)
        return

    def calculatePart1(self):
        result = 0
        for i in range(len(self.operators)):
            if self.operators[i] == "*":
                columnResult = 1
                for numberRow in self.numberRows:
                    columnResult *= numberRow[i]
                result += columnResult
            elif self.operators[i] == "+":
                columnResult = 0
                for numberRow in self.numberRows:
                    columnResult += numberRow[i]
                result += columnResult
        return result

    def calculatePart2(self):
        result = 0
        operator = "+"
        currentOperationResult = 0
        for i in range(len(self.fullOperators)):
            if self.fullOperators[i] == "*":
                operator = "*"
                result += currentOperationResult
                currentOperationResult = 1
            elif self.fullOperators[i] == "+":
                operator = "+"
                result += currentOperationResult
                currentOperationResult = 0

            number = 0
            numberFound = False
            for fullRow in self.fullNumberRows:
                if fullRow[i] == " ":
                    continue

                numberFound = True
                digit = int(fullRow[i])
                number = number * 10 + digit

            if numberFound and operator == "*":
                currentOperationResult *= number
            elif numberFound and operator == "+":
                currentOperationResult += number

        if currentOperationResult != 0:
            result += currentOperationResult
        # log(f"Final result: {result}")
        return result


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
