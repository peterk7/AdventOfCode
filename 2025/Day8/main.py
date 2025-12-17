#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
from collections import defaultdict

import math

import pdb

# import traceback
# import logging
# import json
# import functools
from tqdm import tqdm, trange

DAY = "8"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    ((1, 10), 40, 25272),
    ((2, 1000), 84968, 8663467782),
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
        self.challenge = Challenge(0)
        return

    def __str__(self):
        return f"System"

    def reset(self, numberOfConnections):
        """Reset the system state for a new test run"""
        self.challenge = Challenge(numberOfConnections)

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
        return self.challenge.processPart1()

    def part2(self):
        return self.challenge.processPart2()


class Challenge:

    def __init__(self, numberOfConnections):
        self.nodes = []
        self.numberOfConnections = numberOfConnections
        self.distances = {}
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        # log("\nProcessing line: ", line)
        (x, y, z) = line.split(",")
        node = (int(x), int(y), int(z))
        self.nodes.append(node)
        self.updateDistances(len(self.nodes) - 1)
        return

    def updateDistances(self, newNodeIndex):
        for i in range(0, len(self.nodes)):
            if i == newNodeIndex:
                continue
            distance = self.calculateDistance(self.nodes[newNodeIndex], self.nodes[i])
            self.distances[distance] = (i, newNodeIndex)
        return

    def calculateDistance(self, node1, node2):
        return math.sqrt(
            (node1[0] - node2[0]) ** 2
            + (node1[1] - node2[1]) ** 2
            + (node1[2] - node2[2]) ** 2
        )

    def processPart1(self):
        vertices = []
        # Generate the X vertecies we need to connect
        verteciesCount = 0
        for distance in sorted(self.distances.keys()):
            if verteciesCount >= self.numberOfConnections:
                break
            # log(f"Distance: {distance} ({self.distances[distance]})")
            vertices.append(self.distances[distance])
            verteciesCount += 1

        # print(f"Vertices: {vertices}")
        # Calculate islands (Union find)
        islands = self.generateIslands(vertices)
        largestIslands = self.findLargestIslandSizes(islands, 3)
        # log(f"Largest islands: {largestIslands}")
        product = 1
        for islandSize in largestIslands:
            product *= islandSize
        return product

    def generateIslands(self, vertices):
        # Initialize parents
        parents = {}
        for i in range(len(self.nodes)):
            parents[i] = i

        # Connect vertices
        for vertex in vertices:
            parentRight = self.findParent(parents, vertex[0])
            parentLeft = self.findParent(parents, vertex[1])
            if parentRight != parentLeft:
                self.union(parents, parentRight, parentLeft)

        # log(f"Parents: {parents}")
        islands = defaultdict(list)
        for i in range(len(self.nodes)):
            islands[self.findParent(parents, i)].append(i)
        # log(f"Islands: {islands}")
        return islands

    def findParent(self, parents, i):
        if parents[i] != i:
            return self.findParent(parents, parents[i])
        return parents[i]

    def union(self, parents, i, j):
        parents[j] = i
        return parents

    def findLargestIslandSizes(self, islands, numberOfIslands):
        islandSizes = []
        for island in islands.values():
            islandSizes.append(len(island))
        islandSizes.sort(reverse=True)
        return islandSizes[:numberOfIslands]

    def processPart2(self):
        parents = {}
        for i in range(len(self.nodes)):
            parents[i] = i

        vertices = []
        currentVertex = None
        islands = defaultdict(list)
        for i in range(len(self.nodes)):
            islands[i] = [i]
        for distance in tqdm(sorted(self.distances.keys())):
            # log(f"~" * 60)
            currentVertex = self.distances[distance]
            vertices.append(currentVertex)
            parentRight = self.findParent(parents, currentVertex[0])
            parentLeft = self.findParent(parents, currentVertex[1])
            # log(f"Current vertex: {currentVertex}")
            # log(f"Parent right: {parentRight}")
            # log(f"Parent left: {parentLeft}")
            if parentRight != parentLeft:
                # log(f"Unioning {parentRight} and {parentLeft}")
                self.union(parents, parentRight, parentLeft)
                islands[parentRight] = islands[parentRight] + islands[parentLeft]
                del islands[parentLeft]
                # log(f"Parents: {parents}")
                # log(f"Islands: {islands}")

            if len(islands) == 1:
                break
        log(f"Current vertex: {currentVertex}")
        log(f"Vertices: {vertices}")
        log(f"Parents: {parents}")
        log(f"Islands: {islands}")

        node1 = self.nodes[currentVertex[0]]
        node2 = self.nodes[currentVertex[1]]

        return node1[0] * node2[0]


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


def runTest(system, input_args, expected_part1=None, expected_part2=None):
    (input_num, numberOfConnections) = input_args
    input_path = f"./day{DAY}/input{input_num}.txt"

    print(f"\n{'='*60}")
    print(f"Running test for Input {input_num} with {numberOfConnections} connections")
    print(f"{'='*60}")

    system.reset(numberOfConnections)
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

    for input_args, expected_part1, expected_part2 in test_cases:
        passed = runTest(system, input_args, expected_part1, expected_part2)
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
