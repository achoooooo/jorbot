#!/bin/env python3

import argparse
import re
from sys import exit

import random

# roll an n-sided die
def roll(n):
    return random.randint(1, n)

from dparse import Tokenizer

parser = argparse.ArgumentParser(
    prog = "jorbot-cli",
    description = "command line for jorbot dice parsing"
)

parser.add_argument("expression")

def crash(msg="there was a problem"):
    print(msg)
    parser.print_help()
    exit(1)

def do_roll_logic(exp):
    # Parser (lol)
    match = re.match('(\d\d*)?[dD]?(\d\d*)', exp)
    if match is None:
        crash("this isn't the right input, idiot")
    
    numDice = 1
    if match.group(1) is not None:
        numDice = int(match.group(1))
    
    if match.group(2) is None:
        crash("somehow you're missing the dice size but the regex worked?")
    
    numFaces = int(match.group(2))

    for i in range(numDice):
        r = roll(numFaces)
        print(f"d{numFaces} #{i+1}:\t{r}")

def main():
    args = parser.parse_args()
    exp = str(args.expression).strip()

    tokens = Tokenizer.tokenize(exp)

    for t in tokens:
        print("Type:", t["type"], "Value", t["value"])


main()
