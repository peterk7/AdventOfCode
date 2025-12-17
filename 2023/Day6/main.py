#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
  print('Start')
  f = open("input.txt", "r")
  
  for line in f:
    if (line == "\n"):
      print("Empty line")
    else:
      line = line.strip()
      print("Processed characters for Marker: ", processLine(line, 4))
      print("Processed characters for Message: ", processLine(line, 14))
  
  print('End')

def processLine(line, uniqeCount):
  porocessed = 0
  buffer = []
  for char in line:
    if (len(buffer) < uniqeCount):
      buffer.append(char)
    else:
      if len(buffer) == len(set(buffer)):
        break
      buffer.append(char)
      buffer.pop(0)
    porocessed += 1
    # print(buffer)
  return porocessed

if __name__ == '__main__':
  main()