import cv2
import numpy as np
import copy
import math

###NOTE: getInfo() is the main function to use and IMPORT ALL THOSE FOUR
#Fingers doesn't count the thumb, as the thumb is required to be out for 
#it to detect one finger pointing

#binary image cutoff threshold
threshold = 160

top = cv2.VideoCapture(1)
#cap = cv2.VideoCapture(0)
#hand haar cascade from nikolas markou (imperial college london)
hand_cascade = cv2.CascadeClassifier("Hand.Cascade.1.xml")

#get size of the rectangle
def getSize(hand):
	w = hand[2]
	h = hand[3]
	return w*h
#CREDIT TO IZANE for his finger calc god level next gen bullcrap
def calculateFingers(res,drawing):  # -> finished bool, cnt: finger count
    #  convexity defect
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None):  # avoid crashing.   (BUG not found)

            cnt = 0
            pointerFinger = tuple(res[defects[0][0][0]][0])
            maxDist = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                if(b > maxDist):
                    pointerFinger = start
                    maxDist = b
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                #draw fingers
                cv2.line(drawing, start,far,[255,255,255], 2)
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            return True, cnt, pointerFinger
    return False, 0, (None,None)

#count the contours (probs just 1 lol) and show the res (outline) and hull(contour)
def addContour(output):
	img = output
	#grayscale for threshold
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#blur so that there's less edges for contours to false positive
	blur = cv2.GaussianBlur(gray, (31,31), 0)
	#binary it based on that threshold number (2nd input)
	###NOTE:get the cmu flag from rez
	ret, thresh = cv2.threshold(blur,threshold,255,cv2.THRESH_BINARY)
	image,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#it should have only one contour, and that is the hand
	#cv2.drawContours(thresh, contours, -1, (0,255,0), 3)
	#find the largest contour, which is the hand
	maxArea = -1
	ci = 0
	#make an empty black image in the shape of the frame
	drawing = np.zeros(img.shape, np.uint8)
	if len(contours) > 0:
		for i in range(len(contours)):
			temp = contours[i]
			area = cv2.contourArea(temp)
			if(area > maxArea):
				maxArea = area
				ci = i
		#outline of hand coordinates
		res = contours[ci]
		#contour of hand - the hull is just a list of contours' points
		hull = cv2.convexHull(res)
		#defects to find the junctions between fingers - note: hull must be > 3
		#draw those
		cv2.drawContours(drawing, [res], 0, (255, 255, 0), 2)
		cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
		cv2.putText(drawing, "Contours: " + str(len(contours)), (100,100), \
			cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
		#calculate num fingers
		isFinishCal, cnt, pointerFinger = calculateFingers(res, drawing)
		if isFinishCal is True:
			#NOTE: Fingers doesn't count the thumb
			cv2.putText(drawing, "Fingers: " + str(cnt), (100,200), \
			cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
		return cnt, drawing, pointerFinger
	return 0, drawing, (0,0)

#uses haar cascades to find the hand in blue rect
def findStuff(img):
	roi_color = img
	roi_size = 0
	#__, face = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#grayface = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
	#detect all hands
	handlist = hand_cascade.detectMultiScale(gray,1.4,3)
	#look for fingers?
	for (x,y,w,h) in handlist:
	    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	    #add fingers
	    '''fingers = finger_cascade.detectMultiScale(roi_gray, 1.4,6)
	    for (ex,ey,ew,eh) in fingers:
	        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)'''
	#find biggest hand found
	if(len(handlist) > 0):
		biggest = handlist[0]
		maxsize = getSize(handlist[0])
		for hand in range(len(handlist)):
			if(getSize(handlist[hand]) > maxsize):
				maxsize = getSize(handlist[hand])
				biggest = handlist[hand]
		roi_size = maxsize
		roi_color = biggest
	#return changed image, biggest size and biggest hand coords
	return img, roi_size, roi_color

#Get Info is supposed to return x,y, fingerCount
def getInfo():
	_, img = top.read()
	contour_img = copy.deepcopy(img)
	#get the outlined image, maxsize, maxhand coords
	output, size, hand = findStuff(img)
	handx,handy = hand[0] + hand[2]/10,hand[1]
	#if it doesn't find a hand
	x,y = handx,handy
	#prints size of biggest hand found to confirm that the roi_color is legit for contour processing
	#cv2.putText(img, str(size), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 2, cv2.LINE_AA)
	#find contours and add them
	fingerCount, hand_img, pointerFinger = addContour(contour_img)
	x,y = pointerFinger[0], pointerFinger[1]
	'''if(type(handx) != np.float64 or type(handy) != np.int32):
		x,y = None,None'''
	#draw coords on screen
	cv2.putText(img, "x: " + str(x), (50,50), \
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2, cv2.LINE_AA)
	cv2.putText(img, "y: " + str(y), (50,100), \
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2, cv2.LINE_AA)
	#outputs just the biggest hand found
	cv2.imshow('hands', hand_img)
	cv2.imshow('output', output)
	#return important stuff
	return pointerFinger,fingerCount


"""while(True):
	(x,y),fingers = getInfo()
	#print(x,y,fingers)
	if cv2.waitKey(20) == 27:
		break"""




