# OpenCV bindings
import cv2
# TO performing path manipulations
import os
# Local Binary Pattern function
from skimage.feature import local_binary_pattern
#To calculate a normalized histogram
from scipy.stats import itemfreq
from sklearn.preprocessing import normalize

import cvutils
# To read class from file
import csv
# To wrap my .txt file in .csv file
from io import TextIOWrapper
# To display plot and subplot
import matplotlib.pyplot as plt
# Numpy to use arrays
import numpy as np


def lbp_matching(test_list,train_dic,sizeImages=100):

    ## TRAINING SET PART

    #List for storing the LBP Histograms, adress of images and corresponding labels
    X_test=[]
    X_label=[]
    
    #print("test dic : ", train_dic)
    #print("liste : ",test_list)
    
    #For each image in the training set calculate the LBP histogram
    # and update X_test, X_name and y_test
    for label,im in train_dic.items():
        # Resize the image to 100x100, np.darray.resize
        im.resize((sizeImages,sizeImages), refcheck= False)
        radius = 3
        # Number of points to be considered as neighbourers
        no_points = 8 * radius
        # Uniform LBP is used
        # P-ê erreur ici. lbp accepte un format différent? Array n'est p-e pas le bon? à voir
        lbp = local_binary_pattern(im,no_points,radius,method='uniform')
        # Calculate the histogram
        X = itemfreq(lbp.ravel())
        A = 26*[[0,0]]
        A = np.asarray(A)
        for x in X:
            A[int(x[0])][0]=x[0]
            A[int(x[0])][1]=x[1]
        for index, a in enumerate(A):
            A[index][0]=index
        # Normalize the histogram
        hist = A[:,1]/(sum(A[:,1]))
        # Append image path in X_name
        X_label.append(label)
        # Append histogram to X_name
        X_test.append(hist)
        
    


## TESTING IMAGES PART

    for im in test_list:
        # Resize the image to 100x100, np.darray.resize
        im.resize((sizeImages,sizeImages), refcheck=False)
        radius = 3
        #Number of points to be considered as neighbourers
        no_points = 8 * radius
        #Uniform LBP is used
        lbp = local_binary_pattern(im, no_points, radius, method='uniform')
        #Calculate the histogram
        X = itemfreq(lbp.ravel())
        A = 26*[[0,0]]
        A = np.asarray(A)
        for x in X:
            A[int(x[0])][0]=x[0]
            A[int(x[0])][1]=x[1]
        for index, a in enumerate(A):
            A[index][0]=index        
        #Normalize the histogram
        hist = A[:,1]/sum(A[:,1])
        # Initialisation de results
        results = []
        #Results = {}
        #j=1
        #For each image in the training dataset
        # Calculate the chi-squared distance and the sort the values
        for index, i in enumerate(X_test):
            score = cv2.compareHist(np.array(i, dtype=np.float32), np.array(hist, dtype=np.float32), cv2.HISTCMP_CHISQR)
            results.append((X_label[index],round(score,3)))
            print(" rrrrrr :", results)
            print(index)
            #if index==(len(X_label)-1):
             #   Results["im"]=results
             #   j=j+1
    results = sorted(results, key=lambda score: score[1])
    
    #print("Results : ", Results) 
    label = results[0][0]
    bestscore = results[0][1]

    print("Nb label", X_label)
    print("results : ", results)
    print("label : ",label)
    print("bestscore : ", bestscore)
   
    return results, bestscore, label
    
    
