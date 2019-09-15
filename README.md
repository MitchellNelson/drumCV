## drumCV
Computer vision drum simulator that produces drum sounds while a user is "air drumming" with two colored drum sticks in front of a webcam.

## Motivation
This project has been a way for me to learn and get experience with computer vision. I am a drummer, so I naturally try and connect my two passions - technology and music. 

### Demo Video:
[![Watch the Video](https://img.youtube.com/vi/Ml6xNJcYsfQ/0.jpg)](https://www.youtube.com/embed/Ml6xNJcYsfQ)

## Tech/framework used
<b>Built with</b>
- [OpenCV](https://opencv.org)
- [NumPy](https://numpy.org)
- [Simpleaudio](https://pypi.org/project/simpleaudio/)
- [imutils](https://www.pyimagesearch.com/2015/02/02/just-open-sourced-personal-imutils-package-series-opencv-convenience-functions/)

## Features
* Allows users to ”air drum” in front of a webcam while hearing realistic drum sounds for each ”hit”
* The X-Axis is split into three different sections, each representing a different sound - kick drum, snare drum, and hihat
* Tracks two colored drum sticks and calculates ”hits” based off changes in downward movement

## Credits
[PyImageSearch](https://www.pyimagesearch.com) has excellent tutorials on masking colors and tracking objects that were greatly useful for this project. I followed the tutorial on tracking a solid colored ball and expanded it to work for a drumming application.

### Future Development:
* C++ implementation should help reduce latency
