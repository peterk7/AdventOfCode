#!/usr/bin/env python
# -*- coding: utf-8 -*-

elfList = []

def main():
  print('Start')
  f = open("input.txt", "r")
  sumPerElf = 0
  for line in f:
    if (line == "\n"):
      elfList.append(sumPerElf)
      sumPerElf = 0
    else:
      sumPerElf += int(line)
      # print(line)

  print(elfList.sort())
  print(elfList[-3:])
  print(sum(elfList[-3:]))
  
  print('End')

if __name__ == '__main__':
  main()