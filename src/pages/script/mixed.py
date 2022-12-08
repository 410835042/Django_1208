import time
from .hand_video_detector import hand_video
import cv2
import mediapipe as mp
import pyautogui as pag
import numpy as np
import math


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# basically take camera input and convert it into a cv object
# later to be processed by gen()


def hand_video(flag, frame):
    # For static images:
    # parameters for the detector
    hands = mp_hands.Hands( static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
    # image = cv2.flip(frame, 1)  # flip it along y axis
    image = frame
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # color format conversion
    # print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
        hands.close()
        return frame
    image_hight, image_width, _ = image.shape
    annotated_image = image.copy()
    w, h = 800, 600
    # draw result landmarks
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(121, 87, 76), thickness=1, circle_radius=4),  # 關節點顏色 color:(藍，綠，紅)
            mp_drawing.DrawingSpec(color=(255, 255, 25), thickness=2, circle_radius=2),  # 關節顏色
        )
        # ----手指角度-----
        finger_points = []  # 記錄手指節點座標的串列
        for i in hand_landmarks.landmark:
            # 將 21 個節點換算成座標，記錄到 finger_points
            x = i.x * w
            y = i.y * h
            finger_points.append((x, y))
    # print_hand_length(results)
    if finger_points:
        finger_angle = hand_angle(finger_points)  # 計算手指角度，回傳長度為 5 的串列
        hand_pos(finger_angle, convert_coord(results))  # 取得手勢所回傳的內容
    # flip it back and return
    return cv2.flip(annotated_image, 1)


class V_Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if success:
            # call the detection here
            image = hand_video(success, image)

        return image


# generator that saves the video captured if flag is set
def to_gen(camera, flag):
    if flag == True:
        # time information
        time_now = time.localtime()
        current_time = time.strftime("%H:%M:%S", time_now)
        # default format
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # output which is a cv writer, given the name and format, and resolution
        out = cv2.VideoWriter('output_' + str(current_time) + '.avi', fourcc, 20.0, (640, 480))

        while True:
            ret, jpeg = cv2.imencode('.jpg', camera.get_frame())  # cv object to jpg
            frame = jpeg.tobytes()  # jpg to bytes
            # generator yielding the bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            cv_frame = camera.get_frame()
            out.write(cv_frame)

    else:
        while True:
            ret, jpeg = cv2.imencode('.jpg', camera.get_frame())
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# 抓到手的長度比例
# def print_hand_length(results):
#     joint_list1 = [[1, 2], [5, 9], [5, 9], [9, 13], [13, 17]]  # 量指寬
#     joint_list2 = [[4, 2], [8, 5], [12, 9], [16, 13], [20, 17]]  # 量指長
#     joint_list3 = [[0, 9], [5, 17]]  # 量手掌寬度、高度
#     fl = np.array([])
#     palm = np.array([])
#     fa = np.array([])
#     for hand in results.multi_hand_landmarks:
#         for joint in joint_list1:
#             a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
#             b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
#             # temp = [round(np.linalg.norm(a - b) * 34.5 - 2.0, 3)]
#
#             temp = round(math.sqrt(pow((a[0]-b[0]) * 34.5, 2) + pow((a[1]-b[1]) * 34.5, 2)) - 2.0, 2)
#             fa = np.append(fa, [temp])
#         for joint in joint_list2:
#             a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
#             b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
#             fl_temp = [round(np.linalg.norm(a - b) * 34.5 - 2.0, 3)]
#             fl = np.append(fl, [fl_temp])
#         for joint in joint_list3:
#             a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
#             b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
#             palm_temp = [round(np.linalg.norm(a - b) * 34.5 - 2.0, 3)]
#             palm = np.append(palm, [palm_temp])
#         palm = np.append(palm, [99.9, 99.9, 99.9])
#     fa = np.vstack([fa, fl])
#     fa = np.vstack([fa, palm])
#     return fa


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


def hand_pos(finger_angle, a):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度
    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        pag.moveTo(2559-a[0], a[1])  # 滑鼠移動
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
