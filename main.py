from collections import deque
from webcamvideostream import WebcamVideoStream
import os
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

lpts = deque(maxlen=8)#args["buffer"]) #buffer to hold left stick coordinates
rpts = deque(maxlen=8)#args["buffer"]) #buffer to hold right stick coordinates

xQue = deque(maxlen=2) #length 2 buffer to hold current x-axis positions of l and r sticks
center = deque(maxlen=2) #length 2 buffer to hold center positions of l and r sticks

(lisDown, risDown) = (False, False)

objLower = (30, 86, 14)
objUpper = (97, 244, 255)

wave_clap  = sa.WaveObject.from_wave_file("audio/Clap.wav")
wave_clap2 = sa.WaveObject.from_wave_file("audio/Clap2.wav")
wave_clap3 = sa.WaveObject.from_wave_file("audio/Clap3.wav")
wave_kick  = sa.WaveObject.from_wave_file("audio/Kick.wav")
wave_kick2 = sa.WaveObject.from_wave_file("audio/Kick2.wav")
wave_kick3 = sa.WaveObject.from_wave_file("audio/Kick3.wav")
wave_hat   = sa.WaveObject.from_wave_file("audio/Hat.wav")
wave_hat2  = sa.WaveObject.from_wave_file("audio/Hat2.wav")
wave_hat3  = sa.WaveObject.from_wave_file("audio/Hat3.wav")

play_clap  = wave_clap.play()
play_clap2 = wave_clap2.play()
play_clap3 = wave_clap3.play()
play_kick  = wave_kick.play()
play_kick2 = wave_kick2.play()
play_kick3 = wave_kick3.play()
play_hat   = wave_hat.play()
play_hat2  = wave_hat2.play()
play_hat3  = wave_hat3.play()

frameCount = 0
(ldY, rdirY) = (0, 0)

vs = WebcamVideoStream(src=0).start()
time.sleep(1.0)

while True:
    frame = vs.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, objLower, objUpper)
    mask = cv2.erode(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # sort cnts so we can loop through the two biggest (the sticks hopefully)
    cnts = sorted(cnts,key=lambda x: cv2.contourArea(x), reverse = True)
    for i in range(min(len(cnts), 2)):
        ((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
        xQue.appendleft(x)
        center.appendleft((int(x),int(y)))
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

        #process left stick
        if (left):
            lpts.appendleft(center[i])
            if frameCount >= 4 and lpts[4] is not None:
                # compute the difference in direction between current frame
                # and from 4-frames-ago
                ldY = lpts[4][1] - lpts[1][1]
                
                #Threshold of 10 pixels for downward direction
                if(lisDown and ldY < -20):
                    # Play sound according to x position
                    # Play different volume sample based on distance moved
                    if (xQue[i] <=200):
                        play_kick = wave_kick.play()
                    elif (xQue[i] <=400):
                        print(ldY)
                        if (ldY < -70):
                            play_clap = wave_clap.play()
                        elif (ldY < -60):
                            play_clap2 = wave_clap.play()
                        else:
                            play_clap3 = wave_clap3.play()
                    else:
                        play_hat = wave_hat.play()
                    lisDown = False

                if np.abs(ldY) > 30 and ldY >=0:
                    lisDown = True
            
        #process right stick
        else:
            rpts.appendleft(center[i])
            if frameCount >= 4 and rpts[4] is not None:
                # compute the difference in direction between current frame
                # and from 4-frames-ago
                rdY = rpts[4][1] - rpts[1][1]

                #Threshold of 10 pixels for downward direction 
                if(risDown and rdY < -20):
                    #Play sound according to x position
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
            
    # show the frame to our screen and increment the frame count
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    frameCount += 1
    
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
vs.stop()
cv2.destroyAllWindows()
