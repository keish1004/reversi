# ==========================================================
# view.py
# Copyright (C) 2023 Kei Shioda.  All rights reserved.
# ==========================================================
''' This module defines view classes composing each screen.
'''
from __future__ import annotations
from abc import ABC, ABCMeta, abstractmethod
from reversi.model import Game, Color, GameResult
import re

class View(metaclass = ABCMeta):
    ''' This class is a abstract class of Views.
    There are another classes below that implements this View class.
    '''
    
    @abstractmethod
    def input(self) -> str:
        pass
    
    @abstractmethod
    def output(self) -> None:
        pass

class MainMenuView(View):
    ''' This class composes the main menu screen.
    '''
    def input(self) -> str:
        ''' This method gets a number of an item the user choose.
        
        :return: a code showing the next state
        '''
        s = ""
        while s != "1" or s != "2":
            s = input()
            if s == "1":
                return "CONFIG"
            elif s == "2":
                return "EXIT"
            else:
                print("your input is invalid.  try again.")
    
    def output(self) -> None:
        ''' This method displays contents of the main menu screen.
        '''
        print("REVERSI")
        print("")
        print("<Main Menu>")
        print("Choose a play mode from items below")
        print("-----------------")
        print("1: New Game")
        print("2: Exit")
        print("-----------------")
        print("(input a number indicating an item you choose): ")

class ConfigView(View):
    ''' This class composes the config screen.
    '''
    def input(self) -> str:
        ''' This method gets user inputs showing playing color.
        
        :return: a code showing the user color or the next state
        '''
        s = ""
        while s != "1" or s != "2":
            s = input()
            match s:
                case "1":
                    return "BLACK"
                case "2":
                    return "WHITE"
                case "3":
                    return "MAINMENU"
                case _:
                    print("your input is invalid.  try again.")

    def output(self) -> None:
        ''' This method displays contents of the config screen.
        '''
        print("<Config>")
        print("choose a color showing your playing side.")
        print("if you want to go back to the main menu, choose 3.")
        print("---------------")
        print("1: Black")
        print("2: White")
        print("3: Main Menu")
        print("---------------")

class GameView(View):
    ''' This class composes the game screen.
    '''
    def __init__(self, g: Game) -> GameView:
        ''' This method creates a new instance.
        
        :param g: a given Game instance
        :return; a created instance
        '''
        self.game = g
    
    def input(self) -> str:
        ''' This method gets user inputs showing an user action.
        
        :return: a code showint the user action
        '''
        s = ""
        while True:
            s = input()
            if re.search("[1-8],[1-8]", s):
                return "PUT," + s
            elif s == "p":
                return "PASS"
            elif s == "s":
                return "SURRENDER"
            else:
                print("your input is invalid.  input correct action.")
        
        
    def output(self, c: Color, is_user: bool) -> None:
        ''' This method displays contents of the game screen.
        
        :param c: this turn's color
        :param is_user: if this turn is the user's, then set true,
                        otherwise, set false.
        '''
        board = self.game.get_board_situation()
        print("<BOARD>")
        print("========================")
        print(" ", end=" ")
        for i in range(len(board)):
            print(i + 1, end=" ")
        print("")
        for j in range(len(board)):
            print(j + 1, end=" ")
            for i in range(len(board[j])):
                match board[j][i]:
                    case Color.BLACK:
                        print("B", end=" ")
                    case Color.WHITE:
                        print("W", end=" ")
                    case _:
                        print("-", end=" ")
            print("")
        print("=======================")
        print("this is " + Color.to_str(c) + " turn")
        
        if is_user:
            print("input characters indicating your action")
            print("----------------------------------------")
            print("x,y: coordinates putting your disc at")
            print("p: pass")
            print("s: surrender")
            print("----------------------------------------")
        else:
            print("the opponent player is thinking now")

class ResultView(View):
    ''' This class indicates the game result
    '''
    def __init__(self, g: Game):
        ''' This method creates a new instance.
        
        :param g: a given Game instance
        :return; a created instance
        '''
        self.game = g
    
    def input(self) -> None:
        ''' This method waits your input.
        '''
        print("push a key")
        input()
    
    def output(self) -> None:
        ''' This method displays the result screen.
        '''
        print("")
        print("<RESULT>")
        match self.game.get_result():
            case GameResult.WIN:
                print("you wins!")
            case GameResult.LOSE:
                print("you loses!")
            case GameResult.DRAW:
                print("the game is draw")
            case _:
                print("ERROR")

class ErrorView:
    ''' This class indicates error messages.
    '''
    MESSAGES = { 1:"your position is invalid.  put on another position",
                 2:"your pass is invalid.  put a disc on a valid position",
                 3:"something wrong has happend"
                }
    
    def input(self):
        pass
    
    def output(self, code:int) -> None:
        ''' This method shows an error message according to the given code.
        
        :param code: an error code to corresponde to a error message
        '''
        print("ERROR: " + self.MESSAGES[code])

