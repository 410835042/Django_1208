import mediapipe as mp
import cv2
import numpy as np
import uuid  # 通用唯一辨識碼，生成一個隨機字符串，用到圖像(名稱)上。因此當在抓取實際圖像時，不會重疊。
import os
import math
import eel
import random
from matplotlib import pyplot as plt
mp_drawing = mp.solutions.drawing_utils  # 繪製方法、工具。將座標繪製到螢幕上
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式。匯入手模型
mp_hands = mp.solutions.hands  # mediapipe 偵測手掌方法

eel.init('templates')


@eel.expose
def ran_int():
    return random.randint(0, 100)


eel.start('3d_js.html')


def draw_fingertip_coordinate(image, results):  # 畫指底座標
    # Loop through hands
    joint_list1 = [[3], [5], [9], [13], [17]]
    if (cv2.waitKey(10) & 0xFF == ord('a')):
        print_hand_length(results)
    else:
        for hand in results.multi_hand_landmarks:
            # Loop through joint sets
            for joint in joint_list1:
                a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])  # First coord 指尖
                # 顯示座標
                cv2.putText(image, str(round(a[0], 2)) + " ," + str(round(a[1], 2)),
                            tuple(np.multiply(a, [1250, 600]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return image


def print_hand_length(results):
    joint_list1 = [[5], [9]]  # 量指寬
    joint_list2 = [[9], [12]]  # 量指長
    joint_list3 = [[0], [9]]  # 量手掌高度
    joint_list4 = [[5], [17]]  # 量手掌寬度
    subX = subY = subA = subB = subC = subD = subE = subF = 0.00
    for hand in results.multi_hand_landmarks:
        # Loop through joint sets
        for joint in joint_list1:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            subX = abs(subX - round(a[0], 2))
            subY = abs(subY - round(a[1], 2))
        for joint in joint_list2:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            subE = abs(subE - round(a[0], 2))
            subF = abs(subF - round(a[1], 2))
        for joint in joint_list3:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            subA = abs(subA - round(a[0], 2))
            subB = abs(subB - round(a[1], 2))
        for joint in joint_list4:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            subC = abs(subC - round(a[0], 2))
            subD = abs(subD - round(a[1], 2))
    XY2 = round(math.sqrt(pow(subX, 2)+pow(subY, 2)), 2)
    EF2 = round(math.sqrt(pow(subE, 2) + pow(subF, 2)), 2)
    AB2 = round(math.sqrt(pow(subA, 2)+pow(subB, 2)), 2)
    CD2 = round(math.sqrt(pow(subC, 2) + pow(subD, 2)), 2)
    print("finger width size:" + str(XY2 * 34.5) + "cm")
    print("middle finger length:" + str((EF2 * 34.5)-2.0) + "cm")
    print("palm height:" + str((AB2 * 34.5)-1.5) + "cm")
    print("palm width:" + str((CD2 * 34.5)+1.5) + "cm")


def get_label(image, index, hand, results):  # index:檢測的數量, hand: 手部landmark參數
    output = None  # output: 此函數的結果推出的最終變數
    for idx, classification in enumerate(results.multi_handedness):  # results.multi_handedness: 用score來檢測是右手或左手
        if classification.classification[0].index == index:
            # process results
            label = classification.classification[0].label  # 輸出"左手"或"右手"
            score = classification.classification[0].score  # 左右手的score(信心程度)
            text = '{} {}'.format(label, round(score, 2))
            #print(text)  # 印出信心值
            # 提取真正想要渲染的座標
            coords = tuple(np.multiply(np.array((  # 存進numpy的array
            hand.landmark[mp_hands.HandLandmark.WRIST].x,  # hand:抓取hand results, landmark:抓取地標, WRIST: 通過手腕
            hand.landmark[mp_hands.HandLandmark.WRIST].y)),  # 獲取x和y的座標
            [800, 400]).astype(int))  # 網路攝影鏡頭的尺寸(?)
            # output = text, coords
            cv2.putText(image, text, coords, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # return output  # 回傳"左(右)手", score, xy座標


def draw_finger_angles(image, results):  # image:正在使用的鏡頭影像  # joint_list:一組array
    joint_list = [[7, 6, 5], [11, 10, 9], [15, 14, 13], [19, 18, 17]]  # joint:關節，該變數儲存要渲染的關節組合，數字為手指關節，三個合起來就是一根手指
    for hand in results.multi_hand_landmarks:  # 每隻手
        total_angle = 0.0
        for joint in joint_list:  # 每個關節組
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])  # 第一關節
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])  # 第二關節
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])  # 第三關節
            # hand = results.multi._hand_landmarks[0] # 偵測到的第一張圖的手座標
            # joint = joint_list[1]  # 偵測到的第二個關節組
            # print(hand.landmark[joint[1]].x, hand.landmark[joint[1]].y)
            radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1] - b[1], a[0]-b[0])  #
            # cv2.putText:在圖片上加上文字。cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
            # arctan2：計算弧度的數學工具
            angle = np.abs(radians*180.0/np.pi)
            if angle > 180.0:  # 讓角度不大於180度，若大於就轉換
                angle = 360-angle
            total_angle = total_angle + angle
            cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (61, 97, 5), 2, cv2.LINE_AA)
    return image


