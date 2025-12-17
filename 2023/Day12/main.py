#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import math
import sys
import traceback
import logging

sys.setrecursionlimit(5000)
print(sys.getrecursionlimit())

INPUT_PATH = "./day12/input2.txt"

class System:
  def __init__(self):
    self.grid = Grid()
    self.lineCount = 0
    self.bestSignal = 0

    self.foundPaths = {}
    return

  def __str__(self):
    return f"Counted {self.lineCount} lines.\n{self.grid}"

  def processLine(self, line):
    for node in line:
      self.grid.addNode(node, self.lineCount)
    self.lineCount += 1
    return
  
  def process(self):
    # self.part1()
    self.part2()

  def part1(self):
    print("Part 1")
    print(self)

    memory = []
    for row in range(self.grid.rows + 1):
      memory.append([])
      for col in range(self.grid.columns + 1):
        memory[row].append(math.inf)
    self.findPath(self.grid.start, self.grid.end, 0, memory)

    # steps = math.inf
    # for row in range(self.grid.rows + 1):
    #   for col in range(self.grid.columns + 1):
    #     coordinates = (row, col)
    #     node = self.grid.getNode(coordinates)
    #     currSteps = self.getMemory(memory, coordinates)
    #     if node.elevation == self.bestSignal and currSteps < steps:
    #       steps = currSteps
          
      
    # print(f"Best signal: {self.bestSignal}, Steps: {steps}")
    for row in range(self.grid.rows + 1):
      printStr = ""
      for col in range(self.grid.columns + 1):
        printStr += f"({self.grid.getNode((row, col))},{str(memory[row][col]):3})"
      print(printStr)
    print(self.getMemory(memory, self.grid.end))

    return

  def part2(self):
    print("Part 2")
    print(self)

    minPath = math.inf
    for sRow in range(self.grid.rows + 1):
      memory = []
      for row in range(self.grid.rows + 1):
        memory.append([])
        for col in range(self.grid.columns + 1):
          memory[row].append(math.inf)
      start = (sRow, 0)
      self.findPath(start, self.grid.end, 0, memory)
      shortestPath = self.getMemory(memory, self.grid.end)
      if shortestPath < minPath:
        minPath = shortestPath
    print(shortestPath)


    return

  def findPath(self, start, end, count, memory):
    # if (start in self.foundPaths):
    #   return self.foundPaths[start]

    currElevation = self.grid.getNode(start).elevation
    if currElevation > self.bestSignal:
      self.bestSignal = currElevation

    if (start == end):
      self.setMemory(memory, start, count)
      return

    if self.getMemory(memory, start) > count:
      self.setMemory(memory, start, count)
      
      x = start[0]
      y = start[1]
      targetCoordinates = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
      for tc in targetCoordinates:
        if (self.testStep(start, tc)):
          self.findPath(tc, end, count + 1, memory)

  def testStep(self, src, target):
    x = target[0]
    y = target[1]
    if (x < 0 or y < 0 or x > self.grid.rows or y > self.grid.columns):
      return False

    sourceNode = self.grid.getNode(src)
    targetNode = self.grid.getNode(target)
    return self.grid.canStep(sourceNode, targetNode)
  
  def setMemory(self, memory, coordinates, value):
    memory[coordinates[0]][coordinates[1]] = value

  def getMemory(self, memory, coordinates):
    return memory[coordinates[0]][coordinates[1]]

class Grid:
  def __init__(self):
    self.nodesMatrix = []
    self.rows = -1
    self.columns = -1
    self.start = None
    self.end = None

  def __str__(self):
    retStr = ""
    for row in self.nodesMatrix:
      for node in row:
        retStr += str(node)
      retStr += "\n"
    retStr += f"Start pos: {self.start}, End pos: {self.end}"
    return retStr
  
  def addNode(self, node, row):
    if (row > self.rows):
      self.rows += 1
      self.columns = -1
      self.nodesMatrix.append([])
    self.columns += 1

    if (node == "S"):
      self.start = (self.rows, self.columns)
      node = 'a'
    elif (node == "E"):
      self.end = (self.rows, self.columns)
      node = 'z'

    nodeObj = Node(node)
    self.nodesMatrix[row].append(nodeObj)

  def canStep(self, src, target):
    return (src.elevation + 1 >= target.elevation)

  def getNode(self, coordinates):
    return self.nodesMatrix[coordinates[0]][coordinates[1]]
      

class Node:
  def __init__(self, symbol):
    self.symbol = symbol
    self.elevation = ord(self.symbol)
    return

  def __str__(self):
    return f"{self.symbol}"

def main():
  print('Start')
  f = open(INPUT_PATH, "r")

  s = System()
  
  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      s.processLine(line)
  
  try:
    s.process()
  except Exception as e:
    logging.error(traceback.format_exc())
  print('End')

if __name__ == '__main__':
  main()