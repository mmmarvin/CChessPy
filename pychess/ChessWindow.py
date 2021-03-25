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
import time
import socket

from pychess import BoardRect
from pychess import ChessWindowMainMenu

from pychess import ChessWindowHelpDialog
from pychess import ChessWindowNewGameDialog
from pychess import ChessWindowPromoteDialog

from pychess import define
from pychess import resources

class ChessWindow(QWidget):
    HS_HELLO_MSG = b"\x1A\x1D\0"
    HS_HI_MSG = b"\x1C\x1A\0"
    HS_HI_ACCEPT_MSG = b"\x21\x2D\0"
            
    def __init__(self, windowTitle, port):
        super().__init__()
        self.m_mainMenu = ChessWindowMainMenu.ChessWindowMainMenu(self)

        # Updates 10 per second        
        self.m_timer = QTimer(self)
        self.m_timer.timeout.connect(self.__update)
        self.m_timer.setInterval(100)
        self.m_timer.start()
        
        self.setWindowTitle("")
        self.setFixedSize((64 * 8) + define.TIME_LAYOUT_WIDTH + define.CAPTURE_LAYOUT_WIDTH + define.CHAT_LAYOUT_WIDTH + 20, (64 * 8) + self.m_mainMenu.geometry().height() - 5)
        self.m_board = []
        self.m_fromSquare = None        
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_socket.connect(("localhost", port))
        
        self.m_playerName = "Player"
        self.m_chatHistoryStr = []
        
        self.m_turn = 0
        self.m_whiteTimeLeft = 0
        self.m_blackTimeLeft = 0

        self.m_whiteCaptured = []
        self.m_blackCaptured = []
        
        # Create chat elements
        self.m_chatHistory = QTextEdit(self)
        self.m_chatHistory.setGeometry(self.geometry().width() - define.CHAT_LAYOUT_WIDTH - 5, self.m_mainMenu.geometry().height() - 5, define.CHAT_LAYOUT_WIDTH, self.geometry().height() - self.m_mainMenu.geometry().height() - 5 - 25)
        self.m_chatHistory.setReadOnly(True)
        self.m_chat = QLineEdit(self)
        self.m_chat.setGeometry(self.geometry().width() - define.CHAT_LAYOUT_WIDTH - 5, self.geometry().height() - 25 - 5, define.CHAT_LAYOUT_WIDTH, 25)
        self.m_chat.setMaxLength(define.MAX_CHAT_MSG_LENGTH)
        self.m_chat.setFocus(True)
        self.m_chat.returnPressed.connect(self.__chatReturnPressed)
        
        # Send a hello message to the server
        count = self.m_socket.send(self.HS_HELLO_MSG)
        if count == 0:
            raise RuntimeError("Invalid handshake with display server")
        
        # Read hi message from server
        buff = self.m_socket.recv(255)
        if len(buff) != 3 or buff != self.HS_HI_MSG:
            raise RuntimeError("Invalid handshake with display server")
            
        # Send back a hi confirmation to server
        count = self.m_socket.send(self.HS_HI_ACCEPT_MSG)
        if count == 0:
            raise RuntimeError("Invalid handshake with display server")
            
        # Request the version from the display server
        gameVersion = self.m_socket.recv(255)
        if len(gameVersion) == 0:
            raise RuntimeError("Invalid handshake with display server")
        self.setWindowTitle(windowTitle + " v." + gameVersion.decode("utf-8"))
        
        # Request the display server for the board pieces information
        buff = self.__requestBoardPieceInformation()
            
        # Create the board
        c = 0
        p = 0
        for j in range(0, 8):
            self.m_board.append([])
            for i in range(0, 8):
                x = i * 64
                y = j * 64
                
                if(c % 2 == 0):
                    rect = BoardRect.BoardRect(self, buff[p], x + define.TIME_LAYOUT_WIDTH, y + self.m_mainMenu.geometry().height() - 5, 64, 64, QColor(128, 64, 0, 255))
                    self.m_board[len(self.m_board) - 1].append(rect)
                else:
                    rect = BoardRect.BoardRect(self, buff[p], x + define.TIME_LAYOUT_WIDTH, y + self.m_mainMenu.geometry().height() - 5, 64, 64, QColor(254, 235, 216))
                    self.m_board[len(self.m_board) - 1].append(rect)
                p = p + 1
                c = c + 1
            c = c + 1
    
    def __chatReturnPressed(self):
        self.m_chatHistoryStr.append(self.m_playerName + ": " + self.m_chat.text() + "\n")
        while len(self.m_chatHistoryStr) >= define.MAX_CHAT_HISTORY_COUNT:
            self.m_chatHistoryStr.pop(0)
        
        self.m_chatHistory.clear()
        for l in self.m_chatHistoryStr:
            self.m_chatHistory.setText(self.m_chatHistory.toPlainText() + l)
        self.m_chat.setText("")
        
    def __requestCapturedPiecesInformation(self):
        count = self.m_socket.send(b"l")
        if count == 0:
            raise RuntimeError("Cannot send request for game piece position to display server")
            
        captured = self.m_socket.recv(255)
        if len(captured) == 0 :
            raise RuntimeError("Cannot load game piece positions from display server")
        
        (_, whiteCaptured, blackCaptured) = captured.decode("utf-8").split('s')        
        return (bytes(whiteCaptured, "utf-8"), bytes(blackCaptured, "utf-8"))
            
    def __requestBoardPieceInformation(self):
        count = self.m_socket.send(b"d")
        if count == 0:
            raise RuntimeError("Cannot send request for game piece position to display server")
        
        buff = self.m_socket.recv(255)
        if len(buff) == 0 or len(buff) != 64:
            raise RuntimeError("Cannot load game piece positions from display server")
            
        return buff
            
    def __resetGameBoard(self):
        self.m_fromSquare = None
        buff = self.__requestBoardPieceInformation()

        index = 0
        for j in range(0, 8):
            for i in range(0, 8):
                self.m_board[j][i].setPieceType(buff[index])
                index = index + 1
            
