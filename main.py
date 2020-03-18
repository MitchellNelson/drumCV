from collections import deque
from webcamvideostream import WebcamVideoStream
from DrumSound import DrumSound
from Stick import Stick
import os
import numpy as np
import argparse
import cv2
import imutils
import time
import simpleaudio as sa

drumSound = DrumSound("audio", "Clap", 5, ".wav")

def trackStick(stick):
    stick.setMin(min(stick.getMin(), stick.getY()))
    yDirection = stick.getPoints()[3][1] - stick.getPoints()[0][1]
    if (stick.getIsGoingDown() and yDirection < -20):
        volume = 500 - stick.getMin()
        drumSound.play(int(volume / 100))
        stick.setMin(400)
        stick.updateIsGoingDown(False)
    if np.abs(yDirection) > 30 and yDirection >= 0:
        stick.updateIsGoingDown(True)
    return

def main():
    center = deque(maxlen = 2)
    leftStick = Stick("left")
    rightStick = Stick("right")
    # Upper and lower bounds (HSV) for the stick color
    objLower = (30, 86, 14)
    objUpper = (97, 244, 255)
    #drumSound = DrumSound("audio", "Clap", 3, ".wav")
    #drumSound.play(2)
    frameCount = 0
    vs = WebcamVideoStream(src=0).start()
    time.sleep(1.0)
    while True:
        # Read in 1 frame at a time and flip the image
        frame = vs.read()
        frame = cv2.flip(frame, 1)

        # Mask the image so the result is just the drum stick tips
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, objLower, objUpper)
        mask = cv2.erode(mask, None, iterations=1)

        # find contours in the mask and initialize the current
        # (x, y) center of the stick tips
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # sort cnts so we can loop through the two biggest (the sticks hopefully)
        cnts = sorted(cnts,key=lambda x: cv2.contourArea(x), reverse = True)
        
        numSticks = min(len(cnts), 2)
        for i in range(numSticks):
            ((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
            if (radius > 5):
                center.appendleft((int(x),int(y)))
        for i in range(numSticks):
            if (numSticks > 1):
                if (center[i][0] <= center[(i + 1) % 2][0]):
                    cv2.circle(frame, center[i], 10,(0, 255, 255), 2) 
                    leftStick.addPoint(center[i][0], center[i][1])
                    if (frameCount > 4):
                        trackStick(leftStick)
                else:
                    cv2.circle(frame, center[i], 10,(255, 0, 0), 2) 
                    rightStick.addPoint(center[i][0], center[i][1])
                    if (frameCount > 4):
                        trackStick(rightStick)
            # Only one stick - split screen in half
            else:
                if(center[i][0]<= 300):
                    leftStick.addPoint(center[i][0], center[i][1])
                    if (frameCount > 4):
                        trackStick(leftStick)
                else: 
                    rightStick.addPoint(center[i][0], center[i][1])
                    if (frameCount > 4):
                        trackStick(rightStick)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        frameCount += 1
    
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
    vs.stop()
    cv2.destroyAllWindows()

if __name__== "__main__":
    main()

"""
lpts = deque(maxlen=2)#args["buffer"]) #buffer to hold left stick coordinates
rpts = deque(maxlen=2)#args["buffer"]) #buffer to hold right stick coordinates
xQue = deque(maxlen=2) #length 2 buffer to hold current x-axis positions of l and r sticks
yQue = deque(maxlen=2)
center = deque(maxlen=2) #length 2 buffer to hold center positions of l and r sticks
l_min = 500
r_min = 500
(lisDown, risDown) = (False, False)

# Upper and lower bounds (HSV) for the stick color
objLower = (30, 86, 14)
objUpper = (97, 244, 255)

drumSound = DrumSound("audio", "Clap", 3, ".wav")
drumSound.play(2)


frameCount = 0
(ldY, rdirY) = (0, 0)

vs = WebcamVideoStream(src=0).start()
time.sleep(1.0)
leftStick = Stick()
rightStick = Stick()
while True:

    # Read in 1 frame at a time and flip the image
    frame = vs.read()
    frame = cv2.flip(frame, 1)

    # Mask the image so the result is just the drum stick tips
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, objLower, objUpper)
    mask = cv2.erode(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the stick tips
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # sort cnts so we can loop through the two biggest (the sticks hopefully)
    
    cnts = sorted(cnts,key=lambda x: cv2.contourArea(x), reverse = True)
   
    #for i in range(min(len(cnts), 2)):
     #   ((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
      #  if (radius>5):
            


    for i in range(min(len(cnts), 2)):
        ((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
        if (radius>5):
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
            if frameCount >= 4 and lpts[1] is not None:
                l_min = min(l_min, lpts[0][1])     
                # compute the difference in direction between current frame and from 4-frames-ago
                ldY = lpts[1][1] - lpts[0][1]
                
                #Threshold of 20 pixels for downward direction
                if(lisDown and ldY < -25):
                    l_volume = 500 - l_min
                    
                    # Play sound according to x position
                    # Play different volume sample based on distance moved
                    if (xQue[i] <=180):
                        drumSound.play(1)
                        
                        #if (l_volume < 180):
                            #play_kick3 = wave_kick3.play()
                        #elif (l_volume < 300):
                            #play_kick2 = wave_kick2.play()
                        #else:
                            #play_kick = wave_kick.play()
                    elif (xQue[i] <=400):
                        drumSound.play(2)
                        #if (l_volume < 180):
                            #play_clap3 = wave_clap3.play()
                        #elif (l_volume < 300):
                            #play_clap2 = wave_clap2.play()
                        #else:
                            #play_clap = wave_clap.play()
                    else:
                        drumSound.play(3)
                        #if (l_volume < 180):
                            #play_hat3 = wave_hat3.play()
                        #elif (l_volume < 300):
                            #play_hat2 = wave_hat2.play()
                        #else:
                            #play_hat = wave_hat.play()

                    lisDown = False
                    l_min = 400
                if np.abs(ldY) > 30 and ldY >=0:
                    lisDown = True
        #process right stick
        else:
            rpts.appendleft(center[i])
            if frameCount >= 4 and rpts[1] is not None:
                # compute the difference in direction between current frame and from 4-frames-ago
                r_min = min(r_min, rpts[0][1])
                
                rdY = rpts[0][1] - rpts[1][1]

                #Threshold of 20 pixels for downward direction 
                if(risDown and rdY < -25):
                    r_volume = 500 - r_min

                    #Play sound according to x position
                    
                    if (xQue[i] <=150):
                        drumSound.play(3)
                        #if (r_volume < 180):
                            #play_kick3 = wave_kick3.play()
                        #elif (r_volume < 300):
                            #play_kick2 = wave_kick2.play()
                        #else:
                            #play_kick = wave_kick.play()
                    elif (xQue[i] <=400):
                        drumSound.play(2)
                        #if (r_volume < 180):
                            #play_clap3 = wave_clap3.play()
                        #elif (r_volume < 300):
                            #play_clap2 = wave_clap2.play()
                        #else:
                            #play_clap = wave_clap.play()
                    else:
                        drumSound.play(1)
                        #if (r_volume < 180):
                            #play_hat3 = wave_hat3.play()
                        #elif (r_volume < 300):
                            #play_hat2 = wave_hat2.play()
                        #else:
                            #play_hat = wave_hat.play()
                    
                    risDown = False
                    r_min = 400
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
"""



