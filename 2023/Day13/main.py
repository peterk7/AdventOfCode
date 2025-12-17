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

DAY = "13"
INPUT_PATH = f"./day{DAY}/input2.txt"

def isNumber(var):
  return type(var) == int or type(var) == float

class System:
  def __init__(self):
    self.pairs = []
    self.first = None
    self.packets = []
    return

  def __str__(self):
    return f"System({self.pairs})"

  def processLine(self, line, count):
    # print(line, count)
    arr = json.loads(line)
    # print(arr)
    if (self.first != None):
      pair = [self.first, arr]
      self.pairs.append(pair)
      self.packets.append(arr)
      self.first = None
    else:
      self.first = arr
      self.packets.append(arr)
    return

  def process(self):
    self.part1()
    self.part2()

  def part2(self):
    div1 = [[2]]
    div2 = [[6]]
    self.packets.append(div1)
    self.packets.append(div2)

    sortedPackets = sorted(self.packets, key=functools.cmp_to_key(processPair))
    div1Index = sortedPackets.index(div1) + 1
    div2Index = sortedPackets.index(div2) + 1
    print(f"Div 1 index: {div1Index}, Div 2 index: {div2Index}, Mult: {div1Index * div2Index}")

    return

  def part1(self):
    
    sum = 0
    index = 1
    for pair in self.pairs:
      check = processPair(pair[0], pair[1])
      print(index, check)
      if check < 0:
        sum += index
      index += 1
    
    print(sum)
    return
  
def processPair(first, second):
  if (isNumber(first) and isNumber(second)):
    return first - second
  
  if (isNumber(first)):
    return processPair([first], second)

  if (isNumber(second)):
    return processPair(first, [second])

  index = 0
  while index < len(first) and index < len(second):
    check = processPair(first[index], second[index])
    # Only keep comparing if the integers are equal
    if check != 0:
      return check
    index += 1
  
  return len(first) - len(second)
  # if index == len(first) and index == len(second):
  #   return 0
  # elif index == len(first):
  #   return -1
  # else:
  #   return 1

class Day12:
  def __init__(self):
    return

  def __str__(self):
    return f""

def main():
  print('Start')
  f = open(INPUT_PATH, "r")

  s = System()
  
  count = 0
  for line in f:
    if (line == "\n"):
      # print("Empty line")
      count = 0
    else:
      count += 1
      line = line.strip()
      s.processLine(line, count)
  
  s.process()
  print('End')

if __name__ == '__main__':
  main()