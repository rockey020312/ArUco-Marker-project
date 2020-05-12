import cv2

capture = cv2.VideoCapture(0)

while capture.isOpened():
    list_marker = []
    list_marker_and_code = []
    ret, image_input = capture.read()
    if ret:
        image_code = image_input.copy()
        corners, ids, _ = cv2.aruco.detectMarkers(cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY), cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250))
        cv2.aruco.drawDetectedMarkers(image_code, corners, ids)
        cv2.imshow("frame", image_code)
        if cv2.waitKey(int(1000 / capture.get(cv2.CAP_PROP_FPS))) > 0:
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()