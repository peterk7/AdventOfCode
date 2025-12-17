#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
from collections import defaultdict

import math

# import pdb
# import traceback
# import logging
# import json
# import functools
from tqdm import tqdm, trange

DAY = "9"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (0, 35, 15),
    (3, 135, 52),
    (1, 50, 24),
    # 4661665300 is too high
    (2, 4745816424, 1351617690),
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
        return self.challenge.largestArea()

    def part2(self):
        return self.challenge.largestArea2()


class Challenge:

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.previousNodeIndex = None
        self.areas = defaultdict(list)
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        # log("\nProcessing line: ", line)
        (x, y) = line.split(",")
        node = (int(x), int(y))
        self.nodes.append(node)
        currentNodeIndex = len(self.nodes) - 1
        self.updateAreas(currentNodeIndex)
        if self.previousNodeIndex is not None:
            self.edges.append((self.previousNodeIndex, currentNodeIndex))
        self.previousNodeIndex = currentNodeIndex

        return

    def updateAreas(self, newNodeIndex):
        for i in range(0, len(self.nodes)):
            if i == newNodeIndex:
                continue
            area = self.calculateArea(self.nodes[newNodeIndex], self.nodes[i])
            self.areas[area].append((self.nodes[i], self.nodes[newNodeIndex]))
        return

    def calculateArea(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        distanceX = abs(x1 - x2) + 1
        distanceY = abs(y1 - y2) + 1
        area = distanceX * distanceY
        return area

    def largestArea(self):
        # log(f"Areas: {self.areas}")
        return max(self.areas.keys())

    def largestArea2(self):
        lastNodeIndex = len(self.nodes) - 1
        self.edges.append((0, lastNodeIndex))
        for area in tqdm(sorted(self.areas.keys(), reverse=True)):
            # log(f"Area: {area}")
            for box in self.areas[area]:
                # log(f"Checking Box: {box}")
                node1, node2 = box
                boxNodes = self.buildBoxNodes(node1, node2)
                # log(f"Box Nodes: {boxNodes}")
                boxCornersInsidePolygon = True
                for node in boxNodes:
                    if not self.insidePolygon(node):
                        boxCornersInsidePolygon = False
                        break

                if boxCornersInsidePolygon:
                    # log(f"Box Inside Polygon: {boxNodes}")
                    if self.validateBox(node1, node2):
                        # log(f"Box Validated: {boxNodes}")
                        return area
        return 0

    def buildBoxNodes(self, node1, node3):
        boxNodes = [
            node1,
            (node1[0], node3[1]),
            node3,
            (node3[0], node1[1]),
        ]
        return boxNodes

    def insidePolygon(self, point):
        # log(f"Nodes: {self.nodes}")
        # log(f"Point: {point}")
        # log(f"Vertecies: {self.edges}")
        counter = 0
        for edge in self.edges:
            if self.pointOnEdge(self.nodes, edge, point):
                # log(f"Point on edge: ({self.nodes[edge[0]]}, {self.nodes[edge[1]]})")
                return True
            if self.intersectsVertex(self.nodes, edge, point):
                # log(f"Intersects edge: ({self.nodes[edge[0]]}, {self.nodes[edge[1]]})")
                counter += 1

        return counter % 2 == 1

    def intersectsVertex(self, nodes, edge, point):
        xp, yp = point
        x1, y1 = nodes[edge[0]]
        x2, y2 = nodes[edge[1]]

        flatEdge = y1 == y2
        percentageOfYlength = (yp - y1) / (y2 - y1) if not flatEdge else 0
        XVertexLength = x2 - x1
        edgeXIntersection = x1 + percentageOfYlength * XVertexLength
        if (yp < y1) != (yp < y2) and xp <= edgeXIntersection:
            return True
        return False

    def pointOnEdge(self, nodes, edge, point):
        xp, yp = point
        x1, y1 = nodes[edge[0]]
        x2, y2 = nodes[edge[1]]

        crossProduct = (yp - y1) * (x2 - x1) - (xp - x1) * (y2 - y1)
        if crossProduct != 0:
            return False

        if xp < min(x1, x2) or xp > max(x1, x2):
            return False

        if yp < min(y1, y2) or yp > max(y1, y2):
            return False

        return True

    def validateBox(self, node1, node2):
        # log(
        #     f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Validating Box ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        # )
        # log(f"Node1: {node1}")
        # log(f"Node2: {node2}")

        for node in self.nodes:
            x, y = node
            x1, y1 = node1
            x2, y2 = node2
            minX = min(x1, x2)
            maxX = max(x1, x2)
            minY = min(y1, y2)
            maxY = max(y1, y2)
            if (minX < x < maxX) and (minY < y < maxY):
                return False

        innerBoxEdges = self.buildInnerBoxEdges(node1, node2)
        for edge in self.edges:
            node1Index, node2Index = edge
            edge = (self.nodes[node1Index], self.nodes[node2Index])
            for boxEdge in innerBoxEdges:
                # log(f"Checking edge: {edge} against box edge: {boxEdge}")
                # intersectionPoint = self.edgeIntersectsEdge(edge, boxEdge)
                # if (
                #     intersectionPoint
                #     and intersectionPoint != edge[0]
                #     and intersectionPoint != edge[1]
                # ):
                #     return False
                if self.edgeIntersectsEdge(edge, boxEdge):
                    # log(f"Edge intersects box edge: {edge} and {boxEdge}")
                    return False

        return True

    def edgeIntersectsEdge(self, edge1, edge2):
        x1, y1 = edge1[0]
        x2, y2 = edge1[1]
        x3, y3 = edge2[0]
        x4, y4 = edge2[1]
        denominator = (x4 - x3) * (y2 - y1) - (y4 - y3) * (x2 - x1)
        if denominator == 0:
            return False
        t = ((x1 - x3) * (y2 - y1) - (y1 - y3) * (x2 - x1)) / denominator
        u = ((x1 - x3) * (y4 - y3) - (y1 - y3) * (x4 - x3)) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            # intersectionPoint = (int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1)))
            # log(f"Intersection Point: {intersectionPoint}")
            # return intersectionPoint
            return True
        return False

    def buildInnerBoxEdges(self, node1, node2):
        minX = min(node1[0], node2[0])
        maxX = max(node1[0], node2[0])
        minY = min(node1[1], node2[1])
        maxY = max(node1[1], node2[1])

        minX += 1
        minY += 1
        maxX -= 1
        maxY -= 1

        if minX > maxX:
            return []
        if minY > maxY:
            return []

        return [
            ((minX, minY), (maxX, minY)),
            ((maxX, minY), (maxX, maxY)),
            ((maxX, maxY), (minX, maxY)),
            ((minX, maxY), (minX, minY)),
        ]


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
