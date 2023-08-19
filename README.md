# reversi
This is an implimentation of the reversi game.
Reversi is a two-player strategy game played on an 8x8 board using discs that are colored white on one side and black on the other.
One player plays discs black side up while his opponent plays the discs white side up.

## Rules
### Object of the Game
The object of the game is to place your discs on the board so as to outflank your opponent's discs, flipping them over to your color.
The player who has the most discs on the board at the end of the game wins.

### Rules
Note: For convenience, board positions are denoted by a letter representing the column (A through H) and a number representing the row (1 through 8).

1. Each player chooses a color to play.
1. Every game starts with four discs placed in the center of the board, as shown in Figure1.  
  ![Figure1](./doc/rulesFigure1.gif)
1. Although the players choose who goes first in normal rules, the player who chooses black is first in this implementation.
1. Players take turns making moves.
  A move consists of a player a disc of his color on the board.
  The disc must be placed so as to outflank one or more opponent discs, which are then flipped over to the current player's color.  
  Outflanking your opponent means to place your disc such that it traps one or more or your opponent's discs between another disc of your color along a horizontal, vertical or diagonal line through the board square.
1. If a player cannot make a legal move, he forfeits his turn and the other player moves again (this is also known as passing a turn).
  Note that a player may not forfeit his turn voluntarily.
  If a player can make a legal move on his turn, he must do so.
1. The game ends when neither player can make a legal move.
  This includes when there are no more empty squares on the board or if one player has flipped over all of opponent's discs (a situation commonly known as a wipeout).
1. The player with the most discs of his color on the board at the end of the game wins.
  The game is a draw if both players have the same number of discs.

Note: When making a move, you may outflank your opponent's discs in more than one direction, All outflanked discs are flipped.

## Usecases
### Start a new game
1. start this game application.
1. push "START" button.
1. choose your disc's color.
  If you choose black, you are first.
  Otherwise, your opponent is first.
1. indicate game board in the application window where there are four discs in the center of the board.
  Then a new game gets started.

### Moving a game
1. The black player is first.
   He places a disc of his color in a square where this disc can outflankes one or more his opponent's discs.
   To place a disc is to click a square in which he wants to place his disc.
   Then his turn has finshed.
1. Next, the white player places a disc and his turn has finished.
   If there is no square in which he can place a disc, his turn is passed and his opponent's turn comes.
1. Repeat the above steps until the game has finished

## Referrence
- [Reversi Rules](https://documentation.help/Reversi-Rules/rules.htm)
