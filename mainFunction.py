from handpose_recognize import *
import sys
import LogIn
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import recognize_character
import preFunction
import mediapipe as mp
import numpy as np
import autopy
import cv2
import myClass

class MyWindow(QMainWindow,LogIn.Ui_LogIn):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.scene = myClass.MyScene(self)
        self.graphicsView.setScene(self.scene)
        self.initail_condition() #初始化

        self.my_thread = MyThread()  
        self.score = 0

        self.pushButton_start.clicked.connect(self.scene.startGame)
        self.pushButton_pause.clicked.connect(self.scene.pauseGame)
        self.pushButton_stop.clicked.connect(self.scene.stopGame)
        self.timer_camera.timeout.connect(self.show_camera)  


    def initail_condition(self):
        self.wScr, self.hScr = autopy.screen.size() #獲取螢幕的長寬比
        self.wCam, self.hCam = 640, 480 #鏡頭的長寬比

        self.smoothening = 5         #移動鼠標
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0

        self.mp_hands = mp.solutions.hands   #mediapipe
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                               max_num_hands=1,   #檢測幾隻手
                               min_detection_confidence=0.7,  #檢測出手的置信度
                               min_tracking_confidence=0.5)   #追蹤是不是同一隻手的置信度
        self.mpDraw = mp.solutions.drawing_utils

        self.cap = cv2.VideoCapture()
        self.timer_camera = QTimer()
        self.timer_camera.start(30)     #定時器，30s一次
        

        self.cap.open(0)
        self.cap.set(3, self.wCam)  # width=1920
        self.cap.set(4, self.hCam)  # height=1080

    def show_camera(self):
        flag, self.image = self.cap.read()  
        h, w, c = self.image.shape[0], self.image.shape[1], self.image.shape[2]
        # print(h,w,c)
        frame = cv2.flip(self.image, 1)
        img_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(img_RGB)  #獲取手的訊息
        if results.multi_hand_landmarks:
            self.mpDraw.draw_landmarks(frame, results.multi_hand_landmarks[0], self.mp_hands.HAND_CONNECTIONS)
            #畫出手

            handpoint_list = hand_point(results, h, w)
            hand_pose = judge_handpose(handpoint_list) 

            if hand_pose == 'Index_up':
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
                index_x, index_y = handpoint_list[8]
                screen_x = np.interp(index_x, (50, self.wCam-100), (0, self.wScr)) #將鏡頭的長寬投射到螢幕的長寬
                screen_y = np.interp(index_y, (50, self.hCam-100), (0, self.hScr))
                self.clocX = self.plocX + (screen_x - self.plocX) / self.smoothening 
                self.clocY = self.plocY + (screen_y - self.plocY) / self.smoothening

                autopy.mouse.move(self.clocX, self.clocY) #鼠標移動
                cv2.circle(frame, (index_x, index_y), 10, (255, 0, 255), cv2.FILLED)
                self.plocX, self.plocY = self.clocX, self.clocY

            elif hand_pose == 'Index_middle_up':
                if p_to_p_distance(handpoint_list[8], handpoint_list[12]) < 50:
                    index_x, index_y = handpoint_list[8]
                    middle_x, middle_y = handpoint_list[12]
                    click_x, click_y = int((index_x + middle_x) / 2), int((index_y + middle_y) / 2)
                    cv2.circle(frame, (click_x, click_y), 10, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)  #點左鍵


        new_width, new_height = preFunction.resize_picture(frame, width=self.label_cap.width(),
                                                           height=self.label_cap.height())
        
        qt_img_detect = preFunction.cvimg_to_qtimg(frame) 
        new_img = qt_img_detect.scaled(new_width, new_height, Qt.KeepAspectRatio)
        self.label_cap.setPixmap(QPixmap.fromImage(new_img))
        self.label_cap.setAlignment(Qt.AlignCenter)  #顯示圖片



    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newLeft = int((screen.width()-size.width())/2)
        newTop = int((screen.height()-size.height())/2-40)
        self.move(newLeft,newTop)  

    def add_shadow(self):
        
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0) 
        self.effect_shadow.setBlurRadius(10)  
        self.effect_shadow.setColor(Qt.gray)  
        self.widget.setGraphicsEffect(self.effect_shadow) 

class MyThread(QThread): 
    my_signal = pyqtSignal(str)  
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MyWindow()
    MainWindow.center()
    MainWindow.add_shadow()
    MainWindow.show()
    sys.exit(app.exec_())