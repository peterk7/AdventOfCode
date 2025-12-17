#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdb

def main():
  print('Start')
  f = open("input.txt", "r")

  fullyContainedCount = 0
  overlapCount = 0
  
  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      # print(line)
      if (isFullyContained(line)):
        fullyContainedCount += 1
      if (overlapCheck(line)):
        overlapCount += 1
  
  print("Fully contained count: ", fullyContainedCount)
  print("Overlap count: ", overlapCount)
  print('End')

def isFullyContained(strRep):
  singles = strRep.split(",")
  firstSection = convertSectionToArray(singles[0])
  secondSection = convertSectionToArray(singles[1])
  firstOnly = firstSection - secondSection
  secondOnly = secondSection - firstSection
  if (len(firstOnly) == 0 or len(secondOnly) == 0):
    # print("Fully Contained!", strRep)
    # print("First Section: ", firstSection)
    # print("Second Section: ", secondSection)
    # print("First Only: ", firstOnly)
    # print("Second Only: ", secondOnly)
    # print("\n")

    return True

  return False

def overlapCheck(strRep):
  singles = strRep.split(",")
  firstSection = convertSectionToArray(singles[0])
  secondSection = convertSectionToArray(singles[1])
  overlap = firstSection.intersection(secondSection)
  if (len(overlap) == 0):
    return False

  print("Overlap!", strRep)
  print("First Section: ", firstSection)
  print("Second Section: ", secondSection)
  print("overlap: ", overlap)
  print("\n")

  return True

def convertSectionToArray(sectionStr):
  edges = sectionStr.split("-")
  return set(range(int(edges[0]), int(edges[1]) + 1))

if __name__ == '__main__':
  main()