"""
Dice Roller Utility

This script defines a function `roll_dice` that parses and evaluates standard dice notation strings 
(e.g., '2D6', '1D20+5', '3D4-2') commonly used in tabletop RPGs. It supports rolling a specified number 
of dice with a given number of sides, along with optional addition or subtraction modifiers.

Usage:
    roll_dice("2D6")      -> Rolls two 6-sided dice
    roll_dice("1D20+3")   -> Rolls one 20-sided die and adds 3
    roll_dice("4D4-1")    -> Rolls four 4-sided dice and subtracts 1

Returns:
    The total result as an integer.
Raises:
    ValueError if the input string format is invalid.
"""

import re
import random


def roll_dice(dice_string):
  #parse the dice string
  pattern = r"(\d+)D(\d+)(\s*([\+-]*)\s*(\d+))?"
  flag = re.I

  match = re.search(pattern, dice_string, flag)

  if not match:
    raise ValueError("Invalid dice string format")

  num_dice = int(match.group(1))
  dice_sides = int(match.group(2))
  add_sub = match.group(4)
  modifier = int(match.group(5)) if match.group(4) else 0

  #roll the dice
  rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
  #calculate the total
  if add_sub == "+":
    total = sum(rolls) + modifier
  elif add_sub == "-":
    total = sum(rolls) - modifier
  else:
    total = sum(rolls)
  #return the result
  return total
