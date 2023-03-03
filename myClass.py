import operator
from functools import reduce
from random import Random
from PyQt5 import QtWidgets

# 2D顯示容器  QGraphicsView  QGraphicsScene  QGraphicsItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QCursor


# 坐標體系
# 1. 當場景（scene）小於視圖（view）：
#   QGraphicsView的坐標原點在中心點
#   scene的原點也在中心點（我們指定scene的位置，指定的是scene的原點的位置）
# 2. 當場景大於視圖：
#   兩者的坐標原點都在左上角


class MyScene(QtWidgets.QGraphicsScene):   # 場景  坐標原點在中心點
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.bg = QPixmap(r".\img\no_mouse.jpg")
        self.mole = QPixmap(r".\img\mouse_single.jpg")

        self.items = []  # 定義陣列儲存圖源

        self.w = 4      #行數
        self.h = 6      #列數
        for y in range(self.w):
            self.items.append([])
            for x in range(self.h):
                mp = MyPixmapItem(parent)
                mp.setPos(mp.boundingRect().width()*x, mp.boundingRect().height()*y)
                self.addItem(mp)
                self.items[y].append(mp)

        self.count = 30

        self.timer = QTimer()
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.Refresh)
        self.timer.timeout.connect(self.showMole)

    def startGame(self):
        self.timer.start(2000)
        self.timer2.start(1000)
        for item in reduce(operator.add, self.items):
            item.start = True

    def pauseGame(self):
        self.timer.stop()
        for item in reduce(operator.add, self.items):
            item.start = False

    def stopGame(self):
        for item in reduce(operator.add, self.items):
            item.setPixmap(self.bg)
            item.isMole = False
            item.start = False
        self.timer.stop()
        self.parent.score = 0
        self.parent.lcdNumber_score.display(self.parent.score)

    def showMole(self):
        for item in reduce(operator.add, self.items):
            item.setPixmap(self.bg)
            item.isMole = False

        for i in range(Random().randint(1, 3)):
            x = Random().randint(0, self.h - 1)
            y = Random().randint(0, self.w -1)
            self.items[y][x].setPixmap(QPixmap(self.mole))
            self.items[y][x].isMole = True

    def Refresh(self):
        if self.count > 0:
            self.parent.lcdNumber_time.display(self.count)
            self.count -= 1
        else:
            self.timer2.stop()
            QtWidgets.QMessageBox.information(self.parent,'提示','time out,score:' + str(self.parent.score))
            self.count = 30
            for item in reduce(operator.add, self.items):
                item.setPixmap(self.bg)
                item.isMole = False
                item.start = False
            self.timer.stop()
            self.parent.score = 0
            self.parent.lcdNumber_score.display(self.parent.score)


class MyPixmapItem(QtWidgets.QGraphicsPixmapItem):      # 像素 圖源
    def __init__(self, parent):
        super().__init__()
        self.setPixmap(QPixmap(r".\img\no_mouse.jpg"))
        self.setCursor(QCursor(QPixmap("./img/hammer_up.png")))

        self.parent = parent

        self.__isMole = False       # 標示圖片是否是老鼠
        self.__start = False        # 標示遊戲是否正在進行中

    @property
    def isMole(self):
        return self.__isMole

    @isMole.setter
    def isMole(self,value):
        self.__isMole = value

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    def mousePressEvent(self, event):
      
        self.setCursor(QCursor(QPixmap('./img/hammer_down.png')))
        if self.__start:
            if self.__isMole == True:
                self.__isMole = False
               
                self.parent.score += 10
                self.setPixmap(QPixmap(r".\img\mouse_killed.png"))
                self.parent.lcdNumber_score.display(self.parent.score)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.setCursor(QCursor(QPixmap("./img/hammer_up.png")))
