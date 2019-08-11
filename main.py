from collections import deque
from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import simpleaudio as sa

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=8,
    help="max buffer size")
args = vars(ap.parse_args())

lpts = deque(maxlen=args["buffer"])
rpts = deque(maxlen=args["buffer"])

xQue = deque(maxlen=2)
center = deque(maxlen=2)

(lisDown, risDown) = (False, False)

objLower = (30, 86, 14)
objUpper = (97, 244, 255)

wave_clap = sa.WaveObject.from_wave_file("audio/Clap.wav")
wave_kick = sa.WaveObject.from_wave_file("audio/Kick.wav")
wave_hat = sa.WaveObject.from_wave_file("audio/Hat.wav")
play_clap = wave_clap.play()
play_kick = wave_kick.play()
play_hat = wave_hat.play()

counter = 0
(ldY, rdirY) = (0, 0)

vs = WebcamVideoStream(src=0).start()
time.sleep(1.0)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=600)
    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, objLower, objUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # sort cnts so we can loop through the two biggest (the sticks hopefully)
    cnts = sorted(cnts,key=lambda x: cv2.contourArea(x), reverse = True)
    for i in range(min(len(cnts), 2)):
        ((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
        xQue.appendleft(x)
        M = cv2.moments(cnts[i])
        center.appendleft((int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])))
    for i in range(min(len(cnts), 2)):
        if (len(cnts) > 1):
            if (xQue[i] <= xQue[(i+1)%2]):
                left = True
            else:
                left = False
        else:
            if(xQue[i] <= 300):
                left = True
            else: 
                left = False
        if (left):
            lpts.appendleft(center[i])
            for j in np.arange(1, 8):
                if counter >= 8 and j == 1 and lpts[-8] is not None:
                    # compute the difference between the x and y
                    # coordinates and re-initialize the direction
                    ldY = lpts[-8][1] - lpts[j][1]
                    if(lisDown and ldY < 0):
                        if (xQue[i] <=200):
                            play_kick = wave_kick.play()
                        elif (xQue[i] <=400):
                            play_clap = wave_clap.play()
                        else:
                            play_hat = wave_hat.play()
                        lisDown = False

                    if np.abs(ldY) > 30 and ldY >=0:
                        #if(ldY >= 0):
                        lisDown = True
                
            cv2.circle(frame, center[i], 5, (0, 0, 255), -1)
        else:
            rpts.appendleft(center[i])
            for j in np.arange(1, 8):
                if counter >= 8 and j == 1 and rpts[-8] is not None:
                    # compute the difference between the x and y
                    # coordinates and re-initialize the direction
                    rdY = rpts[-8][1] - rpts[j][1]
                    if(risDown and rdY < 0):
                        if (xQue[i] <=200):
                            play_kick = wave_kick.play()
                        elif (xQue[i] <=400):
                            play_clap = wave_clap.play()
                        else:
                            play_hat = wave_hat.play()
                        risDown = False

                    if np.abs(rdY) > 30 and rdY >=0:
                        #if(rdY >= 0):
                        risDown = True
                
            cv2.circle(frame, center[i], 5, (255, 0, 0), -1)

    # show the frame to our screen and increment the frame counter
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
vs.stop()
cv2.destroyAllWindows()
