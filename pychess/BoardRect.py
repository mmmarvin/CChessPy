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

from pychess import define
from pychess import resources

class BoardRect(QWidget):
    def __init__(self, parent, pieceType, x, y, width, height, color):
        super().__init__(parent)
        super().setGeometry(x, y, width, height)
        
        self.m_parent = parent
        self.m_type = chr(pieceType)
        self.m_x = x
        self.m_y = y
        self.m_width = width
        self.m_height = height
        self.m_color = color
        self.m_tempColor = color
        self.m_image = None
        
        self.__setPieceImage()
        
    def __setPieceImage(self):
        if self.m_type == " ":
            self.m_image = None
        else:
            self.m_image = resources.imageResources[str(self.m_type)]
        
    def setPieceType(self, pieceType):
        self.m_type = chr(pieceType)
        self.__setPieceImage()
        self.update()
        
#    def swap(self, other):
#        self.m_type, other.m_type = other.m_type, self.m_type
#        self.__setPieceImage()
#        other.__setPieceImage()
#        
#        self.update()
#        other.update()
#        
#    def swapToEmpty(self, other):
#        other.m_type = self.m_type
#        self.m_type = " "
#        
#        self.__setPieceImage()
#        other.__setPieceImage()
#        
#        self.update()
#        other.update()
        
    def setColor(self, color):
        self.m_color = color
        self.update()
        
    def returnColor(self):
        self.m_color = self.m_tempColor
        self.update()
                
    def paintEvent(self, event):
        painter = QPainter(self)
        
        rect = QRect(0, 0, self.m_width, self.m_height)
        painter.fillRect(rect, self.m_color)
        
        if not self.m_image == None:
            painter.drawImage(QRectF(0.0, 0.0, 64.0, 64.0), self.m_image, QRectF(0.0, 0.0, 64.0, 64.0))
                
    def mousePressEvent(self, event):
        self.m_parent.selectSquare(self, (self.m_x - define.TIME_LAYOUT_WIDTH) / 64, self.m_y / 64)
