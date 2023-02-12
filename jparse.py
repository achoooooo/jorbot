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

-- operator precedence --

d
^
-
* / %
+ -


lang examples:

-6^2 -> -(^(6, 2)), ^ is higher than -
d6^2 -> ^(d(6), 2), d is higher than ^

20d10 -> 
20 


context-free grammar

DIGIT := "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"
CHAR := /[a-zA-Z]/
LPAREN := "("
RPAREN := ")"
OP_DIE := "d"
OP_EXP := "^"
OP_NEG := "-"
OP_ADD := "+"
OP_SUB := "-"
OP_MUL := "*"
OP_DIV := "/"
OP_MOD := "%"


J := Exp [; Exp]*
Exp := Func | Statement
Func := Ident LPAREN [Statement] ["," Statement]* RPAREN
Ident := IdChar [IdChar]*
IdChar := CHAR | DIGIT | "_"

Statement := St0
St0 := St1 [(OP_ADD | OP_SUB) St1]
St1 := St2 [(OP_MUL | OP_DIV | OP_MOD) St2]
St2 := [OP_NEG] St3
St3 := St4 [OP_EXP St4]
St4 := Int | Die | LPAREN St0 RPAREN
Die := [Int] DIEOP Int
Int := DIGIT DIGIT*


'''

from enum import Enum
from string import ascii_letters

class Token(Enum):
    INT = 1
    CHAR = 2
    IDENT = 3

# Used internally by tokenizer to group similar characters
class _CharType(Enum):
    TERM = 0
    DIGIT  = 2
    LETTER = 3
    SYMBOL = 4

class Tokenizer:
    def __get_ctype(c):
        if c.isdecimal():
            return _CharType.DIGIT
        if c.isalpha():
            return _CharType.LETTER
        if c.isspace():
            return _CharType.TERM
        
        return _CharType.SYMBOL
    
    def __eat_matching_symbols(str, start, ctype):
        if start < 0 or start >= len(str):
            return ""

        end = start
        while end < len(str) and Tokenizer.__get_ctype(str[end]) == ctype:
            end += 1

        return str[start:end]

    def tokenize(text):
        text = text.strip()
        tokens = []

        ii = 0

        while ii < len(text):
            token = text[ii]
            ctype = Tokenizer.__get_ctype(token)

            if ctype == _CharType.DIGIT or ctype == _CharType.LETTER:
                token += Tokenizer.__eat_matching_symbols(text, ii+1, ctype)
            
            if ctype != _CharType.TERM:
                tokenObj = None
                if ctype == _CharType.DIGIT:
                    tokenObj = {"type": Token.INT, "value": int(token)}
                elif ctype == _CharType.LETTER and len(token) > 1:
                    tokenObj = {"type": Token.IDENT, "value": token}
                else:
                    tokenObj = {"type": Token.CHAR, "value": token}
                tokens.append(tokenObj)

            ii += len(token)

        return tokens
            

class JParse:
    tokens
    def __init__():
        pass