def run_all():
    cap = cv2.VideoCapture(0)  # 建立一個VideoCapture物件，物件會連接到一隻網路攝影機，0代表第一支攝影機

    # 用攝像頭即時拍照傳到後台(即時攝影)
    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:  # 啟動偵測和追蹤
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        # with跟try catch差不多，用於異常處理
        # 最大手數=2；最小置信度值(0.8)，被認為是成功的檢測
        while True:  # 原本是while cap.isOpened()，怕一直判斷會拖慢速度
            ret, frame = cap.read()
            # 每次呼叫cap.read()就會讀取一張畫面，第一個傳回值ret代表成功與否（True成功False失敗)，第二個傳回值frame是攝影機的單張畫面。
            if not ret:
                print("Cannot receive frame")
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR轉RGB #轉換顏色設定順序：mediapipe讀法為bgr python為rgb
            image = cv2.flip(image, 1)  # 螢幕左右翻轉
            image.flags.writeable = False  # 為了提高效率，將圖像標記改為不可寫入模式
            results = hands.process(image)  # 在圖像上偵測和追蹤，results就是偵測和追蹤的結果(result會記錄手部關節點的位置(xy軸)和關節點編號)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 以下三行為渲染結果
            if results.multi_hand_landmarks:  # 檢查手座標是否有輸出
                for num, hand in enumerate(results.multi_hand_landmarks):  # num:左手是0右手是1。hand是21個關節點的座標
                    mp_drawing.draw_landmarks(
                        image, hand, mp_hands.HAND_CONNECTIONS,  # 在圖像上實際繪製landmark(改解釋)
                        mp_drawing.DrawingSpec(color=(121, 87, 76), thickness=1, circle_radius=4),  # 關節點顏色 color:(藍，綠，紅)
                        mp_drawing.DrawingSpec(color=(255, 255, 25), thickness=2, circle_radius=2),  # 關節顏色
                    )
                    # print(num)  # 判斷左或右手(雖然不太準)
                    if get_label(image, num, hand, results):
                        get_label(num, hand, results)
                        # cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    # 大小字體一致, 字體顏色, 大小, 類型

                draw_fingertip_coordinate(image, results)
                draw_finger_angles(image, results)

            cv2.imshow("Hand Tracking", image)  # 開新視窗顯示圖片
            if (cv2.waitKey(10) & 0xFF == ord('q')):  # 按鍵盤Q跳出循環
                break

    cap.release()  # 把攝像頭和彈出視窗一併關掉
    cv2.destroyAllWindows()



