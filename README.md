# FreePaint
Computer Vision project for Hack112 @ CMU - 2nd place

This project utilizes OpenCV to read the contours of hand and uses convexity defects in order to read the junctions between fingers and get the longest finger, which acts as the drawing pointer. Use an external webcam and hang it above a black backdrop, and try using your hand to draw! There will be three windows if you initialize home.py, and one will be the app, one the contour map of your hand, and one of the webcam image with your hand being tracked.


TECHNIQUES:
If you want to draw, the camera will draw if it detects two fingers out- I'd recommend using your thumb and forefinger, and it'll automatically go to the longest finger present as the pointer. Your thumb is like the activation for 'draw mode'.

If you want to move to a different section without drawing, just move your index finger - if you just have one finger out, it won't draw, but it'll still follow your hand.

To clear screen: Open your hand - if there's all five fingers present, it'll clear the drawing.

Change color/width of line/erase: 
Use 2,3,4 respectively - the 'help' section will show the keyboard shortcuts too.
