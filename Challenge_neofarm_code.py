import numpy as np
import matplotlib.pyplot as plt
from copy import copy, deepcopy
import json

Plan=str(input("Entrer le plan dans lequel se trouve le robot maraîcher. Exemple: XY, ZX, XZ, YZ, etc. \n")).upper()
Axe=str(input("\nEntrer l'Axe sur lequel se trouve le centre du cercle. Exemple: X, Y ou Z \n")).upper()
r=float(input("\nEntrer la valeur du rayon, en précisant son signe. Exemple:-15, 3 etc. \n")) #signe définit ordonnée y
θ=abs(float(input("\nEntrer la valeur de l'angle θ (en degrés) à parcourir Exemple: 360, 125 etc. \n")))
sens=float(input("\nPréciser le sens de parcours du cercle: 1 pour le sens horaire, -1 pour antihoraire \n")) #-1 antitrigo = horaire, 1=trigo (horaire)
NbPoints =int(input("\nPréciser le nombre de points pour discréditer le cercle: (50 est le maximum) \n"))

sens=-sens #pour travailler en norme trigonométrique
# Plan='YZ'
# Axe='Y'
# r=-15
# θ=90
# sens=-1
# NbPoints=10

Absc_a=0 #Point de départ du robot
Ord_a=0
dθ= θ/(NbPoints-1)
Mat=np.zeros([NbPoints, 2]) #Matrice contenant les points

# Vérification que l'Axe est situé dans le plan
if Axe!=Plan[0] and Axe!=Plan[1]:
    print("Impossible! L'Axe doit être dans le plan! Pressez Ctrl + K pour réinitialiser la console puis rentrez des valeurs correctes")
    exit()

if Axe == 'X':
    Absc_0=r
    Ord_0=0
if Axe == 'Y' and (Plan=='XY' or Plan=='YX'):
    Ord_0=r
    Absc_0=0
if Axe == 'Y' and (Plan=='YZ' or Plan=='ZY'):
    Ord_0=0
    Absc_0=r
if Axe == 'Z':
    Ord_0=r
    Absc_0=0

#angle formé par le repère Ro'(Absc_0) et Ro(0,0)
if Absc_0==0:
    φ = np.pi/2*np.sign(Ord_0)
if Ord_0==0 and Absc_0>0:
    φ = 0
if Ord_0==0 and Absc_0<0:
    φ = np.pi

Mat_passage=[[np.cos(np.pi+φ),np.sin(np.pi+φ)],[-np.sin(np.pi+φ), np.cos(np.pi+φ)]] #Faire un dessin pour comprendre l'addition de pi à φ

angle = 0
for i in range(0,NbPoints):
    Absc=abs(r)*np.cos((angle))
    Ord=abs(r)*np.sin((angle))
    Absc,Ord=np.array([Absc,Ord]).dot(Mat_passage) #Permet d'effectuer la rotation de (x,y) écrit dans la base Ro' vers Ro
    Mat[(i,0)]=Absc+Absc_0
    Mat[(i,1)]=Ord+Ord_0
    angle = angle +sens*np.radians(dθ)
Absc_b=Mat[(NbPoints-1,0)]
Ord_b=Mat[(NbPoints-1,1)]

# Format number of Matrix
float_formatter = lambda x: "%.2f" % x

NewMat=np.zeros([NbPoints,3])
if Plan == 'XY' or Plan=='YX':
    Plan = 'XY'
    Letter = 'Z'
    #return (#,#,0)
    for i in range(NbPoints):
        NewMat[(i,0)]=float_formatter(Mat[(i,0)])
        NewMat[(i,1)]=float_formatter(Mat[(i,1)])
        NewMat[(i,2)]=float_formatter(0)
if Plan == 'YZ' or Plan=='ZY':
    Plan = 'YZ'
    Letter = 'X'
    for i in range(NbPoints):
        NewMat[(i,0)]=float_formatter(0)
        NewMat[(i,1)]=float_formatter(Mat[(i,0)])
        NewMat[(i,2)]=float_formatter(Mat[(i,1)])
    #return (0,#,#)
if Plan == 'XZ' or Plan=='ZX':
    Plan ='XZ'
    Letter = 'Y'
    for i in range(NbPoints):
        NewMat[(i,0)]=float_formatter(Mat[(i,0)])
        NewMat[(i,1)]=float_formatter(0)
        NewMat[(i,2)]=float_formatter(Mat[(i,1)])
    #return (#,0,#)

#---------Generate JSON
import os#must import this library
if os.path.exists('Liste_Points_Mvt_circulaire.json'):
    os.remove('Liste_Points_Mvt_circulaire.json') #this deletes the file.
    file = open('Liste_Points_Mvt_circulaire.json','w+')
    data ={'NB_POINTS': NbPoints, "POINT_LIST":NewMat.tolist()}
    file.write(str(data))
    file.close()
else:
    file = open('Liste_Points_Mvt_circulaire.json','w+')
    data ={'NB_POINTS': NbPoints, "POINT_LIST":NewMat.tolist()}
    file.write(str(data))
    file.close()


# --------2D plot
fig, ax = plt.subplots()
circle1 = plt.Circle((Absc_0, Ord_0), r, color='y', zorder=1)
ax.add_artist(circle1)
ax.scatter(Absc_b,Ord_b,c = 'red', zorder=2)
ax.scatter(Absc_a,Ord_a,c = 'red', zorder=3)
ax.scatter(Absc_0,Ord_0,c = 'red', zorder=4)
ax.plot(Mat[:,0], Mat[:,1], c= 'blue', zorder=5)
ax.set(xlabel=Plan[0], ylabel=Plan[1], title='Tracé du parcours')
ax.grid('equal')
plt.xlim(Absc_0-abs(r)-2,Absc_0+abs(r)+2 )
plt.ylim(Ord_0-abs(r)-2,Ord_0+abs(r)+2 )
ax.axhline(linewidth=1,zorder=1, color="k")
ax.axvline(linewidth=1,zorder=1,color="k")
plt.gca().set_aspect('equal', adjustable='box')
fig.savefig("test.png")
plt.show()