# ==========================================================
# __main__.py
# Copyright (C) 2023 Kei Shioda.  All rights reserved.
# ==========================================================

from reversi.controller import Controller

def main():
    '''This method starts this application.
    '''
    cont = Controller()
    cont.start()

if __name__ == '__main__':
    main()

