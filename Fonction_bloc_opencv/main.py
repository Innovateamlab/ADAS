import sys, os, math
from cv_bloc import CV_bloc
import cvutils
import numpy as np





# Taille des images à redimmesionner. Optionnel.
# Les fonctions resize ne fonctionnent pas bien. Décommentez/commentez les lignes 54, 163,177,191,206 pour resize.  
Size=100

# Image test 
imagetest = cvutils.imlist("../Fonction_bloc_opencv/data/test/")
for im in imagetest:
    # Fonction CV_bloc contient toutes les fonctions opencv nécéssaires
    CV = CV_bloc()
    #Get shape, color and crop_image_test
    shape, color, crop_img_gray= CV.detect_shape_color(im,Size)
    #Show the results
    print(" Shape : ",shape)
    print(" Color : ",color)    
    #Import the right dictionnary
    database_dic = CV.database_reader(shape, color, Size)

    

