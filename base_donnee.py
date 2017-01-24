import cv2
import numpy as np
import os
import pickle

########################################################################
#DANGER
os.chdir("/home/pi/PET-TEO/Base_Donnees_Panneaux/Danger")

base_danger = {}

vir_d = cv2.imread("A1a.bmp",0)
vir_g = cv2.imread("A1b.bmp",0)
virs_d = cv2.imread("A1c.bmp",0)
virs_g = cv2.imread("A1d.bmp",0)
cassis = cv2.imread("A2a.bmp",0)
ralentis = cv2.imread("A2b.bmp",0)
chaussee_retrecie = cv2.imread("A3.bmp",0)
chaussee_retrecie_d = cv2.imread("A3a.bmp",0)
chaussee_retrecie_g = cv2.imread("A3b.bmp",0)
chaussee_glissante = cv2.imread("A4.bmp",0)

base_danger["Virage à droite"] = vir_d
base_danger["Virage à gauche"] = vir_g
base_danger["Succession de virages (droite)"] = virs_d
base_danger["Succession de virages (gauche)"] = virs_g
base_danger["Cassis"] = cassis
base_danger["Ralentissement"] = ralentis
base_danger["Chaussée rétrécie"] = chaussee_retrecie
base_danger["Chaussée rétrécie par la droite"] = chaussee_retrecie_d
base_danger["Chaussée rétrécie par la gauche"] = chaussee_retrecie_g
base_danger["Chaussée glissante"] = chaussee_glissante

with open("fichier_base_danger", "wb") as fichier:
	pickler_BD = pickle.Pickler(fichier)
	pickler_BD.dump(base_danger)

########################################################################
#INDICATION	
os.chdir("/home/pi/PET-TEO/Base_Donnees_Panneaux/Indication")

base_indication = {}

parking = cv2.imread("C1a.bmp",0)
sept_zero = cv2.imread("C4a_ex2.bmp",0)
taxi = cv2.imread("C5.bmp",0)
bus = cv2.imread("C6.bmp",0)
tram = cv2.imread("C7.bmp",0)
droit = cv2.imread("C12.bmp",0)
impasse = cv2.imread("C13a.bmp",0)
pre_impasse = cv2.imread("C13b.bmp",0)
priorite = cv2.imread("C18.bmp",0)
pieton = cv2.imread("C20a.bmp",0)

base_indication["Lieu stationnement"] = parking
base_indication["Vitesse conseillée"] = sept_zero
base_indication["Station de taxis"] = taxi
base_indication["Arrêt d'autobus"] = bus
base_indication["Arrêt de tramway"] = tram
base_indication["Circulation à sens unique"] = droit
base_indication["Impasse"] = impasse
base_indication["Présignalisation d'une impasse"] = pre_impasse
base_indication["Priorité par rapport au sens inverse"] = priorite
base_indication["Passage pour piéton"] = pieton

with open("fichier_base_indication", "wb") as fichier:
	pickler_BD = pickle.Pickler(fichier)
	pickler_BD.dump(base_indication)

########################################################################
#OBLIGATION
os.chdir("/home/pi/PET-TEO/Base_Donnees_Panneaux/Obligation")

base_obligation = {}

d = cv2.imread("B21-1.bmp",0)
g = cv2.imread("B21-2.bmp",0)
b_d = cv2.imread("B21a1.bmp",0)
b_g = cv2.imread("B21a2.bmp",0)
tout_droit = cv2.imread("B21b.bmp",0)
pro_d = cv2.imread("B21c1.bmp",0)
pro_g = cv2.imread("B21c2.bmp",0)
td_d = cv2.imread("B21d1.bmp",0)
td_g = cv2.imread("B21d2.bmp",0)
g_d = cv2.imread("B21e.bmp",0)
cycle = cv2.imread("B22a.bmp",0)
pieton = cv2.imread("B22b.bmp",0)

base_obligation["Obligation de tourner à droite"] = d
base_obligation["Obligation de tourner à gauche"] = g
base_obligation["Contournement obligatoire par la droite"] = b_d
base_obligation["Contournement obligatoire par la gauche"] = b_g
base_obligation["Direction obligatoire : tout droit"] = tout_droit
base_obligation["Direction obligatoire : à droite"] = pro_d
base_obligation["Direction obligatoire : à gauche"] = pro_g
base_obligation["Direction obligatoire : tout droit ou à droite"] = td_d
base_obligation["Direction obligatoire : tout droit ou à gauche"] = td_g
base_obligation["Direction obligatoire : à droite ou à gauche"] = g_d
base_obligation["Piste obligatoire pour les cycles"] = cycle
base_obligation["Chemin obligatoire pour les piétons"] = pieton

with open("fichier_base_obligation", "wb") as fichier:
	pickler_BD = pickle.Pickler(fichier)
	pickler_BD.dump(base_obligation)

########################################################################
#INTERDICTION
os.chdir("/home/pi/PET-TEO/Base_Donnees_Panneaux/Interdiction")

base_interdiction = {}

circulation = cv2.imread("B0.bmp",0)
sens_interdit = cv2.imread("B1.bmp",0)
gauche = cv2.imread("B2a.bmp",0)
droite = cv2.imread("B2b.bmp",0)
demi_tour = cv2.imread("B2c.bmp",0)
depasse = cv2.imread("B3.bmp",0)
pieton = cv2.imread("B9a.bmp",0)
cycle = cv2.imread("B9b.bmp",0)
bus = cv2.imread("B9f.bmp",0)
cinq_zero = cv2.imread("B14_50.bmp",0)
pas_priorite = cv2.imread("B15.bmp",0)

base_interdiction["Circulation interdite"] = circulation
base_interdiction["Sens interdit"] = sens_interdit
base_interdiction["Interdiction de tourner à gauche"] = gauche
base_interdiction["Interdiction de tourner à droite"] = droite
base_interdiction["Interdiction de faire demi-tour"] = demi_tour
base_interdiction["Interdiction de dépasser tous les véhicules à moteur"] = depasse
base_interdiction["Accès interdit aux piétons"] = pieton
base_interdiction["Accès interdit aux cycles"] = cycle
base_interdiction["Accès interdit aux véhicules de transport en commun"] = bus
base_interdiction["Limitation de vitesse"] = cinq_zero
base_interdiction["Cédez le passage à la circulation venant en sens inverse"] = pas_priorite

with open("fichier_base_interdiction", "wb") as fichier:
	pickler_BD = pickle.Pickler(fichier)
	pickler_BD.dump(base_interdiction)
