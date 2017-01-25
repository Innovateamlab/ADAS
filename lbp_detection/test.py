
import os, sys, math
from lbp_matching import *



database_dic={}
imagedatabase = []
labels = []

imageTest = []

# Lien vers le dossier des images de la database
imagedatabase = cvutils.imlist("../lbp_detection/data/training/")
for index, imdatabase in enumerate (imagedatabase):
    # Lecture des images de la base pour avoir un array en h*w*3  (3 pour rgb)
    im = cv2.imread(imdatabase)
    # Conversion en noir et blanc pour avoir un array en 2 dimensions h*w.
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    # On remplit la liste labels. 1 label par photo de la base.
    labels.append(index)
    # le dico: key=label, value=array image
    database_dic[labels[index]] = im

imageTest = cvutils.imlist("../lbp_detection/data/test/")

for index, imTest in enumerate (imageTest):
    im = cv2.imread(imTest)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    imageTest[index]=im
    
sizeImages = 100 # taille en pixels des images de la database et de l'image cropped, redimmensionner
resultats, bestscore, label  = lbp_matching(imageTest,database_dic,sizeImages) 



