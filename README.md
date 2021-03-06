
# Quixo Python

Implementation of turn based game Quixo in Python. Minimax with alpha beta pruning algorithm is used for computer play.

## Playing

Pass any player instance from players.py to play.py<br><br>
***Random vs Random***
```
# 100 Iterations
# play.py
play(RandomPlayer(),RandomPlayer(),100)
```
***AI vs Random***
```
# 100 Iterations
# play.py
play(AI_Player(GOOD_AI_PLAYER),RandomPlayer(),100)
```
## Moves

**play**(piece,move)\
**piece**: tuple = (row,col)\
**move**: int = Direction

  #### Directions
  SLIDE_LEFT = 0\
  SLIDE_UP = 1\
  SLIDE_RIGHT = 2\
  SLIDE_DOWN = 3
  
### Illegal moves:

Only blank and self pieces can be moved.\
Only edge pieces can be moved.\
<br>
if row is 0 cant slide down\
if row is board_size cant slide up\
if col is 0 cant slide right\
if col is board_size cant slide down

## State

### Piece Values

0 = Blank

1 = X

2 = O

### Turn

1 = X

2 = O 

## Value Function

V = evaluate(board)

### Game Terminal Values
V = 100 + depth (X wins with minimum number of movements)\
V = - (100 + depth) (O wins with minimum number of movements)

### Depth Reach Values
More owned pieces on the board is usually better in initial game states.\
V = (X Piece Count) - (O Piece Count)

## Board Methods

**printBoard()** - print game board\
**printTurn()** - prints current turn\
**getPossibleMoves()** - returns all possible moves for the current board.\
Returns moves in list of (piece,move)\
**getPossiblePieceMove()** returns all possible moves for a single piece for current board.\
Returns (move)\
**isGameEnd()** - Returns winner integer value if game ended else returns None\
**changeTurn()** - Changes turn\
**shift()** - Shifts board when moving a piece\
Used by play() method\
**checkMove()** - Check a move if its valid\
Returns True or False
