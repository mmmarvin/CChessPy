##################
#
#    Copyright (C) 2019 Marvin Manese
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
# 
##################
import os
import sys
import subprocess
from PyQt5.QtWidgets import *

from pychess import ChessWindow
from pychess import define
from pychess import resources

def main():
    # Load the game resources
    resources.loadResources()
    
    # Run the chess engine
    subprocess.Popen(["./chess-engine", "-ds", "1234"], stdout=subprocess.PIPE)
    
    # Create interface for chess engine
    app = QApplication([])
    window = ChessWindow.ChessWindow("CChess Client v." + str(define.CLIENT_VERSION_MAJOR) + "." + str(define.CLIENT_VERSION_MINOR) + str(define.CLIENT_VERSION_PATCH) + " Engine ", 1234)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
