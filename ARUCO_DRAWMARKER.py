import cv2 as cv
import numpy as np

dic = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)  # 이미 정의된 마커 딕셔너리를 불러온다.

for i in range(5):
    markerImage = np.zeros((200, 200), dtype=np.uint8)  # 200*200 행렬의 모든 원소를 0으로 정한다.
    markerImage = cv.aruco.drawMarker(dic, i, 200, markerImage, 1)  # opencv 내장 aruco 함수로 그 인덱스의 마커를 그린다.
    img_name = "marker" + str(i) + ".png"
    cv.imwrite(img_name, markerImage)  # 생성된 마커를 이미지로 저장한다. 예: "marker12.png"

