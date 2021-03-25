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

imageResources = {}

def loadResources():
    imageResources['k'] = QImage("assets/black-king.png")
    imageResources['q'] = QImage("assets/black-queen.png")
    imageResources['n'] = QImage("assets/black-knight.png")
    imageResources['b'] = QImage("assets/black-bishop.png")
    imageResources['r'] = QImage("assets/black-rook.png")
    imageResources['p'] = QImage("assets/black-pawn.png")
    imageResources['K'] = QImage("assets/white-king.png")
    imageResources['Q'] = QImage("assets/white-queen.png")
    imageResources['N'] = QImage("assets/white-knight.png")
    imageResources['B'] = QImage("assets/white-bishop.png")
    imageResources['R'] = QImage("assets/white-rook.png")
    imageResources['P'] = QImage("assets/white-pawn.png")
