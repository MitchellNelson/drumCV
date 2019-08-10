from collections import deque
from imutils.video import VideoStream
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


(ldirY, rdirY) = ("", "")

objLower = (30, 86, 14)
objUpper = (97, 244, 255)

wave_clap = sa.WaveObject.from_wave_file("audio/Clap.wav")
play_clap = wave_clap.play()
wave_kick = sa.WaveObject.from_wave_file("audio/Kick.wav")
play_kick = wave_kick.play()


lpts = deque(maxlen=args["buffer"])
rpts = deque(maxlen=args["buffer"])

counter = 0
(ldY, rdirY) = (0, 0)

vs = VideoStream(src=0).start()

time.sleep(1.0)

while True:
    frame = vs.read()
    frame = cv2.flip(frame, 1)

    frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, objLower, objUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # sort cnts so we can loop through the two biggest (the sticks hopefully)
    cnts = sorted(cnts,key=lambda x: cv2.contourArea(x), reverse = True)
    for i in range(min(len(cnts), 2)):
        ((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
        M = cv2.moments(cnts[i])
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 8:
            if (x <= 300):
                left = True
            else:
                left = False
            if (left):
                lpts.appendleft(center)
                for j in np.arange(1, len(lpts)):
                    # if either of the tracked points are None, ignore
                    # them
                    if lpts[j - 1] is None or lpts[j] is None:
                        continue

                    # check to see if enough points have been accumulated in
                    # the buffer
                    if counter >= 8 and j == 1 and lpts[-8] is not None:
                        # compute the difference between the x and y
                        # coordinates and re-initialize the direction
                        # text variables
                        ldY = lpts[-8][1] - lpts[j][1]
                        if np.abs(ldY) > 30:
                            if(ldY >= 0):
                             ldirY = "down"
                    
                        if(ldirY == "down" and ldY < 0):
                            play_kick = wave_kick.play()
                            ldirY = "up"

                cv2.circle(frame, center, 5, (0, 0, 255), -1)
            else:
                rpts.appendleft(center)
                for j in np.arange(1, len(rpts)):
                    # if either of the tracked points are None, ignore
                    # them
                    if rpts[j - 1] is None or rpts[j] is None:
                        continue

                    # check to see if enough points have been accumulated in
                    # the buffer
                    if counter >= 8 and j == 1 and rpts[-8] is not None:
                        # compute the difference between the x and y
                        # coordinates and re-initialize the direction
                        # text variables
                        rdY = rpts[-8][1] - rpts[j][1]
                        if np.abs(rdY) > 30:
                            if(rdY >= 0):
                             rdirY = "down"
                    
                        if(rdirY == "down" and rdY < 0):
                            play_clap = wave_clap.play()
                            rdirY = "up"

                cv2.circle(frame, center, 5, (255, 0, 0), -1)
    
    # show the frame to our screen and increment the frame counter
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
vs.stop()

# close all windows
cv2.destroyAllWindows()
