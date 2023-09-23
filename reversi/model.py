# ==========================================================
# model.py
# Copyright (C) 2023 Kei Shioda.  All rights reserved.
# ==========================================================
''' This module defines game logics of reversi.
'''
from __future__ import annotations
from enum import Enum

class State(Enum):
    ''' This class indicates a state of this application.
    '''
    
    START = 0
    MAINMENU = 1
    CONFIG = 2
    GAMESTART = 3
    USER = 4
    OPPONENT = 5
    RESULT = 6
    EXIT = 7
    ERROR = 8

class Color(Enum):
    ''' This class indicates a color for playing side.
    '''
    BLACK = 0
    WHITE = 1
    NONE = 2
    
    @classmethod
    def get_opponent(cls, c: Color) -> Color:
        '''This method returns an opponent color of the given color
        
        :param c: the given color that must be BLACK or WHITE
        :return: an opponent color
        '''
        assert c is Color.BLACK or c is Color.WHITE
        if c is Color.BLACK:
            return Color.WHITE
        else:
            return Color.BLACK
    
    @classmethod
    def to_str(cls, c:Color) -> str:
        ''' This method returns a word indicating the given color.
        
        :param c: the given color
        :return: a word BLACK, WHITE or NONE
        '''
        assert c is Color.BLACK or c is Color.WHITE
        match c:
            case Color.BLACK:
                return "BLACK"
            case Color.WHITE:
                return "WHITE"
            case _:
                return "NONE"

class Square(Enum):
    ''' This class defines a square of a board.
    '''
    BLACK = -1
    NONE = 0
    WHITE = 1
    WALL = 2
    
    @classmethod
    def to_square(cls, c: Color) -> Square:
        ''' This method returns a value of Square as same as the given color.
        
        :param c: the given color
        :return: a value of square as same as the given color
        '''
        assert c in [i for i in Color]
        
        match c:
            case Color.BLACK:
                return Square.BLACK
            case Color.WHITE:
                return Square.WHITE
            case _:
                return Squre.NONE

class GameResult(Enum):
    ''' This class defines the user's result of a game
    '''
    WIN = 0
    LOSE = 1
    DRAW = 2

class Board:
    ''' This class defines a game board.
    '''
    BOARD_SIZE = 8
    WALL_SIZE = 2
    LOWER_WALL = 0
    UPPER_WALL = 9
    LOWER_CENTER = 4
    UPPER_CENTER = 5
    
    DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1), 
                  (-1, 0), (-1, -1), (0, -1), (1, -1)]
    
    def __init__(self) -> Board:
        ''' This method creates an instance of Board.
        
        :return: a created instance
        '''
        self.board = [[Square.NONE] * (self.BOARD_SIZE + self.WALL_SIZE) for i in range(self.BOARD_SIZE + self.WALL_SIZE)]
        
        for i in range(len(self.board)):
            self.board[self.LOWER_WALL][i] = Square.WALL
            self.board[self.UPPER_WALL][i] = Square.WALL
        for j in range(len(self.board)):
            self.board[j][self.LOWER_WALL] = Square.WALL
            self.board[j][self.UPPER_WALL] = Square.WALL
        
        self.board[self.LOWER_CENTER][self.LOWER_CENTER] = Square.BLACK
        self.board[self.LOWER_CENTER][self.UPPER_CENTER] = Square.WHITE
        self.board[self.UPPER_CENTER][self.LOWER_CENTER] = Square.WHITE
        self.board[self.UPPER_CENTER][self.UPPER_CENTER] = Square.BLACK
    
    def update(self, x: int, y: int, c: Color) -> bool:
        ''' This method updates the board situation.
        
        :param x: indicates x coordinate of a square where a disc is put
        :param y: indicates y coordinate of a square where a disc is put
        :param c: indicates the disc's color
        :return: if update is done, return true, otherwise return false
        '''
        changeable = self.get_changeable(x, y, c)
        
        if len(changeable) <= 1:
            return False
        
        for i in changeable:
            x, y = i
            self.board[y][x] = Square.to_square(c)
        return True
    
    def get_changeable(self, x: int, y: int, c: Color) -> List:
        player = Square.to_square(c)
        opponent = Square.to_square(Color.get_opponent(c))
        change = [(x, y)]
        for d in self.DIRECTIONS:
            dx, dy = d
            i = 1
            j = 1
            candidate = []
            while self.board[y + dy * j][x + dx * i] == opponent:
                candidate.append((x + dx * i, y + dy * j))
                i += 1
                j += 1
            if len(candidate) > 0 and self.board[y + dy * j][x + dx * i] == player:
                for p in candidate:
                    change.append(p)
        return change
    
    def to_color(self) -> List:
        ''' This method converts Square to Color for the board except WALL zone
        
        :return: 8x8 List of Color
        '''
        col = []
        for j in range(self.LOWER_WALL+1, self.UPPER_WALL):
            row = []
            for i in range(self.LOWER_WALL+1, self.UPPER_WALL):
                match self.board[j][i]:
                    case Square.BLACK:
                       row.append(Color.BLACK)
                    case Square.WHITE:
                       row.append(Color.WHITE)
                    case _:
                       row.append(Color.NONE)
            col.append(row)
        return col
    
    def count(self) -> tuple:
        ''' This method counts the number of discs of both players.
        
        :return: a tuple that contains the number of black and that of white
        '''
        black = 0
        white = 0
        for j in self.board:
            for i in j:
                if i == Square.BLACK:
                    black += 1
                elif i == Square.WHITE:
                    white += 1
                else:
                    pass
        return (black, white)

