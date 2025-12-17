#!/usr/bin/env python
# -*- coding: utf-8 -*-

CRATE_MATRIX = []
LINE_MEMORY = []
CRATES_PARSE_START = 1
CRATES_PARSE_JUMP = 4

def main():
  print('Start')
  f = open("input.txt", "r")
  
  fillCratesCheck = True

  for line in f:
    if (line == "\n"):
      fillCrates()
      fillCratesCheck = False
    else:
      # line = line.strip()
      if (fillCratesCheck):
        # print(line)
        saveLine(line)
      else: 
        moveCrates(line)
        # break
  
  print(CRATE_MATRIX)

  print("Top crates are: ", getTopCrates())
  print('End')

def saveLine(line):
  LINE_MEMORY.append(line)
  return

def fillCrates():
  print("Fill Crates!")
  LINE_MEMORY.reverse()
  # print(LINE_MEMORY)

  # Init lists
  stackNumbers = LINE_MEMORY[0].strip().split(" ")
  countStacks = len([i for i in stackNumbers if i != ""])
  while countStacks > 0:
    CRATE_MATRIX.append([])
    countStacks -= 1

  for row in LINE_MEMORY[1:]:
    pos = CRATES_PARSE_START
    lane = 0
    while pos < len(row):
      crate = row[pos]
      if (crate != " "):
        CRATE_MATRIX[lane].append(crate)
      pos += CRATES_PARSE_JUMP
      lane += 1
  print(CRATE_MATRIX)
  return

def moveCrates(line):
  line = line.strip()
  # print("Move Crates!", line)
  splt = line.split(" ")
  mv = int(splt[1])
  fr = int(splt[3]) - 1
  to = int(splt[5]) - 1
  # print("Move", mv, " From", fr, " To", to)
  stack = CRATE_MATRIX[fr]

  # Extract crates to move
  start = len(stack) - mv
  arrToMove = CRATE_MATRIX[fr][start:]

  # Reorder in reverse
  # arrToMove.reverse()
  # print(arrToMove)

  # Update to stack with crates
  CRATE_MATRIX[to].extend(arrToMove)

  # Update from stack removing crates
  CRATE_MATRIX[fr] = CRATE_MATRIX[fr][:start]

  # print(CRATE_MATRIX)
  return

def getTopCrates():
  cratesStr = ""
  for stack in CRATE_MATRIX:
    cratesStr += stack[len(stack)-1]
  return cratesStr

if __name__ == '__main__':
  main()