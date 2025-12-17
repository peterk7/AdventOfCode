#!/usr/bin/env python
# -*- coding: utf-8 -*-

GRID = []
ROWS = 0
COL = 0
MAX_SCORE = 0

class Tree:
  def __init__(self, height, checked = False):
    self.height = height
    self.checked = checked
    self.scenicScore = 0
    self.countUp = 0
    self.countDown = 0
    self.countLeft = 0
    self.countRight = 0

  def __str__(self):
    return f"Tree({self.height}, {self.countUp}, {self.countDown}, {self.countLeft}, {self.countRight}, Score: {self.scenicScore})"

def main():
  print('Start')
  f = open("input.txt", "r")
  
  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      # print(line)
      processLine(line)
  
  printGrid()
  print("Visible: ", countVisible())
  gatherScores()
  print("Max score: ", MAX_SCORE)
  print('End')

def processLine(line):
  global ROWS
  global COL
  GRID.append([])

  COL = 0
  for char in line:
    height = int(char)
    GRID[ROWS].append(Tree(height))
    COL += 1
  ROWS += 1
  # print(GRID, COL, ROWS)
  return
  
def countVisible():
  count = 0

  # printGrid()

  # Top to bottom
  for col in range(COL):
    highest = -1
    for row in GRID:
      tree = row[col]
      height = tree.height
      if (height > highest):
        highest = height
        if (not tree.checked):
          tree.checked = True
          count += 1
      if highest == 9:
        break

  # printGrid()

  # Bottom to top
  for col in range(COL):
    highest = -1
    for row in list(reversed(GRID)):
      tree = row[col]
      height = tree.height
      if (height > highest):
        highest = height
        if (not tree.checked):
          tree.checked = True
          count += 1
      if highest == 9:
        break

  # printGrid()

  # Left to right
  for row in GRID:
    highest = -1
    for tree in row:
      height = tree.height
      if (height > highest):
        highest = height
        if (not tree.checked):
          tree.checked = True
          count += 1
      if highest == 9:
        break

  # printGrid()
  
  # Right to left
  for row in GRID:
    highest = -1
    for tree in list(reversed(row)):
      height = tree.height
      if (height > highest):
        highest = height
        if (not tree.checked):
          tree.checked = True
          count += 1
      if highest == 9:
        break

  # printGrid()
    

  return count

def gatherScores():
  global MAX_SCORE

  for col in range(COL):
    for row in range(ROWS):
      tree = GRID[row][col]
      # print("Tree compared", tree)

      # up
      for r in list(reversed(range(row))):
        compTree = GRID[r][col]
        tree.countUp += 1
        if (tree.height <= compTree.height):
          break

      # down
      # print("Down")
      for r in range(row+1, ROWS):
        compTree = GRID[r][col]
        tree.countDown += 1
        if (tree.height <= compTree.height):
          break

      # print(tree)

      # print("Left")
      for c in list(reversed(range(col))):
        compTree = GRID[row][c]
        tree.countLeft += 1
        if (tree.height <= compTree.height):
          break

      # print("Right")
      for c in range(col+1, COL):
        compTree = GRID[row][c]
        tree.countRight += 1
        if (tree.height <= compTree.height):
          break

      tree.scenicScore = tree.countUp * tree.countDown * tree.countLeft * tree.countRight
      if tree.scenicScore > MAX_SCORE:
        MAX_SCORE = tree.scenicScore
      print("Tree compared", tree)
    print("Col ~~~")

def printGrid():
  print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  print("Grid Columns: ", COL, "Grid Rows:", ROWS)
  for row in GRID:
    rowString = ""
    for tree in row:
      rowString += str(tree) + " | "
    print(rowString)
  print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  return

if __name__ == '__main__':
  main()