#!/usr/bin/env python
# -*- coding: utf-8 -*-

OPONENT_ROCK = "A"
OPONENT_PAPER = "B"
OPONENT_SCISSORS = "C"
# MY_ROCK = "X"
# MY_PAPER = "Y"
# MY_SCISSORS = "Z"
LOOSE = "X"
DRAW = "Y"
WIN = "Z"

SCORE_R = 1
SCORE_P = 2
SCORE_S = 3

# HAND_SCORE_MAP = {
#   MY_ROCK: SCORE_R,
#   MY_PAPER: SCORE_P,
#   MY_SCISSORS: SCORE_S
# }
HAND_SCORE_MAP = {
  (OPONENT_ROCK, LOOSE): SCORE_S,
  (OPONENT_ROCK, DRAW): SCORE_R,
  (OPONENT_ROCK, WIN): SCORE_P,
  (OPONENT_PAPER, LOOSE): SCORE_R,
  (OPONENT_PAPER, DRAW): SCORE_P,
  (OPONENT_PAPER, WIN): SCORE_S,
  (OPONENT_SCISSORS, LOOSE): SCORE_P,
  (OPONENT_SCISSORS, DRAW): SCORE_S,
  (OPONENT_SCISSORS, WIN): SCORE_R,
}

SCORE_WIN = 6
SCORE_DRAW = 3
SCORE_LOOSE = 0

# SCORE_MAP = {
#   (OPONENT_ROCK, MY_ROCK): SCORE_DRAW,
#   (OPONENT_ROCK, MY_PAPER): SCORE_WIN,
#   (OPONENT_ROCK, MY_SCISSORS): SCORE_LOOSE,
#   (OPONENT_PAPER, MY_ROCK): SCORE_LOOSE,
#   (OPONENT_PAPER, MY_PAPER): SCORE_DRAW,
#   (OPONENT_PAPER, MY_SCISSORS): SCORE_WIN,
#   (OPONENT_SCISSORS, MY_ROCK): SCORE_WIN,
#   (OPONENT_SCISSORS, MY_PAPER): SCORE_LOOSE,
#   (OPONENT_SCISSORS, MY_SCISSORS): SCORE_DRAW,
# }
CONCLUSION_SCORE = {
  LOOSE: SCORE_LOOSE,
  DRAW: SCORE_DRAW,
  WIN: SCORE_WIN
}

def main():
  print('Start')
  f = open("input.txt", "r")
  
  totalScore = 0
  # count = 10
  
  for line in f:
    # if (count == 0):
    #   break
    if (line == "\n"):
      print("Empty line")
    else:
      round = tuple(line.strip().split(" "))
      # totalScore += HAND_SCORE_MAP[round[1]] + SCORE_MAP[round]
      totalScore += HAND_SCORE_MAP[round] + CONCLUSION_SCORE[round[1]]
      print(totalScore)
      # count -= 1
  
  print("Final score:", totalScore)
  print('End')

if __name__ == '__main__':
  main()