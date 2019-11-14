import numpy as np
import matplotlib.pyplot as plt
from copy import copy, deepcopy
import json

#Sens de l'angle: A - O - B

# Plan=str(input("Entrer le plan dans lequel se trouve le robot maraîher. Exemple: ZX, XZ, YZ, etc.XZ \n"))
# axe=str(input("\nEntrer l'axe sur lequel se trouve le centre du cercle. Exemple: X, Y ou Z \n"))
# r=float(input("\nEntrer la valeur du rayon, en précisant son signe. Exemple:-15, 3 etc. \n")) #signe définit ordonnée y
# θ=abs(float(input("\nEntrer la valeur de l'angle θ (en degrés) à parcourir Exemple: 360, 125 etc. \n")))
# sens=float(input("\nPréciser le sens de parcours du cercle: -1 pour le sens horaire, 1 pour antihoraire \n")) #-1 antitrigo = horaire, 1=trigo (horaire)
# NbPoints =int(input("\nPréciser le nombre de points pour discréditer le cercle: \n"))

Plan='XZ'
axe='X'
r=-15
θ=150
sens=-1
NbPoints=20

Absc_a=0 #Point de départ du robot
Ord_a=0
dθ= θ/(NbPoints)
Mat=np.zeros([NbPoints, 2]) #Matrice contenant les points

# Vérification que l'axe est situé dans le plan
if axe!=Plan[0] and axe!=Plan[1]:
    print("Impossible! L'axe doit être dans le plan! Pressez Ctrl + K pour réinitialiser la console puis rentrez des valeurs correctes")
    exit()

#Détermination des coordonnées du centre O
if axe == 'X':
    Absc_0=0
    Ord_0=r
if axe == 'Y':
    Ord_0=0
    Absc_0=r
if axe == 'Z':
    Ord_0=0
    Absc_0=r

print("xo = ", Absc_0, ", yo = ", Ord_0)



#angle formé par le repère Ro'(Absc_0) et Ro(0,0)
if Absc_0==0:
    φ = np.pi/2*np.sign(Ord_0)
if Ord_0==0 and Absc_0>0:
    φ = 0
elif Ord_0==0 and Absc_0<0:
    φ = np.pi
elif Absc_0>0:
    φ = np.arctan(Ord_0/Absc_0)
elif Absc_0<0 and Ord_0<0:
    φ = np.pi+abs(np.arctan(Ord_0/Absc_0))
elif Absc_0<0 and Ord_0>0:
    φ = np.pi-abs(np.arctan(Ord_0/Absc_0))

print("φ B par rapport à Ro,", np.degrees(φ))
Mat_passage=[[np.cos(np.pi+φ),np.sin(np.pi+φ)],[-np.sin(np.pi+φ), np.cos(np.pi+φ)]]

angle = 0
for i in range(0,NbPoints):
    Absc=abs(r)*np.cos((angle))
    Ord=abs(r)*np.sin((angle))
    Absc,Ord=np.array([Absc,Ord]).dot(Mat_passage)
    Mat[(i,0)]=Absc+Absc_0
    Mat[(i,1)]=Ord+Ord_0
    angle = angle +sens*np.radians(dθ)
Absc_b=Mat[(NbPoints-1,0)]
Ord_b=Mat[(NbPoints-1,1)]

print("angle = ", np.degrees(angle))

# #Format number of Matrix
float_formatter = lambda x: "%.2f" % x

NewMat=np.zeros([NbPoints,3])
if Plan == 'XY' or 'YX':
    Letter = 'Z'
    #return (#,#,0)
    for i in range(L):
        NewMat[(i,0)]=float_formatter(Mat[(i,0)])
        NewMat[(i,1)]=float_formatter(Mat[(i,1)])
        NewMat[(i,2)]=float_formatter(0)
if Plan == 'YZ' or 'ZY':
    Letter = 'X'
    for i in range(L):
        NewMat[(i,0)]=float_formatter(0)
        NewMat[(i,1)]=float_formatter(Mat[(i,0)])
        NewMat[(i,2)]=float_formatter(Mat[(i,1)])
    #return (0,#,#)
if Plan == 'XZ' or Plan=='ZX':
    Letter = 'Y'
    for i in range(L):
        NewMat[(i,0)]=float_formatter(Mat[(i,0)])
        NewMat[(i,1)]=float_formatter(0)
        NewMat[(i,2)]=float_formatter(Mat[(i,1)])
    #return (#,0,#)



#---------Generate JSON
# json.dumps(NewMat)
file = open('Liste_Points_Mvt_circulaire.json','w+')
data ={'NB_POINTS': NbPoints, "POINT_LIST":NewMat.tolist()}
file.write(str(data))
file.close()



# -----------------2D plot
fig, ax = plt.subplots()
print("Mat = ", NewMat)
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
plt.gca().set_aspect('equal', adjustable='box')
fig.savefig("test.png")
plt.show()

