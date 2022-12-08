import cv2
import mediapipe as mp
import numpy as np
import math


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def hand_video(flag, frame):
    # For static images:
    # parameters for the detector
    hands = mp_hands.Hands( static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
    # flip it along y axis
    # image = cv2.flip(frame, 1)
    image = frame
    # color format conversion
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
        hands.close()
        return frame
    image_hight, image_width, _ = image.shape
    annotated_image = image.copy()

    # draw result landmarks
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(121, 87, 76), thickness=1, circle_radius=4),  # 關節點顏色 color:(藍，綠，紅)
            mp_drawing.DrawingSpec(color=(255, 255, 25), thickness=2, circle_radius=2),  # 關節顏色
        )
        print_hand_length(results)
    # flip it back and return
    return cv2.flip(annotated_image, 1)


def print_hand_length(results):
    joint_list1 = [[5], [9]]  # 量指寬
    joint_list2 = [[4, 2], [8, 5], [12, 9], [16, 13], [20, 17]]  # 量指長
    joint_list3 = [[0, 9], [5, 17]]  # 量手掌寬度、高度
    subX = subY = subA = subB = subC = subD = 0.00
    fw = []
    fl = []
    palm = []
    for hand in results.multi_hand_landmarks:
        for joint in joint_list1:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            subX = abs(subX - round(a[0], 2))
            subY = abs(subY - round(a[1], 2))
        for joint in joint_list2:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
            fl_temp = [round((round(np.linalg.norm(a - b), 2) * 34.5 - 2.0), 3)]
            fl.extend(fl_temp)
        for joint in joint_list3:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
            palm_temp = [round((round(np.linalg.norm(a - b), 2) * 34.5 - 2.0), 3)]
            palm.extend(palm_temp)

    XY2 = round(math.sqrt(pow(subX, 2)+pow(subY, 2)), 2)
    AB2 = round(math.sqrt(pow(subA, 2)+pow(subB, 2)), 2)
    CD2 = round(math.sqrt(pow(subC, 2) + pow(subD, 2)), 2)
    print("finger width:" + str(round(XY2 * 34.5, 3)) + "cm")
    print("finger length:" + str(fl) + "cm")
    print("palm height:" + str(palm[0]) + "cm")
    print("palm width:" + str(palm[1]) + "cm")
