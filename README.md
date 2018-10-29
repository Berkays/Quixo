#Quixo Python

##Moves

Move:Tuple = (row,col)

Only blank and self pieces can be moved.
Only edge pieces can be moved.


###Illegal moves:
if row is 0 cant slide down
if row is board_size cant slide up
if col is 0 cant slide right
if col is board_size cant slide down




##State

###Pieces
0 = Blank
1 = X
2 = O

###Turn
0 = X
1 = O

##Value

V = f(state)

V = -1 X wins
V = 0 Draw
V = 1 O wins





25 Piece
(25 * 3) + 1 bits