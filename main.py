import cv2 as cv
import numpy as np

START_POINT = (0, 0)
END_POINT = (150, 150)

COMMAND_KEYS = {
    2490368: (0, -10),  # UpKey
    2621440: (0, 10),  # DownKey
    2424832: (-10, 0),  # LeftKey
    2555904: (10, 0)  # RightKey
}

COLOR_SCHEME = {
    "Red": (np.array([0, 70, 50]), np.array([10, 255, 255])),
    "Green": (np.array([40, 40, 40]), np.array([70, 255, 255])),
    "Blue": (np.array([100, 150, 0]), np.array([140, 255, 255])),
    "Yellow": (np.array([25, 50, 50]), np.array([32, 255, 255]))
}


def process(img):
    image = img[START_POINT[1]:END_POINT[1], START_POINT[0]:END_POINT[0]].copy()
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    cv.rectangle(img, START_POINT, END_POINT, (255, 0, 0), 2, 8)

    dom_color = None
    max = 0

    for name, (lower, upper) in COLOR_SCHEME.items():
        mask = cv.inRange(hsv, lower, upper)
        # output = cv.bitwise_and(image, image, mask=mask)
        # cv.imshow("images", np.hstack([image, output]))

        mask_size = cv.countNonZero(mask)
        if mask_size > max:
            max = mask_size
            dom_color = name

    print(dom_color)

    return img

capture = cv.VideoCapture("C:/Users/whr1t/Desktop/Repos/CV/videoplayback.mp4")
# capture = cv.VideoCapture(0)

while True:
    ret, frame = capture.read()
    if ret is True:
        result = process(frame)
        cv.imshow("result", result)

        k = cv.waitKeyEx(100)
        frame_move = COMMAND_KEYS.get(k)
        if frame_move:
            START_POINT = tuple(map(lambda x, y: x + y, START_POINT, frame_move))
            END_POINT = tuple(map(lambda x, y: x + y, END_POINT, frame_move))

        if k == 27:  # ESC
            break
    else:
        break

cv.waitKey(0)
capture.release()
cv.destroyAllWindows()
