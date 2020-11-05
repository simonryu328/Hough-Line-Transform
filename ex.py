# Line detection from video
import cv2 as cv
import numpy as np

cap = cv.VideoCapture('Resources/raw_video_feed.mp4')

while cap.isOpened():
    ret, frame = cap.read()  # grabs, decodes, and returns next frame (ret is true or false)

    if not ret:  # if frame is read correctly ret is True
        print("No more frame. Exiting ...")
        break
        # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # Converts an image from one color space to another

    ret, thresh = cv.threshold(frame, 100, 255, cv.THRESH_BINARY)
    startPixel = -1
    endPixel = -1

    for i in range(320):
        val = thresh[225, i, 0]  # val is 0 when it sees black, 255 when it sees white

        if val == 0:  # if you see black
            if startPixel == -1:
                startPixel = i

        else:  # if you see white
            if endPixel == -1 and startPixel != -1:
                endPixel = i
                break

    middle = (endPixel - startPixel) // 2
    cv.circle(thresh, (startPixel + middle, 217), 20, (255, 205, 195), -1)  # y,x coordinate
    cv.imshow('frame', thresh)  # 'frame' is just a string to specify its a frame, thresh is the b&w frame i have

    if cv.waitKey(50) == ord('q'):  # that number is the delay time in milliseconds
        break  # if you type q it breaks

cap.release()
cv.destroyAllWindows()