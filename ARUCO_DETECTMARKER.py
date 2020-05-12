import cv2
import numpy as np


def check_edge(check_marker):
    edge_white = 0
    for i in range(marker_cell):
        cell = check_marker[i * cell_size:(i + 1) * cell_size, 0:cell_size]
        if cv2.countNonZero(cell) > cell_size * cell_size:
            edge_white += 1

        cell = check_marker[i * cell_size:(i + 1) * cell_size, marker_size - cell_size:marker_size]
        if cv2.countNonZero(cell) > cell_size * cell_size:
            edge_white += 1

        cell = check_marker[0:cell_size, i * cell_size:(i + 1) * cell_size]
        if cv2.countNonZero(cell) > cell_size * cell_size:
            edge_white += 1

        cell = check_marker[marker_size - cell_size:marker_size, i * cell_size:(i + 1) * cell_size]
        if cv2.countNonZero(cell) > cell_size * cell_size/2:
            edge_white += 1

    return edge_white



input_name = 'image2.jpg'
list_marker = []
marker_size = 200
marker_cell = 8
cell_size = int(marker_size/marker_cell)
image_input = cv2.imread(input_name, cv2.IMREAD_COLOR)
height, width = image_input.shape[:2]
# threshold 는 input image 로 grayscale 이미지만을 받는다. 따라서 변환 필요.
image_gray = cv2.cvtColor(image_input, cv2.COLOR_RGB2GRAY)
image_blur = cv2.GaussianBlur(image_gray, (9, 9), 0)

# ret, image_binary = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)
# image_binary = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# image_binary = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
ret, image_binary = cv2.threshold(image_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

image_contour = image_input.copy()
array_contour, hierarchy = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
for cnt in array_contour:
    cv2.drawContours(image_contour, [cnt], 0, (255, 0, 0), 3)

for cnt in array_contour:
    epsilon = cv2.arcLength(cnt, True) * 0.07
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    area_min = 2000
    area_max = 50000
    if np.size(approx, 0) == 4 and cv2.isContourConvex(approx) and area_min <= cv2.contourArea(approx) <= area_max:
        point_list = []
        for point in approx.tolist():
            point_list.append(point[0])
        points_1 = np.float32(point_list)
        points_2 = np.float32([[0, 0], [marker_size, 0], [marker_size, marker_size], [0, marker_size]])
        M = cv2.getPerspectiveTransform(points_1, points_2)
        image_marker_tmp = cv2.warpPerspective(image_binary, M, (marker_size, marker_size))
        if check_edge(image_marker_tmp) == 0:
            cv2.drawContours(image_contour, [approx], 0, (0, 0, 255), 3)
            list_marker.append([image_marker_tmp, points_1])

for i in range(len(list_marker)):
    marker = list_marker[i][0]
    name = 'mk' + str(i+1)
    cv2.imshow(name, marker)

image_output = image_contour
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 960, 540)
cv2.imshow('frame', image_output)
cv2.waitKey()