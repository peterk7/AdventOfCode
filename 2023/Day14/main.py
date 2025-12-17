#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import math
import sys
import traceback
import logging
import json
import functools

# sys.setrecursionlimit(5000)
print(sys.getrecursionlimit())

DAY = "14"
INPUT = "2"
INPUT_PATH = f"./day{DAY}/input{INPUT}.txt"

SEPERATOR = " -> "
START_HORIZONTAL = 500
START_VERTICAL = 0
FLOOR_BUFFER = 5
SAND_START = (START_HORIZONTAL, START_VERTICAL)

WALL = "#"
SAND = "O"
AIR = "*"


def isNumber(var):
    return type(var) == int or type(var) == float


def getCoordinates(coordinatesStr):
    (x, y) = coordinatesStr.split(",")
    return [int(x), int(y)]


def generateLine(start, finish):
    lineCoordinates = []
    if start[0] == finish[0]:
        # Using Y coordinate
        initial = min(start[1], finish[1])
        last = max(start[1], finish[1]) + 1
        for y in range(initial, last):
            lineCoordinates.append((start[0], y))
    else:
        # Using X coordinate
        initial = min(start[0], finish[0])
        last = max(start[0], finish[0]) + 1
        for x in range(initial, last):
            lineCoordinates.append((x, start[1]))
    return lineCoordinates


class System:
    def __init__(self):
        self.map = Map()
        return

    def __str__(self):
        return f"System"

    def processLine(self, line):
        # print(line)
        coordinatesArr = line.split(SEPERATOR)
        start = getCoordinates(coordinatesArr[0])
        for coordinatesStr in coordinatesArr[1:]:
            coordinates = getCoordinates(coordinatesStr)
            # print(f"X: {coordinates[0]}, Y:{coordinates[1]}")
            # Process coordinates
            generatedLine = generateLine(start, coordinates)
            for lineCord in generatedLine:
                self.map.addWall(lineCord)
            start = coordinates

        # print(self.map)
        return

    def process(self):
        # self.part1()
        self.part2()

    def part1(self):
        self.countSands()
        return

    def part2(self):
        floorHeight = self.map.height + 2
        right = max(self.map.right, START_HORIZONTAL + floorHeight + FLOOR_BUFFER)
        left = min(self.map.left, START_HORIZONTAL - floorHeight - FLOOR_BUFFER)
        generatedLine = generateLine((left, floorHeight), (right, floorHeight))
        for lineCord in generatedLine:
            self.map.addWall(lineCord)
        self.countSands()
        return

    def countSands(self):
        # print(self.map)
        count = 0
        while self.map.addSand(SAND_START) == 1:
            count += 1
            # print(f"Count {count}")
            # print(self.map)

        print(self.map)
        print(f"Added {count} grains of sand.")
        return


class Map:
    def __init__(self):
        self.walls = {}
        self.sand = {}
        self.height = START_VERTICAL
        self.right = START_HORIZONTAL
        self.left = START_HORIZONTAL
        return

    def __str__(self):
        retStr = f"Height: {self.height}, Left: {self.left}, Right: {self.right}\n"
        for y in range(self.height + 1):
            for x in range(self.left, self.right + 1):
                coordinates = (x, y)
                char = AIR
                if coordinates in self.walls:
                    char = WALL
                elif coordinates in self.sand:
                    char = SAND
                retStr += char
            retStr += "\n"
        return retStr

    def addWall(self, wallCoordinates):
        self.walls[wallCoordinates] = True
        if wallCoordinates[1] > self.height:
            self.height = wallCoordinates[1]
        if wallCoordinates[0] > self.right:
            self.right = wallCoordinates[0]
        if wallCoordinates[0] < self.left:
            self.left = wallCoordinates[0]

    def addSand(self, coordinates):
        if coordinates in self.sand or coordinates in self.walls:
            # Sand already occupies the space
            return 0

        if (
            coordinates[1] > self.height
            or coordinates[0] > self.right
            or coordinates[0] < self.left
        ):
            # Out of bounds!
            return -1

        # Try to add 1 down
        newCoordinates = (coordinates[0], coordinates[1] + 1)
        check = self.addSand(newCoordinates)
        if check != 0:
            return check

        # Try to add 1 down and to the left
        newCoordinates = (coordinates[0] - 1, coordinates[1] + 1)
        check = self.addSand(newCoordinates)
        if check != 0:
            return check

        # Try to add 1 down and to the right
        newCoordinates = (coordinates[0] + 1, coordinates[1] + 1)
        check = self.addSand(newCoordinates)
        if check != 0:
            return check

        # Add them in current position
        self.sand[coordinates] = True
        return 1


def main():
    print("Start")
    f = open(INPUT_PATH, "r")

    s = System()

    for line in f:
        if line == "\n":
            print("Empty line")
        else:
            line = line.strip()
            s.processLine(line)

    s.process()
    print("End")


if __name__ == "__main__":
    main()
