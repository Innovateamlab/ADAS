import os
import cv2
import cvutils
import numpy as np
import imutils
import csv
import matplotlib.pyplot as plt




# Ces fonctions utilise les librairies OpenCV.

# detect_shape_color
# En entrée prend : L'image à tester, la taille pour un optionnel redimesionnement déterminée dans main.py. 
# En sortie sort : La figure géométrique détectée, la couleur de la figure (si c'est une forme ronde), l'image du panneau "zoomé" en niveaux de gris

# database_reader
# En entrée prend : La figure géométrique détectée, la couleur de la figure
# En sortie sort : La base de données conforme à shape et color (sous forme d'un dictionnaire) avec un label attribué par panneaux
class CV_bloc:
    def __init__(self):
        pass


    def detect_shape_color(self,image_test,newSize): #1

        # Bloc image_test
        color = "undefined"
        shape = "undefined"
        crop_image = [[]]
        crop_img_gray = [[]]
        im = cv2.imread(image_test)
        im_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(im_gray, (5,5), 0)
        thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)[1]

        # Find contours in the thresholded image and initialize the shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        
        
        for c in cnts:
            # compute the center of the contour, then detect the name of the shape using only the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
               cX = int((M["m10"] / M["m00"]))   
               cY = int((M["m01"] / M["m00"]))   
            else:
               cX = 0
               cY = 0
            shape,color,crop_img = CV_bloc.detect(c,im)
            #fonction detect
            if len(crop_img)>1:
                 h,w,d = crop_img.shape
                 if h<11:
                     shape="undefined"
                     color="undefined"
                     crop_img= [[]]
                 else:
                         #RESIZE ! Mais les fonctions marchent moyennement
                         crop_img_gray = cv2.cvtColor(crop_img,cv2.COLOR_RGB2GRAY)
                         #crop_img_gray = np.resize(crop_img_gray,(newSize,newSize))
                     
                         cv2.imshow("Cropped_image", crop_img_gray)
                         cv2.waitKey(0)

                         # multiply the contour (x,y)-coordinates by the resize ratio, then draw the contours and the name of the shape on the image
                         c = c.astype("float")
                         c = c.astype("int")
                         cv2.drawContours(im, [c], -1, (0,255,0), 2)
                         cv2.putText(im, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                         cv2.imshow("Image", im)
                         cv2.waitKey(0)
                         break
                        
            else:
                shape="undefined"
                color="undefined"
                crop_img_gray= [[]]
            

        return shape,color, crop_img_gray




    def detect(c,image): #2
                # initialize the shape name and approximate the contour
                shape = "unidentified"
                color = "unidentified"
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.04 * peri, True)
                crop_img = []
                image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                
                # if the shape is a triangle, it will have 3 vertices
                if len(approx) == 3:
                        shape = "triangle"
                        (x, y, w, h) = cv2.boundingRect(approx)
                        ar = w / float(h)
                        if ar >= 0.9 and ar <= 1.10:
                                # draw the form
                                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2) #image_gray p-ê?
                                # extract the form & the histogram from the crop
                                crop_img = image[y:y+h,x:x+w]    
 
                # if the shape has 4 vertices, it is either a square or a rectangle
                elif len(approx) == 4:
                        # a square will have an aspect ratio that is approximately equal to one, otherwise, the shape is a rectangle
                        shape = "square"
                        # compute the bounding box of the contour and use the bouding box to compute the aspect ratio
                        (x, y, w, h) = cv2.boundingRect(approx)
                        ar = w / float(h)
                        if ar >= 0.95 and ar <= 1.05:
                                # draw the form
                                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2) #image_gray p-ê?
                                # extract the form
                                crop_img = image[y:y+h,x:x+w]

                # otherwise, we assume the shape is a circle
                else:
                        shape = "circle"
                        (x, y, w, h) = cv2.boundingRect(approx)
                        ar = w / float(h)
                        if ar >= 0.95 and ar <= 1.05:
                                # draw the form
                                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2) #image_gray p-ê?
                                # extract the form
                                crop_img = image[y:y+h,x:x+w]
                                crop_img_gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
                                h,w = crop_img_gray.shape
                                # extract the color
                                (b1,g1,r1) = crop_img[int(0.05*h),int(0.5*w)] #pixel Ouest
                                (b2,g2,r2) = crop_img[int(0.95*h),int(0.5*w)] #pixel Est
                                (b3,g3,r3) = crop_img[int(0.5*h),int(0.05*w)] #pixel Nord
                                (b4,g4,r4) = crop_img[int(0.5*h),int(0.95*w)] #pixel Sud
                                #print("rouge", r1,r2,r3,r4, "\nbleu",b1,b2,b3,b4)
                                r = r1/4 + r2/4 + r3/4 + r4/4 
                                b = b1/4 + b2/4 + b3/4 + b4/4
                                
                                if  r > b:
                                    color = "red"
                                else:
                                    color = "blue"

                return shape, color, crop_img                
                


    def database_reader(self,shape,color,newSize): #3

        database_dic = {}
        labels = []
        imagedatabase = []
    
        # Bloc image database (train_dic)
        if shape == "triangle":
            imagedatabase = cvutils.imlist("../Fonction_bloc_opencv/data/Base_Donnees_Panneaux/Danger/")
            for index, imdatabase in enumerate (imagedatabase):
                # Lecture des images de la base pour avoir un array en h*w*3  (3 pour rgb)
                im = cv2.imread(imdatabase)
                # Conversion en noir et blanc pour avoir un array en 2 dimensions h*w.
                im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
                # Resize
                im = np.resize(im,(newSize,newSize)) 
                # On remplit la liste labels. 1 label par photo de la base.
                labels.append(index)
                # le dico: key=label, value=array image
                database_dic[labels[index]] = im
        
        elif shape == "square":
            imagedatabase = cvutils.imlist("../Fonction_bloc_opencv/data/Base_Donnees_Panneaux/Indication/")
            for index, imdatabase in enumerate (imagedatabase):
                # Lecture des images de la base pour avoir un array en h*w*3  (3 pour rgb)
                im = cv2.imread(imdatabase)
                # Conversion en noir et blanc pour avoir un array en 2 dimensions h*w.
                im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
                # Resize
                im = np.resize(im,(newSize,newSize)) 
                # On remplit la liste labels. 1 label par photo de la base.
                labels.append(index)
                # le dico: key=label, value=array image
                database_dic[labels[index]] = im
        
        elif shape == "circle":
            if color=="red":
                imagedatabase = cvutils.imlist("../Fonction_bloc_opencv/data/Base_Donnees_Panneaux/Interdiction/")
                for index, imdatabase in enumerate (imagedatabase):
                   # Lecture des images de la base pour avoir un array en h*w*3  (3 pour rgb)
                   im = cv2.imread(imdatabase)
                   # Conversion en noir et blanc pour avoir un array en 2 dimensions h*w.
                   im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
                   # Resize
                   im = np.resize(im,(newSize,newSize))              
                   # On remplit la liste labels. 1 label par photo de la base.
                   labels.append(index)
                   # le dico: key=label, value=array image
                   database_dic[labels[index]] = im
        
            else:
                imagedatabase = cvutils.imlist("../Fonction_bloc_opencv/data/Base_Donnees_Panneaux/Obligation/")
                for index, imdatabase in enumerate (imagedatabase):
                   # Lecture des images de la base pour avoir un array en h*w*3  (3 pour rgb)
                   im = cv2.imread(imdatabase)
                   # Conversion en noir et blanc pour avoir un array en 2 dimensions h*w.
                   im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
                   # Resize
                   im = np.resize(im,(newSize,newSize)) 
                   # On remplit la liste labels. 1 label par photo de la base.
                   labels.append(index)
                   # le dico: key=label, value=array image
                   database_dic[labels[index]] = im
                        
        return database_dic



