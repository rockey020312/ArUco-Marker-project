from djitellopy import Tello
import cv2

width = 640  # WIDTH OF THE IMAGE
height = 480  # HEIGHT OF THE IMAGE

drone = Tello()
drone.connect()
drone.streamoff()
drone.streamon()


capture = cv2.VideoCapture(1)
capture.set(3, width)
capture.set(4, height)


while True:

    frame_read = drone.get_frame_read()
    droneFrame = frame_read.frame
    image_code = cv2.resize(droneFrame, (width, height))

    list_marker = []
    list_marker_and_code = []
    ret, image_input = capture.read()
    if ret:
        corners, ids, _ = cv2.aruco.detectMarkers(cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY), cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250))
        cv2.aruco.drawDetectedMarkers(image_code, corners, ids)
        cv2.imshow("frame", image_code)
        if cv2.waitKey(int(1000 / capture.get(cv2.CAP_PROP_FPS))) > 0:
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()
