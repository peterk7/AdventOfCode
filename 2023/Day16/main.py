#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import math
import sys
import traceback
import logging
import json
import functools
from tqdm import tqdm, trange
import time

# sys.setrecursionlimit(5000)
print(sys.getrecursionlimit())

DAY = "16"
INPUT = "1"
INPUT_PATH = f"./day{DAY}/input{INPUT}.txt"

# STEPS = 30 # Part 1
STEPS = 26 # Part 2
TIME_TO_OPEN = 1
START_NODE_ID = "AA"


class System:
    def __init__(self):
        self.graph = Graph()
        return

    def __str__(self):
        return f"System"

    def processLine(self, line):
        # print(line)
        splt = line.split(" ")
        # print(splt)
        name = splt[1]
        flowRate = int(splt[4].split("=")[1][:-1])
        connections = splt[9:]
        connections = list(map(lambda c: c[:2], connections))
        # print(f"Name: {name}, flowRate: {flowRate}, connections: {connections}")
        self.graph.addNode(name, flowRate, connections)
        return

    def process(self):
        print(self.graph)
        # self.part1()
        self.part2()

    def part1(self):
        print("Total Pressure Released: ", self.graph.findBestFlowRate())
        return

    def part2(self):
        return


class Graph:
    def __init__(self):
        self.nodes = {}
        self.brokenNodes = []
        return

    def __str__(self):
        retStr = f"Graph(\n"
        for node in self.nodes.values():
            retStr += f"  {node}\n"
        retStr += ")\n"
        return retStr

    def addNode(self, name, flowRate, connections):
        node = Node(name, flowRate, connections)
        self.nodes[name] = node

        if flowRate == 0:
            self.brokenNodes.append(name)

    def findBestFlowRate(self):
        return self.bestFlowRateDFS(STEPS, START_NODE_ID, [])

    def bestFlowRateDFS(self, steps_left, current_node, opened):
        if steps_left <= 0:
            return 0

        # Shortest route to un-opened valve
        dist = self.findShortestRoutes(current_node)

        # Filter out opened and broken valves
        for id in self.brokenNodes:
            del dist[id]
        for id in opened:
            del dist[id]

        best_release_pressure = 0
        for id in dist.keys():
            opened_copy = opened.copy()
            opened_copy.append(id)
            steps_left_after_open = steps_left - dist[id] - TIME_TO_OPEN
            if steps_left_after_open < 0:
                continue
            node_release_pressure = steps_left_after_open * self.nodes[id].flowRate
            remaining_flow_rate = self.bestFlowRateDFS(steps_left_after_open, id, opened_copy)
            if best_release_pressure < node_release_pressure + remaining_flow_rate:
                best_release_pressure = node_release_pressure + remaining_flow_rate

        return best_release_pressure

    def findShortestRoutes(self, source):
        dist = {}
        # prev = {}
        queue = []

        for node in self.nodes.values():
            dist[node.name] = math.inf
            # prev[node.name] = None
            queue.append(node)
        dist[source] = 0

        while len(queue) > 0:
            u = min(queue, key=lambda value: dist[value.name])
            queue.remove(u)

            neighbors = [self.nodes[node_id] for node_id in u.connections if self.nodes[node_id] in queue]
            for neighbor in neighbors:
                # Wight of all edges is 1
                alt = dist[u.name] + 1
                if alt < dist[neighbor.name]:
                    dist[neighbor.name] = alt
                    # prev[neighbor.name] = u

        return dist




    # def checkNode(self, node, stepsLeft, turnedOn, memory):
    #     # pair = (node.name, stepsLeft, frozenset(turnedOn))

    #     # if pair in memory:
    #     #     return memory[pair]

    #     currentOn = node.name in turnedOn

    #     if stepsLeft <= 0:
    #         # memory[pair] = 0
    #         return 0

    #     # Step
    #     jumpFirstRates = {}
    #     jumpAfterRates = {}
    #     if stepsLeft > 1:
    #         for connection in node.connections:
    #             conNode = self.nodes[connection]
    #             print(f"Check ({node.name}) -> ({connection})")
    #             updatedSteps = stepsLeft - 1
    #             connectionRate = self.checkNode(
    #                 conNode, updatedSteps, turnedOn.copy(), memory
    #             )
    #             jumpFirstRates[(connection, updatedSteps)] = connectionRate

    #             if not currentOn and updatedSteps > 0:
    #                 updatedSteps -= 1
    #                 connectionRate = self.checkNode(
    #                     conNode, updatedSteps, turnedOn.copy(), memory
    #                 )
    #                 jumpAfterRates[(connection, updatedSteps)] = connectionRate

    #     # Turn on
    #     flowRate = node.flowRate * stepsLeft
    #     if not currentOn and stepsLeft == 1:
    #         print("Last node, turning on.")
    #         return flowRate

    #     bestFlow = 0
    #     for value in jumpFirstRates.values():
    #         if value > bestFlow:
    #             bestFlow = value
    #     for value in jumpAfterRates.values():
    #         flowToCheck = value + flowRate
    #         if flowToCheck > bestFlow:
    #             turnedOn.add(node.name)
    #             bestFlow = flowToCheck

    #     pair = (node.name, stepsLeft, frozenset(turnedOn))
    #     print(pair, bestFlow)
    #     # memory[pair] = bestFlow
    #     return bestFlow


class Node:
    def __init__(self, name, flowRate, connections=[]):
        self.name = name
        self.flowRate = flowRate
        self.connections = connections
        return

    def __str__(self):
        return f"Node(name: {self.name}, flowRate: {self.flowRate}, connections: {self.connections})"


def main():
    print("Start")
    st = time.time()

    f = open(INPUT_PATH, "r")

    s = System()

    for line in f:
        if line == "\n":
            print("Empty line")
        else:
            line = line.strip()
            s.processLine(line)

    s.process()

    elapsed_time = time.time() - st
    print("Execution time:", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print("End")


if __name__ == "__main__":
    main()


def isNumber(var):
    return type(var) == int or type(var) == float
