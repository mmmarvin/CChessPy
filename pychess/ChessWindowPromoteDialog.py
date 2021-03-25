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
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ChessWindowPromoteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(10 + (64 + 10) * 4, 64 + 20)
        self.setWindowTitle("Promote Piece")
        self.m_result = b" "
        
        queenButton = QPushButton("Queen", self)
        queenButton.setGeometry(10, 10, 64, 64)
        queenButton.clicked.connect(self.__promoteToQueen)
        
        rookButton = QPushButton("Rook", self)
        rookButton.setGeometry(10 + (10 + 64) * 1, 10, 64, 64)
        rookButton.clicked.connect(self.__promoteToRook)
        
        bishopButton = QPushButton("Bishop", self)
        bishopButton.setGeometry(10 + (10 + 64) * 2, 10, 64, 64)
        bishopButton.clicked.connect(self.__promoteToBishop)
        
        knightButton = QPushButton("Knight", self)
        knightButton.setGeometry(10 + (10 + 64) * 3, 10, 64, 64)
        knightButton.clicked.connect(self.__promoteToKnight)
        
    def getDialogResult(self):
        return self.m_result
    
    def __promoteToQueen(self):
        self.m_result = b"Q"
        self.close()
        
    def __promoteToRook(self):
        self.m_result = b"R"
        self.close()
        
    def __promoteToBishop(self):
        self.m_result = b"B"
        self.close()
        
    def __promoteToKnight(self):
        self.m_result = b"N"
        self.close()
