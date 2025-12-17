#!/usr/bin/env python
# -*- coding: utf-8 -*-

class System:
  def __init__(self):
    self.cycle = 0
    self.x = 1
    self.signalStrengths = []
    self.nextMilestone = 40
    self.milestoneJump = 40
    self.line = ""

  def __str__(self):
    return f"({self.cycle}, {self.x})"

def main():
  print('Start')
  f = open("input3.txt", "r")
  
  s = System()

  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      processLine(line, s)
  
  print(s)
  print(s.signalStrengths)
  print(sum(s.signalStrengths))
  print('End')

def processLine(line, sys):
  splt = line.split(" ")
  if (splt[0] == "noop"):
    nextMilestone(sys)
  elif (splt[0] == "addx"):
    # 1 cycle nothing
    nextMilestone(sys)
    # 2 cycle nothing
    nextMilestone(sys)
    # end of 2, add splt[1] to x
    sys.x += int(splt[1])
  return

def nextMilestone(sys):
  sys.cycle += 1
  # draw
  relativeCycle = sys.cycle % sys.milestoneJump
  if (relativeCycle >= sys.x and relativeCycle < sys.x + 3):
    sys.line += "#"
  else:
    sys.line += "."
  
  if (sys.cycle == sys.nextMilestone):
    sys.signalStrengths.append(sys.cycle * sys.x)
    sys.nextMilestone += sys.milestoneJump
    print(sys.line)
    sys.line = ""
  return

if __name__ == '__main__':
  main()
  