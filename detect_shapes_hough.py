# import the necessary packages
from shapeDetection.shapedetector import ShapeDetector
from picamera.array import PiRGBArray
from picamera import PiCamera 
import imutils
import cv2
import time
import numpy as np

# initialize the camera and grap a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# grab an image from the camera
camera.resolution = (680, 400)
camera.capture(rawCapture, format = "bgr")
image = rawCapture.array

# resize the image to a smaller factor so that the shapes can be approximated better
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly, and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
#thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find circles using Hough Transform
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

for i in circles[0,:]:
	# draw the outer circle
	cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
	# draw the center of the circle
	cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)	

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
