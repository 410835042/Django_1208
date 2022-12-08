import time
from .hand_video_detector import hand_video
import cv2
import mediapipe as mp
import numpy as np
import math


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# basically take camera input and convert it into a cv object
# later to be processed by gen()


def hand_video(flag, frame):
    hands = mp_hands.Hands( static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
    image = cv2.flip(frame, 1)  # flip it along y axis
    # image = frame
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # color format conversion
    # print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
        hands.close()
        return frame
    # image_hight, image_width, _ = image.shape
    # annotated_image = image.copy()
    # # draw result landmarks
    # for hand_landmarks in results.multi_hand_landmarks:
    #     mp_drawing.draw_landmarks(
    #         annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
    #         mp_drawing.DrawingSpec(color=(121, 87, 76), thickness=1, circle_radius=4),  # 關節點顏色 color:(藍，綠，紅)
    #         mp_drawing.DrawingSpec(color=(255, 255, 25), thickness=2, circle_radius=2),  # 關節顏色
    #     )
    if results.multi_hand_landmarks:
        for num, hand in enumerate(results.multi_hand_landmarks):  # multi_hand_landmarks中是x,y,z座標
            mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(121, 87, 76), thickness=1, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(255, 255, 25), thickness=2, circle_radius=2),
                                      )
            # Render left or right detection
            if results.multi_handedness:  # results.multi_handedness 有 index:0or1, score, label:"Left" or "Right"
                for index, classification in enumerate(results.multi_handedness):
                    label = str(classification.classification[0].label)
                    coords = tuple(np.multiply(np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x,
                                                         hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                                               [640, 480]).astype(int))
                    cv2.putText(image, label, coords, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    ratio = print_hand_length(results)

    f = open('static/Ratio.txt', 'w')
    if f.writable():
        f.write(str(ratio)+"\n")
    else:
        print("cannot write")
    # flip it back and return

    f.close()
    return cv2.flip(image, 1)


class V_Camera2(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()


    def get_frame(self):
        success, image = self.video.read()
        if success:
            # call the detection here
            image = hand_video(success, image)
            # hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
            # results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # color format conversion
            # if not results.multi_hand_landmarks:
            #     hands.close()
            #     return image
            #
            # for hand_landmarks in results.multi_hand_landmarks:
            #     mp_drawing.draw_landmarks(
            #         image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            #         mp_drawing.DrawingSpec(color=(121, 87, 76), thickness=1, circle_radius=4),  # 關節點顏色 color:(藍，綠，紅)
            #         mp_drawing.DrawingSpec(color=(255, 255, 25), thickness=2, circle_radius=2),  # 關節顏色
            #     )
            # print_hand_length(results)
        return cv2.flip(image, 1)


# generator that saves the video captured if flag is set
def to_gen2(camera, flag):
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
def print_hand_length(results):
    joint_list1 = [[1, 2], [5, 9], [5, 9], [9, 13], [13, 17]]  # 量指寬
    joint_list2 = [[4, 2], [8, 5], [12, 9], [16, 13], [20, 17]]  # 量指長
    joint_list3 = [[0, 9], [5, 17]]  # 量手掌寬度、高度
    fl = np.array([])
    palm = np.array([])
    fa = np.array([])
    for hand in results.multi_hand_landmarks:
        for joint in joint_list1:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
            # temp = [round(np.linalg.norm(a - b) * 34.5 - 2.0, 3)]

            temp = round(math.sqrt(pow((a[0]-b[0]) * 34.5, 2) + pow((a[1]-b[1]) * 34.5, 2)) - 2.0, 2)
            fa = np.append(fa, [temp])
        for joint in joint_list2:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
            fl_temp = [round(np.linalg.norm(a - b) * 34.5 - 2.0, 3)]
            fl = np.append(fl, [fl_temp])
        for joint in joint_list3:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
            palm_temp = [round(np.linalg.norm(a - b) * 34.5 - 2.0, 3)]
            palm = np.append(palm, [palm_temp])
        palm = np.append(palm, [99.9, 99.9, 99.9])
    fa = np.vstack([fa, fl])
    fa = np.vstack([fa, palm])
    # print("finger width:" + str(fa[0]) + "cm")
    # print("finger length:" + str(fa[1]) + "cm")
    # print("palm height:" + str(fa[2][0]) + "cm")
    # print("palm width:" + str(fa[2][1]) + "cm")
    return fa


def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            label = classification.classification[0].label
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))
            output = label, coords
    return output




