#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdb
import math

ROUNDS = 10000
COMMON = 9599690

class Monkeys:
  def __init__(self):
    self.monkeys = []

  def __str__(self):
    retStr = f""
    for monkey in self.monkeys:
      retStr += str(monkey) + "\n"
    retStr += "\n\n"
    return retStr

class Monkey:
  def __init__(self, id):
    self.id = id
    self.items = []
    self.operationType = "None"
    self.operationValue = 0
    self.test = 0
    self.trueMonkey = None
    self.falseMonkey = None
    self.inspectedCount = 0

  def __str__(self):
    # retStr = f"Monkey({self.items})"
    retStr = f"Monkey({self.id}, {self.inspectedCount}, {self.operationType}, {self.operationValue}, {self.test}"
    retStr += f", {self.trueMonkey}"
    retStr += f", {self.falseMonkey}"
    retStr += f", items:{self.items}"
    retStr += ")"
    return retStr

def main():
  print('Start')
  f = open("input2.txt", "r")

  monkeys = Monkeys()
  
  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      processLine(line, monkeys)
  
  print(monkeys)
  for i in range(ROUNDS):
    playRound(monkeys)
  print("\n")
  print(monkeys)
  print(calcSumInspected(monkeys, 2))
  print('End')

def processLine(line, monkeys):
  splt = line.split(" ")
  if (splt[0] == "Monkey"):
    monkeys.monkeys.append(Monkey(splt[1][:-1]))
  elif (splt[0] == "Starting"):
    monkey = monkeys.monkeys[-1]
    monkey.items = list(map(cleanItem, splt[2:]))
    return
  elif (splt[0] == "Operation:"):
    monkey = monkeys.monkeys[-1]
    monkey.operationType =splt[-2]
    monkey.operationValue =splt[-1]
    return
  elif (splt[0] == "Test:"):
    monkey = monkeys.monkeys[-1]
    monkey.test = int(splt[-1])
    return
  elif (splt[0] == "If" and splt[1] == "true:"):
    monkey = monkeys.monkeys[-1]
    monkey.trueMonkey = int(splt[-1])
    return
  elif (splt[0] == "If" and splt[1] == "false:"):
    monkey = monkeys.monkeys[-1]
    monkey.falseMonkey = int(splt[-1])
    return
  return

def cleanItem(item):
  if item[-1] == ",":
    item = item[:-1]
  return int(item)

def playRound(monkeys):
  common = 1
  for monkey in monkeys.monkeys:
    common *= monkey.test

  for monkey in monkeys.monkeys:
    for item in monkey.items:
      woryLevel = calcWoryLevel(monkey, item, common)
      if (woryLevel % monkey.test == 0):
        target = monkeys.monkeys[monkey.trueMonkey]
        target.items.append(woryLevel)
      else:
        target = monkeys.monkeys[monkey.falseMonkey]
        target.items.append(woryLevel)
      monkey.inspectedCount += 1
    monkey.items = []
    # print(monkeys, "\n\n")
  return

def calcWoryLevel(monkey, item, common):
  woryLevel = item
  if (monkey.operationType == "*"):
    if (monkey.operationValue == "old"):
      woryLevel *= woryLevel
    else:
      woryLevel *= int(monkey.operationValue)
  if (monkey.operationType == "+"):
    if (monkey.operationValue == "old"):
      woryLevel += woryLevel
    else:
      woryLevel += int(monkey.operationValue)
  
  # woryLevel = math.floor(woryLevel/3)
  woryLevel = woryLevel % common

  return woryLevel

def calcSumInspected(monkeys, topX):
  top1 = 0
  top2 = 0
  for monkey in monkeys.monkeys:
    if monkey.inspectedCount >= top1:
      top1 = monkey.inspectedCount
    elif monkey.inspectedCount >= top2:
      top2 = monkey.inspectedCount
  return top1 * top2

if __name__ == '__main__':
  main()