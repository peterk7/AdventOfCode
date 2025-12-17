#!/usr/bin/env python
# -*- coding: utf-8 -*-

UP = "U"
DOWN = "D"
LEFT = "L"
RIGHT = "R"
BLANK = "*"

GRID = []

DIRECTION_MAP = {
  "U": (0,1),
  "D": (0,-1),
  "L": (-1,0),
  "R": (1,0)
}

class Knot:
  def __init__(self, name):
    self.name = name
    self.coordinates = (0,0)
    self.prevCoordinates = (0,0)
    self.visitedCoordinates = set()
    self.visitedCoordinates.add(self.coordinates)

  def __str__(self):
    return f"{self.name}{self.coordinates}"

# LENGTH = 2
LENGTH = 10

def main():
  print('Start')
  f = open("input.txt", "r")

  knots = []
  for i in range(LENGTH):
    knots.append(Knot(f"{i}"))

  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      processLine(line, knots)
  
  print(knots[0])
  print(knots[LENGTH - 1])
  # print(knots[LENGTH - 1].visitedCoordinates)
  print(len(knots[LENGTH - 1].visitedCoordinates))
  print('End')

def processLine(line, knots):

  splt = line.split(" ")
  # print(splt)
  direction = splt[0]
  amount = int(splt[1])

  for i in range(amount):
    # Move head
    head = knots[0]
    head.prevCoordinates = head.coordinates
    # print(head, direction, DIRECTION_MAP[direction])
    head.coordinates = addVectors(head.coordinates, DIRECTION_MAP[direction])

    for j in range(1, LENGTH):
      # Should move section
      prev = knots[j-1]
      curr = knots[j]
      distance = subVectors(prev.coordinates, curr.coordinates)
      absDistance = absVector(distance)
      currDirection = extractDirection(distance)
      # print(j, distance, absDistance, currDirection)
      if absDistance[0] > 1 or absDistance[1] > 1:
        curr.prevCoordinates = curr.coordinates
        curr.coordinates = addVectors(curr.coordinates, currDirection)
        # print(curr.coordinates)
        curr.visitedCoordinates.add(curr.coordinates)
        
  return

def addVectors(vec1, vec2):
  return (vec1[0] + vec2[0], vec1[1] + vec2[1])

def subVectors(vec1, vec2):
  return (vec1[0] - vec2[0], vec1[1] - vec2[1])

def absVector(vec):
  return (abs(vec[0]), abs(vec[1]))

def extractDirection(vec):
  x = 0
  if vec[0] > 0:
    x = 1
  elif vec[0] < 0:
    x = -1

  y = 0
  if vec[1] > 0:
    y = 1
  elif vec[1] < 0:
    y = -1

  return (x, y)

if __name__ == '__main__':
  main()