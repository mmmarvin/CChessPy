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

class ChessWindowMainMenu(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.m_parent = parent
        
        self.m_game = self.addMenu("Game")
        newGameAction = self.m_game.addAction("New Game")
        newGameAction.triggered.connect(self.m_parent.createNewGame)
        exitAction = self.m_game.addAction("Exit")
        exitAction.triggered.connect(self.m_parent.close)
        
        self.m_multiplayer = self.addMenu("Multiplayer")
        createServerAction = self.m_multiplayer.addAction("Create Game")
        createServerAction.setEnabled(False)
        connectToServerAction = self.m_multiplayer.addAction("Connect...")
        connectToServerAction.setEnabled(False)
        multiplayerRestartGameAction = self.m_multiplayer.addAction("Request Restart")
        multiplayerRestartGameAction.setEnabled(False)
        
        self.m_help = self.addMenu("Help")
        helpAction = self.m_help.addAction("About")
        helpAction.triggered.connect(self.m_parent.showAboutHelp)
        
