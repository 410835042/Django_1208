import mediapipe as mp
import cv2
import numpy as np
import math
import pyautogui as pag
mp_drawing = mp.solutions.drawing_utils  # 繪製方法、工具。將座標繪製到螢幕上
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式。匯入手模型
mp_hands = mp.solutions.hands  # mediapipe 偵測手掌方法


def convert_coord(results):  # 將手掌中心在視窗內座標轉換成螢幕座標
    joint_list1 = [[0], [5]]
    b = np.array([])
    for hand in results.multi_hand_landmarks:
        # Loop through joint sets
        for joint in joint_list1:
            a = np.array([2559*hand.landmark[joint[0]].x, 1439*hand.landmark[joint[0]].y])
            b = np.concatenate([b, a])
    c = np.array([(b[0]+b[2])/2, (b[1]+b[3])/2])
    return c


def vector_2d_angle(v1, v2):  # 根據兩點的座標，計算角度
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_


def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list


def hand_pos(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度
    a = convert_coord(results)
    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        pag.moveTo(a[0], a[1])  # 滑鼠移動
        return 'good'
    elif f1 >= 50 and f2 >= 50 and f3 < 50 and f4 < 50 and f5 < 50:
        pag.dragTo(a[0], a[1], 0.5, button='left')
        return 'ok'
    elif f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        pag.click(a[0], a[1], button='left', duration=0.5)  # 左鍵點擊
        return '0'
    elif f1 >= 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        pag.PAUSE = 0.7
        pag.press('tab')
        pag.PAUSE = 0.1
        return '1'
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        pag.PAUSE = 0.7
        pag.hotkey('shift', 'tab')
        pag.PAUSE = 0.1
        return '2'
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 > 50:
        pag.press('enter')
        return '3'
    else:
        return ''


def draw_fingertip_coordinate(image, results):  # 畫指底座標
    # Loop through hands
    joint_list1 = [[4], [8], [12], [16], [20]]
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
    print("finger width size:" + str(XY2 * 100) + "cm")  # 假設手距離鏡頭100公分
    print("middle finger length:" + str((EF2 * 100)-2.0) + "cm")
    print("palm height:" + str((AB2 * 100)-1.5) + "cm")
    print("palm width:" + str((CD2 * 100)+1.5) + "cm")


def get_label(index, hand, results):  # index:檢測的數量, hand: 手部landmark參數
    output = None  # output: 此函數的結果推出的最終變數
    for idx, classification in enumerate(results.multi_handedness):  # results.multi_handedness: 用score來檢測是右手或左手
        if classification.classification[0].index == index:
            # process results
            label = classification.classification[0].label  # 輸出"左手"或"右手"
            score = classification.classification[0].score  # 左右手的score(信心程度)
            text = '{} {}'.format(label, round(score, 2))
            # 提取真正想要渲染的座標
            coords = tuple(np.multiply(np.array((  # 存進numpy的array
            hand.landmark[mp_hands.HandLandmark.WRIST].x,  # hand:抓取hand results, landmark:抓取地標, WRIST: 通過手腕
            hand.landmark[mp_hands.HandLandmark.WRIST].y)),  # 獲取x和y的座標
            [800, 400]).astype(int))  # 網路攝影鏡頭的尺寸(?)


cap = cv2.VideoCapture(0)  # 建立一個VideoCapture物件，物件會連接到一隻網路攝影機，0代表第一支攝影機

# 用攝像頭即時拍照傳到後台(即時攝影)
with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:  # 啟動偵測和追蹤
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    w, h = 800, 600
    # with跟try catch差不多，用於異常處理
    # 最大手數=2；最小置信度值(0.8)，被認為是成功的檢測
    while True:  # 原本是while cap.isOpened()，怕一直判斷會拖慢速度
        ret, frame = cap.read()
        image = cv2.resize(frame, (w, h))
        # 每次呼叫cap.read()就會讀取一張畫面，第一個傳回值ret代表成功與否（True成功False失敗)，第二個傳回值frame是攝影機的單張畫面。
        if not ret:
            print("Cannot receive frame")
            break
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR轉RGB #轉換顏色設定順序：mediapipe讀法為bgr python為rgb
        image = cv2.flip(image, 1)  # 螢幕左右翻轉
        image.flags.writeable = False  # 為了提高效率，將圖像標記改為不可寫入模式
        results = hands.process(image)  # 在圖像上偵測和追蹤手勢，results就是偵測和追蹤的結果(result會記錄手部關節點的位置(xy軸)和關節點編號)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (w, h))

        # 以下三行為渲染結果
        if results.multi_hand_landmarks:  # 檢查手座標是否有輸出
            for num, hand in enumerate(results.multi_hand_landmarks):  # num:左手是0右手是1。hand是21個關節點的座標
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,  # 在圖像上實際繪製landmark(改解釋)
                mp_drawing.DrawingSpec(color=(121, 87, 76), thickness=1, circle_radius=4),  # 關節點顏色color:(藍，綠，紅)
                mp_drawing.DrawingSpec(color=(255, 255, 25), thickness=2, circle_radius=2),  # 關節顏色
                )

                # ----手指角度-----
                finger_points = []  # 記錄手指節點座標的串列
                for i in hand.landmark:
                    # 將 21 個節點換算成座標，記錄到 finger_points
                    x = i.x * w
                    y = i.y * h
                    finger_points.append((x, y))
                if finger_points:
                    finger_angle = hand_angle(finger_points)  # 計算手指角度，回傳長度為 5 的串列
                    text = hand_pos(finger_angle)  # 取得手勢所回傳的內容
                    # ----需要coords座標----
                    coords = tuple(np.multiply(np.array((  # 存進numpy的array
                        hand.landmark[mp_hands.HandLandmark.WRIST].x,  # hand:抓取hand results, landmark:抓取地標, WRIST: 通過手腕
                        hand.landmark[mp_hands.HandLandmark.WRIST].y)),  # 獲取x和y的座標
                        [800, 400]).astype(int))
                    # ----需要coords座標----
                    cv2.putText(image, text, coords, cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA)  # 印出手勢意義

                # ----手指角度-----
                # if get_label(num, hand, results):
                #     text, coord = get_label(num, hand, results)

            draw_fingertip_coordinate(image, results)
            # draw_finger_angles(image, results)  # 印出手指角度

        cv2.imshow("Hand Tracking", image)  # 開新視窗顯示圖片
        if (cv2.waitKey(10) & 0xFF == ord('q')):  # 按鍵盤Q跳出循環
            break

cap.release()  # 把攝像頭和彈出視窗一併關掉
cv2.destroyAllWindows()