#    def __changePieceOnSquare(self, toSquare):
#        self.m_fromSquare.swap(toSquare)
#        
#    def __changePieceOnSquareToEmpty(self, toSquare):
#        self.m_fromSquare.swapToEmpty(toSquare)
            
    def __resetSelectedSquares(self):
        self.m_fromSquare.returnColor()
        self.m_fromSquare = None
        
    def __updateCapturedPieces(self):
        (whiteCaptured, blackCaptured) = self.__requestCapturedPiecesInformation()
                
        self.m_whiteCaptured.clear()
        self.m_blackCaptured.clear()
        
        for i in range(0, len(whiteCaptured)):
            c = chr(whiteCaptured[i])
            self.m_whiteCaptured.append(resources.imageResources[str(c)])
            
        for i in range(0, len(blackCaptured)):
            c = chr(blackCaptured[i])
            self.m_blackCaptured.append(resources.imageResources[str(c)])

        self.update()
        
    def __update(self):
        count = self.m_socket.send(b"u")
        if count == 0:
            raise RuntimeError("Cannot send command to display server")

        buff = self.m_socket.recv(255)
        if len(buff) == 0:
            raise RuntimeError("Cannot read command from display server")
                        
        (whiteTimeLeftStr, blackTimeLeftStr) = buff.decode("utf-8").split(' ')
        self.m_whiteTimeLeft = int(whiteTimeLeftStr)
        self.m_blackTimeLeft = int(blackTimeLeftStr)
        self.update()
        
    def __changeTurns(self):
        if self.m_turn == 0:
            self.m_turn = 1
        else:
            self.m_turn = 0
            
    def  __requestPromote(self, sender):
        r = b" "
        while True:
            # show promote dialog
            promoteDialog = ChessWindowPromoteDialog.ChessWindowPromoteDialog()
            promoteDialog.setModal(True)
            promoteDialog.exec()
            r = promoteDialog.getDialogResult()
            
            # send the piece to promote to
            count = self.m_socket.send(b"pr " + r)
            if count == 0:
                raise RuntimeError("Cannot send command to display server")
            
            # read server's reply
            buff = self.m_socket.recv(255)
            if len(buff) == 0:
                raise RuntimeError("Cannot read command from display server")
            
            # if the server's reply is ok, exit. else, keep asking the client
            # what piece to promote to
            if buff == b"ok":
                break
            elif buff == b"np":
                r = b" "
                break;

        return r
    
    def __restartGame(self, timed):
        count = 0
        if timed == True:
            count = self.m_socket.send(b"rt")
        else:
            count = self.m_socket.send(b"rn")
            
        if count == 0:
            raise RuntimeError("Cannot send command to display server")
            
        buff = self.m_socket.recv(255)
        if len(buff) == 0:
            raise RuntimeError("Cannot read command from display server")
            
        if buff == b"ok":
            self.__resetGameBoard()
            self.m_turn = 0
            self.m_whiteCaptured.clear()
            self.m_blackCaptured.clear()
        
    def showAboutHelp(self):
        windowHelp = ChessWindowHelpDialog.ChessWindowHelpDialog()
        windowHelp.setModal(True)
        windowHelp.exec()
        
    def close(self):
        self.m_socket.send(b"e")
        super().close()
                    
    def createNewGame(self):
        newGameDialog = ChessWindowNewGameDialog.ChessWindowNewGameDialog()
        newGameDialog.setModal(True)
        newGameDialog.exec()
        dr = newGameDialog.getDialogResult()
        if dr == -1:
            return
        elif dr == 0:
            self.__restartGame(True)
        elif dr == 1:
            self.__restartGame(False)
            
    def selectSquare(self, sender, x, y):
        # send a select request to display server
        count = self.m_socket.send(bytes("s " + str(int(x)) + " " + str(int(y)), "utf-8"))
        if count == 0:
            raise RuntimeError("Cannot send command to display server")
            
        # wait for answer from display server
        buff = self.m_socket.recv(255)
        if len(buff) == 0:
            raise RuntimeError("Cannot read command from display server")
            
        if buff == b"ca":
            sender.returnColor()
            
        elif buff == b"pm":
            sender.setColor(Qt.green)
            self.m_fromSquare = sender
            
        elif buff == b"00":
            self.__resetSelectedSquares()
        
        elif buff == b"ok":
