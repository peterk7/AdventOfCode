#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdb 

COMMAND = "$"
COMMAND_LS = 'ls'
COMMAND_CD = 'cd'
LS_DIR = "dir"
CD_BACK = ".."
CD_ROOT = "/"

TYPE_DIR = "D"
TYPE_FILE = "F"
INDENT = "  "

TOTAL_SYSTEM_SIZE = 70000000
UNUSED_SPACE_NEEDED = 30000000

class TreeNode:
  def __init__(self, data = None):
    self.data = data
    self.children = []
    self.parent = None

  def __str__(self):
    return self.toStr()

  def toStr(self, indent = ""):
    objStr = f"{indent} - {self.data}\n"
    for child in self.children:
        objStr += child.toStr(indent + INDENT)
    return objStr

  def getSize(self):
    if (self.data.size == 0 and self.data.type == TYPE_DIR):
      for child in self.children:
        self.data.size += child.getSize()
    return self.data.size


class NodeData:
  def __init__(self, name, type = TYPE_DIR, size = 0):
    self.name = name
    self.type = type
    self.size = size

  def __str__(self):
    return f"{self.name} ({self.type}, {self.size})"

def main():
  print('Start')
  f = open("./input.txt", "r")
  
  root = TreeNode(NodeData("/"))
  root.parent = root
  current = root

  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      current = processLine(line, current, root)
  
  # pdb.set_trace()
  print("Total size: ", root.getSize())
  print(root)
  print("Size sum < 100000:", calculateDirSize(root, 100000))
  totalSizeToFree = UNUSED_SPACE_NEEDED - TOTAL_SYSTEM_SIZE + root.getSize()
  print("Total size to free needed:", totalSizeToFree)
  closestCandidate = findClosestCandidate(root, totalSizeToFree)
  print(closestCandidate.data.size)
  print('End')

def processLine(line, current, root):
  splt = line.split(" ")
  if (splt[0] == COMMAND):
    # process command
    
    if (splt[1] == COMMAND_LS):
      # Skip LS command, we will process the next lines instead
      return current
    elif (splt[1] == COMMAND_CD):
      op = splt[2]
      if (op == CD_ROOT):
        current = root
      elif (op == CD_BACK):
        current = current.parent
      else:
        # Find or create child
        current = findOrCreateDir(op, current)
      return current
    else: 
      print("Error: Command invalid - {splt[1]}")
      return current
  elif (splt[0] == LS_DIR):
    findOrCreateDir(splt[1], current)
    return current
  else:
    # file
    size = int(splt[0])
    fileName = splt[1]
    findOrCreateFile(current, fileName, size)
    return current

  return current

def findOrCreateDir(dirName, current):
  dir = next((dir for dir in current.children if dir.data.name == dirName), None)
  if (dir == None):
    # Create dir
    dir = TreeNode(NodeData(dirName))
    dir.parent = current
    current.children.append(dir)
  return dir

def findOrCreateFile(current, fileName, size):
  file = next((dir for dir in current.children if dir.data.name == fileName), None)
  if (file == None):
    # Create File
    file = TreeNode(NodeData(fileName, TYPE_FILE, size))
    file.parent = current
    current.children.append(file)
  return file

def calculateDirSize(root, maxSize):
  if (root.data.type == TYPE_FILE):
    return 0
  sizeSum = 0
  currSize = root.data.size
  if (root.data.type == TYPE_DIR and currSize <= maxSize):
    sizeSum += currSize
  for child in root.children:
    sizeSum += calculateDirSize(child, maxSize)

  return sizeSum

def findClosestCandidate(root, sizeNeeded):
  if (root.data.type == TYPE_FILE):
    return None
  
  currentCandidate = None
  currSize = root.data.size
  if (currSize >= sizeNeeded):
    currentCandidate = root
  
  for child in root.children:
    childCandidate = findClosestCandidate(child, sizeNeeded)
    currentCandidate = compareCandidates(currentCandidate, childCandidate)

  return currentCandidate

def compareCandidates(first, second):
  if first == None:
    return second
  if second == None:
    return first
  return first if first.data.size < second.data.size else second

if __name__ == '__main__':
  main()