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

from pyvis.network import Network

# import traceback
# import logging
import json
# import functools

DAY = "11"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    (1, 5, 0),
    (3, 0, 2),
    (2, 472, 526811953334940),
    (4, 0, 3)
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
        return self.challenge.processPart1()

    def part2(self):
        return self.challenge.processPart2()


class Challenge:

    def __init__(self):
        self.graph = Graph()
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        split = line.split(" ")
        originNode = split[0][:-1]
        destinationNodes = split[1:]
        # log(f"OriginNode: {originNode}")
        # log(f"destinationNodes: {destinationNodes}")
        for destinationNode in destinationNodes:
            self.graph.addEdge(originNode, destinationNode)

        return

    def processPart1(self):
        return len(self.findPaths("you", "out"))

    def findPaths(self, startNode, endNode, excludeNodes=[]):
        queue = deque([(startNode, 0, [startNode])])

        paths = []
        while queue:
            currentNode, currentDistance, currentPath = queue.popleft()
            # log(f"CurrentNode: {currentNode}, CurrentDistance: {currentDistance}, CurrentPath: {currentPath}")
            # if currentNode in visited:
            #     continue
            if currentNode in excludeNodes:
                continue
            if currentNode == endNode:
                paths.append(currentPath)
                continue
            # visited.add(currentNode)
            for neighbor in self.graph.edges[currentNode]:
                queue.append((neighbor, currentDistance + 1, currentPath + [neighbor]))

        return paths

    def processPart2(self):
        # self.graph.show()
        # return 0
        # log(f"Graph: {self.graph}")
        
        pathsSvrToFFT = self.findPathsDFS("svr", "fft", ["dac"], {})
        # log(f"\nPathsSvrToFFT: {pprint.pformat(pathsSvrToFFT)}")

        pathsFFTToDAC = self.findPathsDFS("fft", "dac", ["svr"], {})
        # log(f"\nPathsFFTToDAC: {pprint.pformat(pathsFFTToDAC)}")

        pathsDACToOut = self.findPathsDFS("dac", "out", ["svr", "fft"], {})
        # log(f"\nPathsDACToOut: {pprint.pformat(pathsDACToOut)}")

        return pathsSvrToFFT * pathsFFTToDAC * pathsDACToOut

        # svr -> aaa -      -> eee -> fft
        #     -> bbb ^      ^
        #     -> ccc -> ddd |
        # DAC -> FFT is empty, therefore this flow is 0 by default.
        # pathsSvrToDAC = self.findPaths("svr", "dac", ["fft"])
        # log(f"\nPathsSvrToDAC: {pprint.pformat(pathsSvrToDAC)}")

        # pathsDACToFFT = self.findPaths("dac", "fft", ["svr"])
        # log(f"\nPathsDACToFFT: {pprint.pformat(pathsDACToFFT)}")

        # pathsFFTToOut = self.findPaths("fft", "out", ["svr", "dac"])
        # log(f"\nPathsFFTToOut: {pprint.pformat(pathsFFTToOut)}")

        
        return 0

    def findPathsDFS(self, startNode, endNode, excludeNodes=[], visited={}):
        
        if startNode == endNode:
            # log(f"Found end node: {startNode}")
            return 1
        if startNode in excludeNodes:
            # log(f"Excluded node: {startNode}")
            return 0
        
        if startNode in visited:
            # log(f"Visited node: {startNode}")
            return visited[startNode]
        paths = 0
        for neighbor in self.graph.edges[startNode]:
            paths += self.findPathsDFS(neighbor, endNode, excludeNodes, visited)
        visited[startNode] = paths
        return paths


class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        # self.net = Network(notebook=True, bgcolor="#222222", font_color="white", height="750px", width="100%")
        self.net = Network(directed=True, select_menu=True)
        # Enable hierarchical layout
        options = {
            "layout": {
                "hierarchical": {
                    "enabled": True,
                    "levelSeparation": 150,
                    "nodeSpacing": 100,
                    "treeSpacing": 200,
                    "blockShifting": True,
                    "edgeMinimization": True,
                    "parentCentralization": True,
                    "direction": "UD",
                    "sortMethod": "directed"
                }
            }
        }

        self.net.set_options(json.dumps(options))


    def __str__(self):
        return f"Graph(nodes: {self.nodes}, edges: {pprint.pformat(self.edges)})"
        

    def show(self):
        # self.net.show_buttons(filter_=['physics'])
        self.net.show("network.html", notebook=False)
        return

    def addEdge(self, originNode, destinationNode):

        self.nodes.add(originNode)
        self.nodes.add(destinationNode)
        self.edges[originNode].append(destinationNode)

        self.net.add_node(originNode, label=originNode)
        self.net.add_node(destinationNode, label=destinationNode)
        self.net.add_edge(originNode, destinationNode)



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
