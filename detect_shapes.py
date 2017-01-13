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
camera.resolution = (800, 600)
camera.capture(rawCapture, format = "bgr")
image = rawCapture.array

# resize the image to a smaller factor so that the shapes can be approximated better
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly, and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)[1]

cv2.imshow("Debug",thresh)
cv2.waitKey(0)

# find contours in the thresholded image and initialize the shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the shape using only the contour
	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"])*ratio)
	cY = int((M["m01"] / M["m00"])*ratio)
	shape = sd.detect(c)

	# multiply the contour (x,y)-coordinates by the resize ratio, then draw the contours and the name of the shape on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0,255,0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)
