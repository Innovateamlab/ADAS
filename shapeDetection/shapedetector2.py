# import the necessary packages 
import cv2
import numpy as np
from scipy.spatial import distance as dist

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c, image, base):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		crop_img = []
		score = {}
		
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
			if ar >= 0.9 and ar <= 1.10:
				# draw the form
				cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
				# extract the form & the histogram from the crop
				crop_img = cv2.cvtColor(image[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY)
				hist_crop = cv2.calcHist([crop_img],[0],None,[256],[0,256])
				hist_crop = cv2.normalize(hist_crop, hist_crop).flatten()
				for key, hist_db in base.items():
					#size_img = img_db.shape
					#crop_img = cv2.resize(crop_img, size_img)
					#similitude = cv2.compareHist(hist_crop,hist_db, cv2.HISTCMP_CORREL)
					d = dist.euclidean(hist_crop,hist_db)
					score[key] = d
				# sort the results
				result = sorted([(v,k) for (k,v) in score.items()])
				print(result)
 
		# if the shape has 4 vertices, it is either a square or a rectangle
		elif len(approx) == 4:
			# a square will have an aspect ratio that is approximately equal to one, otherwise, the shape is a rectangle
			shape = "square"
			# compute the bounding box of the contour and use the bouding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
			if ar >= 0.95 and ar <= 1.05:
				# draw the form
				cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
				# extract the form
				crop_img = image[y:y+h,x:x+w]

		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
			if ar >= 0.95 and ar <= 1.05:
				# draw the form
				cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
				# extract the form
				crop_img = image[y:y+h,x:x+w]

		# return the name of the shape
		return shape
			
		

