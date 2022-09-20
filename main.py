import cv2 as cv
import numpy as np

START_POINT = (0, 0)
END_POINT = (150, 150)

vid_width = 0
vid_height = 0

RECTANGLE_COLOR = (255, 0, 0)
FONT_COLOR = (124, 252, 0)
FONT_SCALE = 1
THICKNESS = 1
LINE_TYPE = 2
TEXT_LEFT_BOTTOM_CORNER = (0, 0)

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
    # cv.rectangle(img, START_POINT, END_POINT, (255, 0, 0), LINE_TYPE, THICKNESS*8)

    color_name = "Not found"
    max_mask_size = 0

    # Сравниваем размер маски для каждого цвета
    for cur_name, (lower, upper) in COLOR_SCHEME.items():
        mask = cv.inRange(hsv, lower, upper)

        mask_size = cv.countNonZero(mask)
        if mask_size > max_mask_size:
            max_mask_size = mask_size
            color_name = cur_name

    # Область в которой мы определяем цвет
    cv.rectangle(img, START_POINT, END_POINT, RECTANGLE_COLOR, LINE_TYPE, THICKNESS*8)

    # Отображение названия цвета
    cv.rectangle(img, (vid_width-160, vid_height-50), (vid_width, vid_height), (0, 0, 0), -1)
    cv.putText(img, color_name,
               TEXT_LEFT_BOTTOM_CORNER,
               cv.FONT_HERSHEY_SIMPLEX,
               FONT_SCALE,
               FONT_COLOR,
               THICKNESS,
               LINE_TYPE)

    return img

capture = cv.VideoCapture("C:/Users/whr1t/Desktop/Repos/CV/videoplayback.mp4")
# capture = cv.VideoCapture(0)

vid_width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
vid_height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))

TEXT_LEFT_BOTTOM_CORNER = (vid_width - 160, vid_height - 10)

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
