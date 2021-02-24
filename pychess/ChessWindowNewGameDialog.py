################
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>. 
#
################
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

class ChessWindowNewGameDialog(QDialog):
    def __init__(self):
        super().__init__()
        super().setFixedSize(170, 130)
        self.setWindowTitle("Choose Game Type")
        self.m_result = -1
        
        nonTimedGameButton = QPushButton("Casual Game", self)
        nonTimedGameButton.setGeometry(10, 10, 150, 50)
        nonTimedGameButton.clicked.connect(self.__newCasualGame)
        
        timedGameButton = QPushButton("Timed Game", self)
        timedGameButton.setGeometry(10, 10 + 50 + 10, 150, 50)
        timedGameButton.clicked.connect(self.__newTimedGame)
        
    def __newTimedGame(self):
        self.m_result = 0
        self.close()
        
    def __newCasualGame(self):
        self.m_result = 1
        self.close()

    def getDialogResult(self):
        return self.m_result
                
    def paintEvent(self, event):
        painter = QPainter(self)
