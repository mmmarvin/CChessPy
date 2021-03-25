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

class ChessWindowHelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        super().setFixedSize(50 + 300, 50 + 175)
        self.setWindowTitle("CChess About")
        okButton = QPushButton("Close", self)
        okButton.setGeometry((self.geometry().width() / 2) - 35, self.geometry().height() - 60, 70, 40)
        okButton.clicked.connect(self.close)
                    
    def paintEvent(self, event):
        painter = QPainter(self)
        font = painter.font()
        font.setPixelSize(15)
        painter.setFont(font)
        
        painter.drawText(QRectF(25, 25, 300, 125), Qt.AlignCenter, "CChess chess engine developed by\nMarvin Manese\n\nCChessPy interface developed by\nMarvin Manese\n\nCopyright(c) 2019")
        
        return
