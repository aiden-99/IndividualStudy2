import cv2
import numpy as np

PI = 3.14159265

def FindDistance(x1, y1, x2, y2):
    distance = np.sqrt(np.power(x2 - x1, 2) + pow(y2 - y1, 2))
    return distance


def radianToAngle(radian):
    return radian * 180 / PI


def main():
    img = cv2.imread("1.jpg")
    qrCodeDetector = cv2.QRCodeDetector()
    points = []
    decodedText, points, _ = qrCodeDetector.detectAndDecode(img)

    eachlineDistance = []
    eachlineDistance.append(FindDistance(int(points[0][0][0]), int(points[0][0][1]), int(points[0][1][0]), int(points[0][1][1])))
    eachlineDistance.append(FindDistance(int(points[0][1][0]), int(points[0][1][1]), int(points[0][2][0]), int(points[0][2][1])))
    eachlineDistance.append(FindDistance(int(points[0][2][0]), int(points[0][2][1]), int(points[0][3][0]), int(points[0][3][1])))
    eachlineDistance.append(FindDistance(int(points[0][3][0]), int(points[0][3][1]), int(points[0][0][0]), int(points[0][0][1])))

    distance = []
    #qrcode의 각 변의 픽셀 수를 이용해서 카메라로부터 각 변까지의 거리 측정
    for i in range(4):
        distance.append(464.25 * 51 /eachlineDistance[i])
    dif_width = 0
    dif_height = 0
    if distance[0] < distance[2]:
        dif_width = distance[2] - distance[0]
    else:
        dif_width = distance[0] - distance[2]

    if distance[1] < distance[3]:
        dif_height = distance[3] - distance[1]
    else:
        dif_height = distance[1] - distance[3]

    final_distance = 0
    final_angle = 0
    #QRcode과 상하좌우 어느쪽으로도 회전하지 않은 경우
    if dif_width < 4 and dif_height < 4:
        final_distance = (distance[0] + distance[2]) / 2

    #QRcode가 상하로 회전한 경우
    elif dif_width > 4 and dif_height < 4:
        final_distance = (distance[0] + distance[2]) / 2
        radian = np.arccos(dif_width / 20)
        final_angle = radianToAngle(radian)

    #QRcode가 좌우로 회전한 경우
    elif dif_width < 4 and dif_height > 4:
        final_distance = (distance[1] + distance[3]) / 2
        radian = np.arcsin(dif_height / 20)
        final_angle = radianToAngle(radian)

    else:
        print("QRcode를 찾지 못함")

    print('최종 거리', str(final_distance))
    print('최종 각도', str(final_angle))

if __name__ == "__main__":
    main()