# ==========================================================
# controller.py
# Copyright (C) 2023 Kei Shioda.  All rights reserved.
# ==========================================================
''' This module defines controllers.
'''
from reversi.view import MainMenuView, ConfigView, GameView, ResultView, ErrorView
from reversi.model import State, Color, Game, Player, Opponent
import time

class Controller:
    ''' This class controlls contents of screen and manipulates items 
    of the model module.
    '''
    DURATION_TIME = 1
    
    def __init__(self):
        ''' This is a constructer of the Controller class.
        '''
        self.mainmenuview = MainMenuView()
        self.configview = ConfigView()
        self.errorview = ErrorView()
        self.state = State.START
    
    def start(self) -> None:
        ''' This method takes actions according to the current state.
        '''
        self.state = State.MAINMENU
        while self.state is not State.EXIT:
            match self.state:
                case State.MAINMENU:
                    self.state = self._do_mainmenu_case()
                case State.CONFIG:
                    self.state = self._do_config_case()
                case State.GAMESTART:
                    self.state = self._make_game()
                case State.USER:
                    self.state = self._do_user_turn()
                case State.OPPONENT:
                    self.state = self._do_opponent_turn()
                case State.RESULT:
                    self.state = self._do_result_case()
                case State.EXIT:
                    break
                case _:
                    self.state = self._do_error_case()
        print("Good bye!")
    
    def _do_mainmenu_case(self) -> State:
        self.mainmenuview.output()
        match self.mainmenuview.input():
            case "CONFIG":
                return State.CONFIG
            case "EXIT":
                return State.EXIT
            case _:
                return State.ERROR
    
    def _do_config_case(self) -> State:
        self.configview.output()
        match self.configview.input():
            case "BLACK":
                self.usercolor = Color.BLACK
                return State.GAMESTART
            case "WHITE":
                self.usercolor = Color.WHITE
                return State.GAMESTART
            case "MAINMENU":
                return State.MAINMENU
            case _:
                return State.ERROR
    
    def _make_game(self) -> State:
        self.game = Game()
        self.user = Player(self.game, self.usercolor)
        self.opponent = Opponent(self.game, Color.get_opponent(self.usercolor))
        self.gameview = GameView(self.game)
        self.resultview = ResultView(self.game)
        
        return State.USER if self.usercolor == Color.BLACK else State.OPPONENT
    
    def _do_user_turn(self) -> State:
        self.gameview.output(self.usercolor, True)
        while True:
            s = self.gameview.input()
            match s.split(",")[0]:
                case "PUT":
                    c, x, y = s.split(",")
                    if int(x) > 0 and int(x) < 9 and int(y) > 0 and int(y) < 9 and self.user.put_disc(int(x), int(y)):
                        return State.OPPONENT
                    else:
                        self.errorview.output(1)
                case "PASS":
                    if self.user.take_pass():
                        if self.game.is_finished():
                            self.game.set_result(True, self.usercolor)
                            return State.RESULT
                        return State.OPPONENT
                    else:
                        self.errorview.output(2)
                case "SURRENDER":
                    self.user.surrender(True)
                    return State.RESULT
                case _:
                    return State.ERRROR
    
    def _do_opponent_turn(self) -> State:
        self.gameview.output(Color.get_opponent(self.usercolor), False)
        time.sleep(self.DURATION_TIME)
        if self.opponent.move():
            return State.USER
        else:
            if self.game.is_finished():
                self.game.set_result(False, Color.get_opponent(self.usercolor))
                return State.RESULT
            return State.USER
                
    
    def _do_result_case(self) -> State:
        self.resultview.output()
        self.resultview.input()
        return State.MAINMENU
    
    def _do_error_case(self) -> State:
        self.errorview.output(3)
        return State.EXIT
