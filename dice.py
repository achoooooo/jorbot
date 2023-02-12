import random

'''

operators
- 'd':        turns number to dice[] of size 1
- () []
- arithmetic operators
    - +, -, *, /
    - behavior with dice:
        - N * dice[]: turns dice[] of size M into dice of size N*M

function list
- sort? -> sorts dice[] by resolved value upon evaluation
    - input:  dice[]
    - output: dice[]

- explode -> re-rolls any dice that are rolled to max value upon evaluation
    - input: dice[]
    - output: dice[]

- countGreater -> counts how many dice are greater than a specified value
    - input: dice[], int
    - output: int
- countLess -> counts how many dice are less than a specified value
    - input: dice[], int
    - output: int

- keep/keepBest/advantage -> discard everything but the highest value, or the top N values if int is given
    - input: dice[], int?
    - output: dice[]
- keepWorst/disadvantage -> discard everything but the worst value, or the lowest N values if int is given
    - input: dice[], int?
    - output: dice[]
- keepGreater -> discard any dice that aren't greater than specified value
    - input: dice[], int
    - output: dice[]
- keepLess -> discard any dice that aren't less than the specified value
    - input: dice[], int
    - output: dice[]


- rerollGreater
    - input: dice[], int, times = int?
    - output: dice[]
- rerollLess
    - input: dice[], int, times = int?
    - output: dice[]
- rerollIf
    - input: dice[], int, times = int?
    - output: dice[]
- rerollUntilGreater
    - input: dice[], int
    - output: dice[]
- rerollUntilLess
    - input: dice[], int
    - output: dice[]


2d6r[<2]

rerollLess(2d6, 3)

advantage(2d20)


'''

'''
context-free grammar

DIGIT := "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
CHAR := /[a-zA-Z]/
LPAREN := "("
RPAREN := ")"
OP_DIE := "d"
OP_ADD := "+"
OP_SUB := "-"
OP_MUL := "*"
OP_DIV := "/"


Int := DIGIT DIGIT*
Die := DIEOP Int

'''



