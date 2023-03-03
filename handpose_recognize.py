import numpy as np

def p_to_p_distance(p1,p2):
    return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))

def hand_point(result,h,w):
    handpoint_list = []
    hand_21 = result.multi_hand_landmarks[0]
    handpoint_list.append([int(hand_21.landmark[0].x * w), int(hand_21.landmark[0].y * h)])
    handpoint_list.append([int(hand_21.landmark[1].x * w), int(hand_21.landmark[1].y * h)])
    handpoint_list.append([int(hand_21.landmark[2].x * w), int(hand_21.landmark[2].y * h)])
    handpoint_list.append([int(hand_21.landmark[3].x * w), int(hand_21.landmark[3].y * h)])
    handpoint_list.append([int(hand_21.landmark[4].x * w), int(hand_21.landmark[4].y * h)])
    handpoint_list.append([int(hand_21.landmark[5].x * w), int(hand_21.landmark[5].y * h)])
    handpoint_list.append([int(hand_21.landmark[6].x * w), int(hand_21.landmark[6].y * h)])
    handpoint_list.append([int(hand_21.landmark[7].x * w), int(hand_21.landmark[7].y * h)])
    handpoint_list.append([int(hand_21.landmark[8].x * w), int(hand_21.landmark[8].y * h)])
    handpoint_list.append([int(hand_21.landmark[9].x * w), int(hand_21.landmark[9].y * h)])
    handpoint_list.append([int(hand_21.landmark[10].x * w), int(hand_21.landmark[10].y * h)])
    handpoint_list.append([int(hand_21.landmark[11].x * w), int(hand_21.landmark[11].y * h)])
    handpoint_list.append([int(hand_21.landmark[12].x * w), int(hand_21.landmark[12].y * h)])
    handpoint_list.append([int(hand_21.landmark[13].x * w), int(hand_21.landmark[13].y * h)])
    handpoint_list.append([int(hand_21.landmark[14].x * w), int(hand_21.landmark[14].y * h)])
    handpoint_list.append([int(hand_21.landmark[15].x * w), int(hand_21.landmark[15].y * h)])
    handpoint_list.append([int(hand_21.landmark[16].x * w), int(hand_21.landmark[16].y * h)])
    handpoint_list.append([int(hand_21.landmark[17].x * w), int(hand_21.landmark[17].y * h)])
    handpoint_list.append([int(hand_21.landmark[18].x * w), int(hand_21.landmark[18].y * h)])
    handpoint_list.append([int(hand_21.landmark[19].x * w), int(hand_21.landmark[19].y * h)])
    handpoint_list.append([int(hand_21.landmark[20].x * w), int(hand_21.landmark[20].y * h)])

    return handpoint_list

def judge_handpose(handpoint_list):

    if handpoint_list[8][1] < handpoint_list[7][1] < handpoint_list[6][1] and \
         handpoint_list[10][1] < handpoint_list[11][1] < handpoint_list[12][1]  and \
         handpoint_list[14][1] < handpoint_list[15][1] < handpoint_list[16][1]  and \
         handpoint_list[18][1] < handpoint_list[19][1] < handpoint_list[20][1]:

        return 'Index_up'

    elif handpoint_list[12][1] < handpoint_list[11][1] < handpoint_list[10][1] and \
        handpoint_list[8][1] < handpoint_list[7][1] < handpoint_list[6][1] and \
        handpoint_list[14][1] < handpoint_list[15][1] < handpoint_list[16][1] and \
        handpoint_list[18][1] < handpoint_list[19][1] < handpoint_list[20][1]:

        return 'Index_middle_up'

    elif abs(handpoint_list[8][1] - handpoint_list[7][1]) < 40 and \
         abs(handpoint_list[7][1] - handpoint_list[6][1]) < 40 :

        return 'Index_down'

    else:
        return None






