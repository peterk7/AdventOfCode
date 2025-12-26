#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
import math
import pdb
import pprint

from collections import defaultdict, deque
from tqdm import tqdm, trange

# import traceback
# import logging
# import json
# import functools
import copy

DAY = "12"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (3, 1, None),
    (1, 2, None),
    (2, 517, None),
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
                line = line.strip()
                self.challenge.processLine(line)

    def getResults(self):
        """Return the results as a tuple (part1, part2)"""
        return (self.part1(), self.part2())

    def part1(self):
        return self.challenge.processPart1()

    def part2(self):
        return self.challenge.processPart2()


NUMBER_OF_PRESENTS = 6
PRESENT_SHAPE_WIDTH = 3
PRESENT_SHAPE_HEIGHT = 3


class Challenge:
    def __init__(self):
        self.presentId = -1
        self.presentShape = []
        self.lineIndex = 0
        self.presentCollection = PresentCollection()
        self.regions = []
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        # log("\nProcessing line: ", line)

        if line == "":
            if self.presentId != -1:
                self.presentCollection.addPresent(
                    Present(self.presentId, self.presentShape)
                )
                self.presentId = -1
                self.presentShape = []
                self.lineIndex = 0
            return

        if self.presentCollection.count() < NUMBER_OF_PRESENTS:
            if self.lineIndex == 0:
                # ID line
                split = line.split(":")
                self.presentId = int(split[0])
                self.lineIndex += 1
                return
            elif self.lineIndex > 0:
                # Shape line
                self.presentShape.append(list(line))
                self.lineIndex += 1
                return
        else:
            # Process maps
            mapSize, presents = line.split(":")
            width, height = mapSize.split("x")
            width = int(width)
            height = int(height)
            expectedPresentCounts = presents.strip().split(" ")
            expectedPresents = {}
            for index, presentCount in enumerate(expectedPresentCounts):
                presentId = index
                count = int(presentCount)
                expectedPresents[presentId] = count
            self.regions.append(Region(width, height, expectedPresents))
        return

    def processPart1(self):
        # log(self.presentCollection)
        count = 0
        for region in self.regions:
            if region.preValidateAreas(self.presentCollection):
                # log(f"Region {region} is valid")
                count += 1
                # This is not a real test, its just a pre-validation ... but it works for the input 2 it seems ^^"
                # It does not work for input 1 though ...
            # else:
            # log(f"Region {region} is invalid")
            # log(region)
            # log(f"\n")

            # regionState = RegionState(
            #     region.width, region.height, region.expectedPresents.copy()
            # )
            # self.fillRegion(regionState)
        return count

    def fillRegion(self, regionState):

        for present in self.presentCollection.presents:
            if regionState.needToPlacePresent(present.id):
                log(f"Checking present: {present}")
                regionStateCopy = regionState.copy()
                for variation in present.variations:
                    regionStateCopy.placePresent(present.id, variation)

        return

    def processPart2(self):
        return 0


class Present:
    def __init__(self, id, shape):
        self.id = id
        self.shape = shape
        self.area = 0
        self.calculateArea()
        self.shapeWidth = PRESENT_SHAPE_WIDTH
        self.shapeHeight = PRESENT_SHAPE_HEIGHT

        self.variations = []
        self.calculateVariations()

    def __str__(self):
        return f"Present {self.id} with shape {self.shape} and area {self.area}"

    def calculateArea(self):
        for row in self.shape:
            for cell in row:
                if cell == "#":
                    self.area += 1
        return

    def calculateVariations(self):
        # Rotate = 4 options
        # Flit + rotate = 4 options
        # log(f"Calculating variations for present {self.id}, shape: {self.shape}")
        tempShape = self.shape.copy()
        for i in range(4):
            self.variations.append(tempShape)
            tempShape = self.rotate(tempShape)

        tempShape = self.flip(tempShape)
        for i in range(4):
            self.variations.append(tempShape)
            tempShape = self.rotate(tempShape)

        # log(f"Variations: {pprint.pformat(self.variations)}")
        return

    def rotate(self, shape):
        newShape = [["."] * self.shapeWidth for _ in range(self.shapeHeight)]
        for i in range(self.shapeHeight):
            for j in range(self.shapeWidth):
                newShape[i][j] = shape[j][self.shapeHeight - i - 1]
        return newShape

    def flip(self, shape):
        newShape = [["."] * self.shapeWidth for _ in range(self.shapeHeight)]
        for i in range(self.shapeHeight):
            for j in range(self.shapeWidth):
                newShape[i][j] = shape[self.shapeHeight - i - 1][j]
        return newShape


class PresentCollection:
    def __init__(self):
        self.presents = {}
        return

    def __str__(self):
        ret = f"PresentCollection with {len(self.presents)} presents"
        for presentID, present in self.presents.items():
            ret += f"\n{presentID}: {present}"
        return ret

    def addPresent(self, present):
        self.presents[(present.id)] = present
        return

    def count(self):
        return len(self.presents)


class Region:
    def __init__(self, width, height, expectedPresents):
        self.width = width
        self.height = height
        self.expectedPresents = expectedPresents
        return

    def __str__(self):
        ret = f"Region with width {self.width} and height {self.height}"
        for present in self.expectedPresents:
            ret += f"\n{present} count: {self.expectedPresents[present]}"
        return ret

    def preValidateAreas(self, presentCollection):
        currentRegionArea = self.width * self.height
        neededPresentArea = 0
        for presentID, present in presentCollection.presents.items():
            neededPresentArea += present.area * self.expectedPresents[presentID]
        return currentRegionArea >= neededPresentArea


class RegionState:
    def __init__(self, width, height, expectedPresents, state=None):
        self.width = width
        self.height = height
        self.state = [["."] * width for _ in range(height)] if state is None else state
        self.expectedPresents = expectedPresents
        return

    def __str__(self):
        ret = f"RegionState with width {self.width} and height {self.height}"
        for row in self.state:
            ret += f"\n{row}"
        return ret

    def copy(self):
        return RegionState(
            self.width,
            self.height,
            self.expectedPresents.copy(),
            copy.deepcopy(self.state),
        )

    def needToPlacePresent(self, presentID):
        return self.expectedPresents[presentID] > 0


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
