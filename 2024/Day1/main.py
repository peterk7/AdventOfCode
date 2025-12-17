#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
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

DAY = "1"
INPUT = "2"
INPUT_PATH = f"./day{DAY}/input{INPUT}.txt"


class System:
    def __init__(self):
        self.challenge = Challenge()
        return

    def __str__(self):
        return f"System"

    def processLine(self, line):
        splitArray = line.split(" ")
        leftValue = int(splitArray[0])
        rightValue = int(splitArray[len(splitArray) - 1])

        self.challenge.inserPair(leftValue, rightValue)
        return

    def process(self):
        self.challenge.sortLists()
        self.part1()
        self.part2()

    def part1(self):
        print(f"Part 1 answer is: {self.challenge.evaluateDistances()}")

    def part2(self):
        print(f"Part 2 answer is: {self.challenge.evaluateSimilarityScore()}")


class Challenge:
    leftList = []
    rightList = []
    rightListCountMap = defaultdict(int)

    def __init__(self):
        return

    def __str__(self):
        return f""

    def inserPair(self, leftValue, rightValue):
        self.leftList.append(leftValue)
        self.rightList.append(rightValue)

    def sortLists(self):
        self.leftList.sort()
        self.rightList.sort()

    def evaluateDistances(self):
        totalDistance = 0

        # Assume arrays are the same length
        for i in range(len(self.leftList)):
            leftValue = self.leftList[i]
            rightValue = self.rightList[i]
            distance = self.calculateDistance(leftValue, rightValue)
            totalDistance += distance

        return totalDistance

    def calculateDistance(self, firstValue, secondValue):
        return abs(firstValue - secondValue)

    def evaluateSimilarityScore(self):
        totalSimilarityScore = 0

        self.preProcessRightList()

        for value in self.leftList:
            similarityScore = value * self.rightListCountMap[value]
            totalSimilarityScore += similarityScore

        return totalSimilarityScore

    def preProcessRightList(self):
        for value in self.rightList:
            self.rightListCountMap[value] += 1


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
