#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdb

LOWER_CASE_SHIFT = -96
UPPER_CASE_SHIFT = -38

def main():
  print('Start')
  f = open("input.txt", "r")
  prioritySum = 0
  groupPrioritySum = 0
  group = []
  
  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      prioritySum += processLine(line)
      group.append(line)
      if (len(group) == 3):
        groupPrioritySum += groupPriority(group)
        group = []

  
  print("Group leftover", group)
  print("Priority Sum = ", prioritySum)
  print("Group priority Sum = ", groupPrioritySum)
  print('End')
  # print(ord('a')) # -96
  # print(ord('z')) # -96
  # print(ord('A')) # -38
  # print(ord('Z')) # -38

def processLine(line):

  firstHalf = line[:len(line)//2]
  secondHalf = line[len(line)//2:]
  priority = 0

  # print("First half", firstHalf);
  # print("Second half", secondHalf);
  intersection = set(firstHalf).intersection(secondHalf)
  # print(intersection)
  for i in intersection:
    priority += getCharScore(i)

  return priority

def groupPriority(groupArr):
  common = set(groupArr[0])
  for line in groupArr[1:]:
    common = common.intersection(line)
  print(common)
  priority = 0
  for i in common:
    priority += getCharScore(i)
  return priority


def getCharScore(char):
  asciiVal = ord(char)
  if (97 <= asciiVal and asciiVal <= 122):
    return (asciiVal + LOWER_CASE_SHIFT)
  elif (65 <= asciiVal and asciiVal <= 90):
    return (asciiVal + UPPER_CASE_SHIFT)
  else:
    print("Error! Wrong char given: ", char, asciiVal)
    return 0

if __name__ == '__main__':
  main()