#            self.__changePieceOnSquare(sender)
            self.__resetSelectedSquares()
            self.__changeTurns()
            self.__resetGameBoard()
            
        elif buff == b"okw":
#            self.__changePieceOnSquare(sender)
            self.__resetSelectedSquares()
            self.__changeTurns()
            r = self.__requestPromote(sender)
            sender.m_type = r
            self.__resetGameBoard()
            
        elif buff == b"co":
#            self.__changePieceOnSquareToEmpty(sender)
            self.__resetSelectedSquares()
            self.__updateCapturedPieces()
            self.__changeTurns()
            self.__resetGameBoard()
            
        elif buff == b"cow":
#            self.__changePieceOnSquareToEmpty(sender)
            self.__resetSelectedSquares()
            self.__updateCapturedPieces()
            self.__changeTurns()
            r = self.__requestPromote(sender)
            sender.m_type = r
            self.__resetGameBoard()
                
    def paintEvent(self, event):
        painter = QPainter(self)

        # setup font
        font = painter.font()
        font.setPixelSize(15)
        painter.setFont(font)

        #draw time
        sx = 25
        sy = ((self.geometry().height() - self.m_mainMenu.geometry().height() + 5) / 2)
        painter.drawText(QRectF(sx, sy, define.TIME_LAYOUT_WIDTH - 50, 25), 0, "Time:")

        if self.m_turn == 0:
            timeStr = time.strftime("%M:%S", time.gmtime(self.m_whiteTimeLeft))
            painter.drawText(QRectF(sx, sy + 25, define.TIME_LAYOUT_WIDTH - 50, 25), 0, timeStr)
        else:
            timeStr = time.strftime("%M:%S", time.gmtime(self.m_blackTimeLeft))
            painter.drawText(QRectF(sx, sy + 25, define.TIME_LAYOUT_WIDTH - 50, 25), 0, timeStr)

        #draw the captured white pieces
        sx = self.geometry().width() - define.CAPTURE_LAYOUT_WIDTH - define.CHAT_LAYOUT_WIDTH - 20 + 10
        sy = (self.m_mainMenu.geometry().height() - 5) + 30

        x = sx
        y = sy - 25
        painter.drawText(QRectF(x, y, define.CAPTURE_LAYOUT_WIDTH, 25), 0, "White Captured:")

        x = sx
        y = sy
        for image in self.m_whiteCaptured:
            painter.drawImage(QRectF(x, y, 32.0, 32.0), image, QRectF(0.0, 0.0, 64.0, 64.0))
            x = x + 32
            if x >= self.geometry().width() - 32 - define.CHAT_LAYOUT_WIDTH - 10:
                y = y + 32
                x = sx

        # draw the captured black pieces
        sy = ((self.geometry().height() - self.m_mainMenu.geometry().height() + 5) / 2) + 30
        
        x = sx
        y = sy - 25
        painter.drawText(QRectF(x, y, define.CAPTURE_LAYOUT_WIDTH, 25), 0, "Black Captured:")
        
        x = sx
        y = sy
        for image in self.m_blackCaptured:
            painter.drawImage(QRectF(x, y, 32.0, 32.0), image, QRectF(0.0, 0.0, 64.0, 64.0))
            x = x + 32
            if x >= self.geometry().width() - 32 - define.CHAT_LAYOUT_WIDTH - 10:
                y = y + 32
                x = sx
