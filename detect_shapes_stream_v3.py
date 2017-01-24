# import the necessary packages
from shapeDetection.shapedetector2 import ShapeDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import cv2
import time
import numpy as np
import pickle

# initialize the camera and grap a reference to the raw camera capture
camera = PiCamera() 
camera.resolution = (640, 480)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(640,480))

# allow the camera to warmup
time.sleep(0.1)

# define range of blue and red color in HSV
blueLower = np.array([75,50,50])
blueUpper = np.array([130,255,255]) 

redLower1 = np.array([0,50,50])
redUpper1 = np.array([10,255,255])
redLower2 = np.array([160,50,50])
redUpper2 = np.array([180,255,255])

# Get registred database (dictionnary)
with open("/home/pi/PET-TEO/Base_Donnees_Panneaux/Danger/fichier_base_danger","rb") as fichier:
	depickler_BD = pickle.Unpickler(fichier)
	base_danger = depickler_BD.load()
	
with open("/home/pi/PET-TEO/Base_Donnees_Panneaux/Indication/fichier_base_indication","rb") as fichier:
	depickler_BD = pickle.Unpickler(fichier)
	base_indication = depickler_BD.load()
	
with open("/home/pi/PET-TEO/Base_Donnees_Panneaux/Obligation/fichier_base_obligation","rb") as fichier:
	depickler_BD = pickle.Unpickler(fichier)
	base_obligation = depickler_BD.load()
	
with open("/home/pi/PET-TEO/Base_Donnees_Panneaux/Interdiction/fichier_base_interdiction","rb") as fichier:
	depickler_BD = pickle.Unpickler(fichier)
	base_interdiction = depickler_BD.load()
	

# capture frames from the camera 
for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
	
	image = frame.array 
	
	# Smooth the image
	median = cv2.medianBlur(image,5)

	# convert into HSV
	hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
	
	# construct mask for the color "blue"/"red"
	blueMask = cv2.inRange(hsv, blueLower, blueUpper)
	blueMask = cv2.erode(blueMask, None, iterations=2)
	blueMask = cv2.dilate(blueMask, None, iterations=2)
	
	redMask1 = cv2.inRange(hsv, redLower1, redUpper1)
	redMask1 = cv2.erode(redMask1, None, iterations=2)
	redMask1 = cv2.dilate(redMask1, None, iterations=2)

	redMask2 = cv2.inRange(hsv, redLower2, redUpper2)
	redMask2 = cv2.erode(redMask2, None, iterations=2)
	redMask2 = cv2.dilate(redMask2, None, iterations=2)	
	
	# add the masks in order to obtain region of interest
	Mask = blueMask + redMask1 + redMask2
	cv2.imshow("Seuillage",Mask)
	
	# find contours in the thresholded image and initialize the shape detector
	cnts = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()
	
	# loop over the contours
	for c in cnts:
		# compute the center of the contour, 
		# then detect the name of the shape using only the contour
		M = cv2.moments(c)
		if M["m00"] == 0: M["m00"]=1
		cX = int((M["m10"] / M["m00"]))
		cY = int((M["m01"] / M["m00"]))
		shape, crop_img = sd.detect(c, image, base_danger)
		
		# multiply the contour (x,y)-coordinates by the resize ratio, 
		# then draw the contours and the name of the shape on the image
		#cv2.drawContours(image, [c], -1, (0,255,0), 2)
		cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		
		# resize the image
	
	# show the output image
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	
	# if the 'q' key was pressed, break from the loop 
	if key == ord("q"):
		break		 
 