class Game:
    ''' This class defines a game of reversi.
    '''
    def __init__(self) -> Game:
        ''' This method creates a instance
        
        :return: a created instance
        '''
        self.board = Board()
        self.passflag = False
        self.finishflag = False
        self.gameresult = None
    
    def get_board_situation(self) -> List:
        ''' This method returns the current situation on the board
        
        :return: a 8x8 List of Color
        '''
        return self.board.to_color()
    
    def put_disc(self, x: int, y: int, c: Color) -> bool:
        ''' This method puts a disc on the board.
        
        :param x: x coordinate of the position
        :param y: y coordinate of the position
        :param c: a putting disc's color
        :return: if the putting position is valid, return true,
                 otherwise, return false.
        '''
        if not self.board.update(x, y, c):
            return False
        
        self.passflag = False
        return True
    
    def take_pass(self, c: Color) -> bool:
        ''' This method lets player pass his turn.
        
        :param c: player's color of this turn
        :return: if there is no valid putting position, return true,
                 otherwise, return false
        '''
        b = self.board.to_color()
        indices = []
        for j in range(0,len(b)):
            for i in range(0,len(b)):
                if b[j][i] == Color.NONE:
                    indices.append((i, j))
        
        is_valid = False
        for i in indices:
            x, y = i
            if len(self.board.get_changeable(x + 1, y + 1, c)) > 1:
                is_valid = True
                break
        
        if is_valid:
            return False
        
        if self.passflag:
            self.finishflag = True
        
        self.passflag = True
        return True
    
    def surrender(self, is_user: bool) -> bool:
        ''' This method is for surrender.
        
        :param is_user: if this turn's player is the user, set true,
                        otherwise, set false
        :return: always return true
        '''
        self.finishflag = True
        self.gameresult = GameResult.LOSE if is_user else GameResult.WIN
        return True
    
    def is_finished(self) -> bool:
        ''' This method indicates whether the game is over or not.
        
        :return: if the game is finished, return true,
                 otherwise, return false.
        '''
        return self.finishflag
    
    def set_result(self, is_user: bool, c: Color) -> None:
        ''' This method distinguishes which player wins.
        
        :param is_user: if the user calls this method, set true,
                        otherwise, set false.
        :param c: the color of this turn's player
        '''
        assert self.finishflag == True
        
        black, white = self.board.count()
        print((black, white))
        if black > white:
            if (c == Color.BLACK and is_user) or (c == Color.WHITE and not is_user):
                self.gameresult = GameResult.WIN
            else:
                self.gameresult = GameResult.LOSE
        elif white > black:
            if (c == Color.WHITE and is_user) or (c == Color.BLACK and not is_user):
                self.gameresult = GameResult.WIN
            else:
                self.gameresult = GameResult.LOSE
        else:
            self.gameresult = GameResult.DRAW
    
    def get_result(self) -> GameResult:
        ''' This method returns a game's result
        
        :return: if the user wins, return WIN,
                 if the user loses, return LOSE,
                 if the game is draw, return DRAW
        '''
        assert self.gameresult != None
        return self.gameresult
    
    def get_valid(self, c: Color) -> List:
        ''' This method finds valid squares.
        
        :param c: the color of this turn's player
        :return: a list of tuples that contains coordinates of a valid square
                 and the number of discs flipped over
        '''
        b = self.board.to_color()
        indices = []
        for j in range(0,len(b)):
            for i in range(0,len(b)):
                if b[j][i] == Color.NONE:
                    indices.append((i, j))
        
        valid = []
        for i in indices:
            x, y = i
            n = len(self.board.get_changeable(x + 1, y + 1, c))
            if n > 1:
                valid.append((i, n))
        return valid

class Player:
    ''' This class defines a player.
    '''
    def __init__(self, g: Game, c: Color) -> Player:
        ''' This method create a Player instance.
        
        :param g: a game this player plays
        :param c: a color this player's side is
        :return: a created instance
        '''
        self.game = g
        self.color = c
    
    def put_disc(self, x: int, y: int) -> bool:
        ''' This method puts a disc on the board.
        
        :param x: x coordinate of the putting position
        :param y: y coordinate of the putting position
        :return: if the putting position is valid, return true,
                 otherwise, return false.
        '''
        return self.game.put_disc(x, y, self.color)
    
    def take_pass(self) -> bool:
        ''' This method is for pass.
        
        :return: if this pass is success, return true,
                 otherwise, return false.
        '''
        return self.game.take_pass(self.color)
    
    def surrender(self, is_user: bool) -> bool:
        ''' This method is for surrender.
        
        :param is_user: if this turn's player is the user, set true,
                        otherwise, set false
        :return: always return true
        '''
        return self.game.surrender(is_user)

class Opponent:
    ''' This class defines an opponent player.
    '''
    def __init__(self, g: Game, c: Color) -> Opponent:
        ''' This method creates an instance.
        
        :param g: a given game
        :param c: this player's playing color
        :return: a created instance
        '''
        self.game = g
        self.color = c
        self.player = Player(g, c)
    
    def move(self) -> bool:
        ''' This method lets the opponent player take an action at his turn.
        
        :return: if he puts a disc, return true,
                 if he passes, return false
        '''
        valid = self.game.get_valid(self.color)
        if len(valid) < 1:
            self.player.take_pass()
            return False
        
        max = -1
        x = y = 0
        for i in valid:
            if i[1] > max:
                max = i[1]
                x, y = i[0]
        assert self.player.put_disc(x + 1, y + 1) == True
        return True
