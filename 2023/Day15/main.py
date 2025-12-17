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

DAY = "15"
INPUT = "2"
INPUT_PATH = f"./day{DAY}/input{INPUT}.txt"

ROW_TO_CHECK = 2000000
# ROW_TO_CHECK = 10

TOP_RANGE = 4000000
# TOP_RANGE = 20
BOTTOM_RANGE = 0

FREQUENCY_MULTIPLIER = 4000000


def isNumber(var):
    return type(var) == int or type(var) == float


class System:
    def __init__(self):
        self.map = Map()
        self.blockedC = {}
        return

    def __str__(self):
        return f"System"

    def processLine(self, line):
        # print(line)
        splt = line.split(" ")
        sensorX = int(splt[2].split("=")[1][:-1])
        sensorY = int(splt[3].split("=")[1][:-1])
        beaconX = int(splt[8].split("=")[1][:-1])
        beaconY = int(splt[9].split("=")[1])
        # print(f"Sensonr ({sensorX}, {sensorY}), Beacon({beaconX}, {beaconY})")
        sensorC = (sensorX, sensorY)
        beaconC = (beaconX, beaconY)
        self.map.addSensor(sensorC, beaconC)
        return

    def process(self):
        print(self.map)
        # self.part1()
        self.part2()
        return

    def part1(self):
        print(self.map)
        blockedCoordinates = self.map.getBlockedRow(ROW_TO_CHECK)
        print(blockedCoordinates)
        print(f"Count: {len(blockedCoordinates)}")
        return

    def part2(self):

        # blocked = set()
        # for y in trange(TOP_RANGE + 1):
        #     blocked = self.map.getBlockedRow(y, False, 0, TOP_RANGE)
        #     if len(blocked) == TOP_RANGE:
        #         break
        # coordinates = (0, 0)
        # for x in trange(TOP_RANGE + 1):
        #     coordinates = (x, y)
        #     if not (coordinates in blocked):
        #         print(coordinates)
        #         break

        # # print(f"possibleLocations: {possibleLocations}")
        # # beacon = possibleLocations.pop()
        # frequency = coordinates[0] * FREQUENCY_MULTIPLIER + coordinates[1]
        # print(f"Frequency: {frequency}")
        beacon = self.map.findFreeBeacon()
        print(beacon)
        frequency = beacon[0] * FREQUENCY_MULTIPLIER + beacon[1]
        print(f"Frequency: {frequency}")

        return


class Map:
    def __init__(self):
        self.sensors = {}
        self.beacons = []
        return

    def __str__(self):
        retStr = "Map(\n"
        for sensor, value in self.sensors.items():
            retStr += f"  {sensor} -> {value}\n"
        retStr += ")"
        return retStr

    def addSensor(self, sensorC, beaconC):
        distance = calcManhattanDistance(sensorC, beaconC)
        self.sensors[sensorC] = distance
        self.beacons.append(beaconC)

    def getBlockedRow(
        self,
        row,
        removeBeacons=True,
        lowerRange=-FREQUENCY_MULTIPLIER,
        topRange=FREQUENCY_MULTIPLIER,
    ):
        blockedC = set()
        for sensor in self.sensors:
            self.getBlockedCoordinates(row, sensor, blockedC, lowerRange, topRange)
        if removeBeacons:
            blockedC = blockedC - set(self.beacons)
        return blockedC

    def getBlockedCoordinates(
        self,
        row,
        sensor,
        blockedC,
        lowerRange=-FREQUENCY_MULTIPLIER,
        topRange=FREQUENCY_MULTIPLIER,
    ):
        # blockedC = set()
        coverage = self.sensors[sensor]
        (x, y) = sensor
        distanceFromRow = abs(row - y)
        distanceLeft = coverage - distanceFromRow

        if distanceLeft < 0:
            return blockedC

        # print(
        #     f"Sensor({sensor}) SensorCoverage({coverage}) Distance({distanceFromRow}), DistanceLeft({distanceLeft})"
        # )
        right = min(x + distanceLeft, topRange)
        left = max(x - distanceLeft, lowerRange)
        for i in range(left, right + 1):
            blocked = (i, row)
            blockedC.add(blocked)
        return blockedC

    def findFreeBeacon(self):
        for sensor, distance in tqdm(self.sensors.items()):
            newManhattanDistance = distance + 1
            top = min(sensor[1] + newManhattanDistance, TOP_RANGE)
            bottom = max(sensor[1] - newManhattanDistance, BOTTOM_RANGE)
            for y in trange(bottom, top + 1):
                remainder = newManhattanDistance - abs(sensor[1] - y)
                rightX = sensor[0] + remainder
                right = (rightX, y)
                if (
                    rightX >= BOTTOM_RANGE
                    and rightX <= TOP_RANGE
                    and (not self.checkCoordinateCoverage(right))
                ):
                    return right
                if remainder != 0:
                    leftX = sensor[0] + remainder
                    left = (leftX, y)
                    if (
                        leftX >= BOTTOM_RANGE
                        and leftX <= TOP_RANGE
                        and (not self.checkCoordinateCoverage(left))
                    ):
                        pdb.set_trace()
                        return left

        return None

    def checkCoordinateCoverage(self, coordinate):
        for sensor, distance in self.sensors.items():
            if calcManhattanDistance(sensor, coordinate) <= distance:
                return True
        return False


def calcManhattanDistance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


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
