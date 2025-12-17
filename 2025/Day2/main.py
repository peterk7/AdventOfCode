#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
from collections import defaultdict
from primes import primesLowerThan

# import pdb
# import traceback
# import logging
# import json
# import functools
from tqdm import tqdm, trange


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


DAY = "2"
DEV = False  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (0, 0, 111 + 1111111 + 123123123),
    (1, 1227775554, 4174379265),
    (2, 16793817782, 27469417404),  # Slow
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
        log("\nProcessing line: ", line)
        ranges = line.split(",")
        for range in tqdm(ranges):
            if range == "":
                continue
            start, end = range.split("-")
            self.challenge.processRange(int(start), int(end))

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
        log(f"Invalid IDs: {self.challenge.invalidIds}")
        return self.challenge.invalidIdsSum

    def part2(self):
        log(f"Invalid IDs parts: {self.challenge.invalidIdsParts}")
        return self.challenge.invalidIdsPartsSum


CHECKED_IDS = {}


class Challenge:

    def __init__(self):
        self.invalidIds = []
        self.invalidIdsSum = 0
        self.invalidIdsParts = []
        self.invalidIdsPartsSum = 0
        return

    def __str__(self):
        return f""

    def processRange(self, start, end):
        for id in tqdm(range(start, end + 1)):
            isInvalid, isInvalidParts = self.isInvalidId(str(id))
            if isInvalid:
                self.invalidIds.append(id)
                self.invalidIdsSum += id
            if isInvalidParts:
                self.invalidIdsParts.append(id)
                self.invalidIdsPartsSum += id
        return

    def isInvalidId(self, id):
        log(f"\nChecking ID: {id}")
        if id in CHECKED_IDS:
            return CHECKED_IDS[id]

        # Empty ID is invalid
        if id == "":
            return True, True

        length = len(id)
        if self.isValidIdParts(id, 2):
            log(f"Invalid ID, 2 parts: {id}")
            CHECKED_IDS[id] = (True, True)
            return True, True

        primesLowerThanLength = primesLowerThan(length + 1)
        for prime in primesLowerThanLength:
            if self.isValidIdParts(id, prime):
                log(f"Invalid ID, {prime} parts: {id}")
                CHECKED_IDS[id] = (False, True)
                return False, True

        CHECKED_IDS[id] = (False, False)
        return False, False

    def isValidIdParts(self, id, numParts):
        if len(id) % numParts != 0:
            return False

        length = len(id)
        partLength = length // numParts
        log(f"Length: {length}")
        log(f"Part length: {partLength}")
        parts = []
        while len(id) > 0:
            parts.append(id[:partLength])
            id = id[partLength:]
        log(f"Parts: {parts}")

        for i in range(numParts):
            if parts[i] != parts[0]:
                return False
        return True


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
