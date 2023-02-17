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

# Other idea
Statement := Func | Exp
Func :=  Identifier "(" [Args | ɛ] ")"
Args :=  Exp ["," Exp]*


Int := DIGIT DIGIT*
Die := DIEOP Int

'''


from enum import Enum
from string import ascii_letters

class TokenType(Enum):
    End    = 0
    Int    = 1
    Ident  = 2
    DieOp  = 3

class Token:
    def __init__(self, type: TokenType) -> None:
        self.type = type
    
    def getType(self) -> TokenType:
        return self.type

class TokenEnd(Token):
    def __init__(self):
        super().__init__(TokenType.End)

class TokenInt(Token):
    def __init__(self, value):
        super().__init__(TokenType.Int)
        self.value = value

class TokenIdent(Token):
    def __init__(self, name):
        super().__init__(TokenType.Ident)
        self.name = name

class TokenDieOp(Token):
    def __init__(self):
        super().__init__(TokenType.DieOp)

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
                    tokenObj = TokenInt(int(token))
                elif ctype == _CharType.LETTER and len(token) > 1:
                    tokenObj = TokenIdent(token)
                elif ctype == _CharType.LETTER and token == 'd':
                    tokenObj = TokenDieOp()
                else:
                    # TODO: Make tokens for individual terminators
                    tokenObj = TokenIdent(token)
                tokens.append(tokenObj)

            ii += len(token)
        
        tokens.append(TokenEnd())

        return tokens
            
class JorParseError(Exception):
    def __init__(self, message):
        self.message = message

class ASTNodeType(Enum):
    Error = 0
    DiceList = 1

class ASTNode:
    def __init__(self, type: ASTNodeType) -> None:
        self.type = type
    
    def getType(self) -> ASTNodeType:
        return self.type

class ASTError(ASTNode):
    def __init__(self, message) -> None:
        super().__init__(ASTNodeType.Error)
        self.message = message

class ASTDiceList(ASTNode):
    def __init__(self, sides, count=1) -> None:
        super().__init__(ASTNodeType.DiceList)
        self.sides = sides
        self.count = count
    
    def getCount(self):
        return self.count
    
    def getSides(self):
        return self.sides

class JorParse:
    def __init__(self):
        self.tokens = []
        self.pos = None

    def parse(self, tokens) -> ASTDiceList:
        self.tokens = tokens
        self.pos = 0

        parse = None

        try:
            # Right now all we parse is a dice op, ie. 2d20
            parse = self.parseDice()
            end = self.__peek()
            if end.getType() is not TokenType.End:
                raise JorParseError("Unexpected extra tokens")
        except JorParseError as e:
            return ASTError(e.message)
        
        return parse

    def __peek(self) -> Token:
        if self.pos is None:
            return None
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def __eat(self) -> Token:
        tok = self.__peek()
        if tok is not None:
            self.pos += 1
        return tok

    # D -> Num? 'd' Num
    def parseDice(self):
        count = 1

        if self.__peek().getType() != TokenType.DieOp:
            countTok = self.expectInt("Expected a number of sides, or a 'd'")
            count = countTok.value
            if count < 1:
                raise JorParseError("Expected at least one die")
        
        dieTok = self.__eat()

        if dieTok.getType() != TokenType.DieOp:
            print("woah nelly, this op is", dieTok.getType())
            raise JorParseError("Expected a 'd' to identify a die, ie. 'd20'")
        
        sideTok = self.expectInt("Expected a number of faces after 'd'")
        
        return ASTDiceList(sideTok.value, count)
    
    def expectInt(self, errmsg) -> TokenInt:
        tok = self.__peek()
        if tok.getType() != TokenType.Int:
            raise JorParseError(errmsg)
        return self.__eat()