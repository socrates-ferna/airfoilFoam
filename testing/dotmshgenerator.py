#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 08:25:17 2019

@author: usuario
"""
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, pi

###################################################################################################################################

#             ORDENAR LOS PUNTOS PARA CREAR EL PERFIL

###################################################################################################################################

data=np.genfromtxt('airfoil_file.csv',delimiter=',',names=True)

a=data
ptosorig= [ 0 for i in range(len(a['X'])) ]
ptoc= []
ptosextaux= []
ptosintaux= []
ptosext= []
ptosint= []

c= 1

#POSICIONES PORCENTUALES DE LOS BLOQUES
peri= 5   ;peri2= 50
pere= 1  ;distrug= 25

for i in range(len(a['X'])):
    ptosorig[i]=[a['X'][i],a['Y'][i]]
      
###########################################################################################
#             ORDENAMOS LOS PUNTOS
###########################################################################################
    
#Determinamos pto borde de salida será nuestro punto inicial
pos1= np.argmax(a['X'])
ptoc.append(ptosorig[pos1])
ptosorig.pop(pos1)

#DEFINIMOS LINEA MEDIA
def linea_media(x):
    f= -2.3933044298*x**6+8.1445548453*x**5-10.9549147363*x**4+7.3382035032*x**3-2.5712651537*x**2+0.4067841764*x+0.0971833586-0.0675    
    return f

#SEPARAMOS EN INTRADOS Y EXTRADOS
for i in range(len(ptosorig)):
    referencia = linea_media(ptosorig[i][0])
    if ptosorig[i][1]>=referencia:
        ptosextaux.append(ptosorig[i])
    else:
        ptosintaux.append(ptosorig[i])
        
#FUNCION QUE HALLA LAS DISTANCIAS ABSOLUTAS
def distancia(p0x,p0y,p1x,p1y):
    dist= (p0x-p1x)**2+(p1y-p0y)**2
    return dist

#FUNCION QUE HALLA LAS DISTANCIAS EN EJE DE ORDENADAS
def distx(p0,p1):
    dist= (p0-p1)**2
    return float(dist)


#INTRODUCIMOS PUNTOS EN INTRADÓS Y EXTRADÓS
while len(ptosintaux)>0:
    dist= [ distancia(ptoc[-1][0],ptoc[-1][1],ptosintaux[i][0],ptosintaux[i][1]) for i in range(len(ptosintaux)) ]
    minpos= dist.index(min(dist))
    ptoc.append(ptosintaux[minpos])
    ptosint.append(ptosintaux[minpos])
    ptosintaux.pop(minpos)
cuerda= abs(ptoc[0][-1]-ptoc[0][0])
while len(ptosextaux)>0:
    dist= [ distancia(ptoc[-1][0],ptoc[-1][1],ptosextaux[i][0],ptosextaux[i][1])for i in range(len(ptosextaux)) ]
    minpos= dist.index(min(dist))
    ptoc.append(ptosextaux[minpos])
    ptosext.append(ptosextaux[minpos])
    ptosextaux.pop(minpos)
    
ptosext= tuple(ptosext)
ptosint= tuple(ptosint)
    
#FUNCION QUE ELIGE UN PUNTO DEL MAS CERCANO A VERTICE X
def punto_correcto(puntos,percent,c):
    ref=c*percent
    dists=[]
    for i in range(len(puntos)):
        dist = distx(puntos[i][0],ref)
        dists.append(dist)
    min_dist= min(dists)
    dists = np.array(dists)
    pos = np.where(dists==min_dist)[0][0]
    return pos

###########################################################################################
#             CAMBIAR PUNTOS PARA AJUSTAR POSICIÓN DE BLOQUES EN EL PERFIL
###########################################################################################

#PUNTO DEL BORDE DE SALIDA
ptole= 1

#PUNTO DONDE EMPIEZA EL PRIMER BLOQUE DEL INTRADÓS
ptoint= ptole+punto_correcto(ptosint,peri/100,cuerda)

#PUNTO DONDE EMPIEZA TIRA RUGOSA
ptorug = ptole+len(ptosint)+punto_correcto(ptosext,pere/100,cuerda)

#PUNTO DONDE EMPIEZA EL BLOQUE DEL EXTRADÓS
ptosup = ptole+len(ptosint)+punto_correcto(ptosext,(pere+distrug)/100,cuerda)

#PUNTO DONDE EMPIEZA EL SEGUNDO BLOQUE DEL INTRADÓS 
ptoinf = ptole+punto_correcto(ptosint,peri2/100,cuerda)


#Mostrar perfil
puntos = np.array(ptoc)
plt.plot(puntos[:,0],puntos[:,1])
plt.show()

###########################################################################################
#            ESCRIBE GUIÓN DEL GMESH PARA CREAR LA MALLA
###########################################################################################

np.savetxt('airfoil_file.dat', puntos, fmt='%.8e')
ficherofin= open('airfoil_mesh.geo', 'w')

###########################################################################################
#             CREAMOS PUNTOS Y LINEAS DE LAS MALLA
###########################################################################################

for i in range(len(puntos)):
    ficherofin.write("Point(" + str(i+1) + ") = {" + str(puntos[i,0]) + "," + str(puntos[i,1]) + ", 0};" + '\n')
# spline 1 intrados from LE to ptoinf
sp1=1
ficherofin.write("Spline(" + str(sp1) + ") = {" + str(1) + ":"+ str(ptoinf) + "};" + '\n' )
# spline 2 intrados from ptoinf to ptoint
sp2=2
ficherofin.write("Spline(" + str(sp2) + ") = {" + str(ptoinf) + ":"+ str(ptoint) + "};" + '\n' )
# spline 1 intrados from ptoint to ptorug
sp3=3
ficherofin.write("Spline(" + str(sp3) + ") = {" + str(ptoint) + ":"+ str(ptorug) + "};" + '\n' )
# spline zona rugosidad
sp4=4
ficherofin.write("Spline(" + str(sp4) + ") = {" + str(ptorug) + ":"+ str(ptosup) + "};" + '\n' )
# spline 1 intrados from ptosup to LE
sp5=5
ficherofin.write("Spline(" + str(sp5) + ") = {" + str(ptosup) + ":" + str(len(puntos)) + "," + str(1) + "};" + '\n' )


diff_extr = len(puntos)+10

for i in range(len(puntos)):
    ficherofin.write("Point(" + str(diff_extr+i+1) + ") = {" + str(puntos[i,0]) + "," + str(puntos[i,1]) + ", 1};" + '\n')
# spline 1 intrados from LE to ptoinf
sp1e=6
ficherofin.write("Spline(" + str(sp1e) + ") = {" + str(diff_extr+1) + ":"+ str(diff_extr+ptoinf) + "};" + '\n' )
# spline 2 intrados from ptoinf to ptoint
sp2e=7
ficherofin.write("Spline(" + str(sp2e) + ") = {" + str(diff_extr+ptoinf) + ":"+ str(diff_extr+ptoint) + "};" + '\n' )
# spline 1 intrados from ptoint to ptosup
sp3e=8
ficherofin.write("Spline(" + str(sp3e) + ") = {" + str(diff_extr+ptoint) + ":"+ str(diff_extr+ptorug) + "};" + '\n' )
# spline 1 intrados from ptoint to ptosup
sp4e=9
ficherofin.write("Spline(" + str(sp4e) + ") = {" + str(diff_extr+ptorug) + ":"+ str(diff_extr+ptosup) + "};" + '\n' )
# spline 1 intrados from ptosup to LE
sp5e=10
ficherofin.write("Spline(" + str(sp5e) + ") = {" + str(diff_extr+ptosup) + ":" + str(diff_extr+len(puntos)) + "," + str(len(puntos)+11) + "};" + '\n' )

numsplines = 10

angulorug = 15*pi/180
angulosup = 75*pi/180
angulomedio = -70*pi/180
anguloinf = -80*pi/180
centre = [c, 0.0]
R = cuerda*30 
puntoFF7 = [ centre[0]-R*cos(angulorug), centre[1]+R*sin(angulorug) ]
puntoFF9 = [ centre[0]-R*cos(angulosup), centre[1]+R*sin(angulosup) ]
puntoFF1 = [ centre[0]-R*cos(angulomedio), centre[1]+R*sin(angulomedio) ]
puntoFF8 = [ centre[0]-R*cos(anguloinf), centre[1]+R*sin(anguloinf) ]

#puntos y lineas del FF
# front
pto_front = len(puntos)+1
ficherofin.write("Point(" + str(pto_front) + ") = {" + str(puntoFF1[0]) + ","+str(puntoFF1[1]) +", 0};" + '\n')
# superior
pto_sup = len(puntos)+2
ficherofin.write("Point(" + str(pto_sup) + ") = {" + str(cuerda) + ", " + str(cuerda*30) + ", 0};" + '\n')
# inferior
pto_inf = len(puntos)+3
ficherofin.write("Point(" + str(pto_inf) + ") = {" + str(cuerda) + ", " + str(-cuerda*30) + ", 0};" + '\n')
# sup wake
pto_supwake = len(puntos)+4
ficherofin.write("Point(" + str(pto_supwake) + ") = {" + str((cuerda)*50) + ", " + str((cuerda)*30) + ", 0};" + '\n')
# middle wake
pto_midwake = len(puntos)+5
ficherofin.write("Point(" + str(pto_midwake) + ") = {" + str((cuerda)*50) + ", 0, 0};" + '\n')
# inf wake
pto_infwake = len(puntos)+6
ficherofin.write("Point(" + str(pto_infwake) + ") = {" + str((cuerda)*50) + ", " + str((-cuerda)*30) + ", 0};" + '\n')
# front rug
pto_rug = len(puntos)+7
ficherofin.write("Point(" + str(pto_rug) + ") = {" + str(puntoFF7[0]) + ","+str(puntoFF7[1]) +", 0};" + '\n')
# front sup
pto_frontsup = len(puntos)+8
ficherofin.write("Point(" + str(pto_frontsup) + ") = {" + str(puntoFF9[0]) + ","+str(puntoFF9[1]) +", 0};" + '\n')
# front inf
pto_frontinf = len(puntos)+9
ficherofin.write("Point(" + str(pto_frontinf) + ") = {" + str(puntoFF8[0]) + ","+str(puntoFF8[1]) +", 0};" + '\n')

#new_points_FF_extrusion = 2*len(puntos)+8

# same with extusion
# front
ficherofin.write("Point(" + str(pto_front+diff_extr) + ") = {" + str(puntoFF1[0]) + ","+str(puntoFF1[1]) +", 1.0};" + '\n')
# superior
ficherofin.write("Point(" + str(pto_sup+diff_extr) + ") = {" + str(cuerda) + ", " + str(cuerda*30) + ", 1.0};" + '\n')
# inferior
ficherofin.write("Point(" + str(pto_inf+diff_extr) + ") = {" + str(cuerda) + ", " + str(-cuerda*30) + ", 1.0};" + '\n')
# sup wake
ficherofin.write("Point(" + str(pto_supwake+diff_extr) + ") = {" + str((cuerda)*50) + ", " + str((cuerda)*30) + ", 1.0};" + '\n')
# middle wake
ficherofin.write("Point(" + str(pto_midwake+diff_extr) + ") = {" + str((cuerda)*50) + ", 0, 1.0};" + '\n')
# inf wake
ficherofin.write("Point(" + str(pto_infwake+diff_extr) + ") = {" + str((cuerda)*50) + ", " + str((-cuerda)*30) + ", 1.0};" + '\n')
# front rug
ficherofin.write("Point(" + str(pto_rug+diff_extr) + ") = {" + str(puntoFF7[0]) + ","+str(puntoFF7[1]) +", 1.0};" + '\n')
# front sup
ficherofin.write("Point(" + str(pto_frontsup+diff_extr) + ") = {" + str(puntoFF9[0]) + ","+str(puntoFF9[1]) +", 1.0};" + '\n')
# front inf
ficherofin.write("Point(" + str(pto_frontinf+diff_extr) + ") = {" + str(puntoFF8[0]) + ","+str(puntoFF8[1]) +", 1.0};" + '\n')

#lineas círculo
"+ str(1) +"
#linea superior
C1 = numsplines+1
ficherofin.write("Circle("+ str(C1) +") = {" + str(pto_sup) + ","+ str(1) + "," + str(pto_frontsup) + "};" + '\n' )
#linea superior extrusión
C1e = numsplines+2
ficherofin.write("Circle("+ str(C1e) +") = {" + str(pto_sup+diff_extr) + "," + str(1+diff_extr) + "," + str(pto_frontsup+diff_extr) + "};" + '\n' )
#linea superior rugosidad
C2 = numsplines+3
ficherofin.write("Circle("+ str(C2) +") = {" + str(pto_frontsup) + ","+ str(1) + "," + str(pto_rug) + "};" + '\n' )
#linea superior rugosidad extrusión
C2e = numsplines+4
ficherofin.write("Circle("+ str(C2e) +") = {" + str(pto_frontsup+diff_extr) + ","+ str(1+diff_extr) + "," + str(pto_rug+diff_extr) + "};" + '\n' )
#linea rugosidad entrada
C3 = numsplines+5
ficherofin.write("Circle("+ str(C3) +") = {" + str(pto_rug) + ","+ str(1) + "," + str(pto_front) + "};" + '\n' )
#linea rugosidad entrada extrusión
C3e = numsplines+6
ficherofin.write("Circle("+ str(C3e) +") = {" + str(pto_rug+diff_extr) + ","+ str(1+diff_extr) + "," + str(pto_front+diff_extr) + "};" + '\n' )
#linea inferior entrada
C4 = numsplines+7
ficherofin.write("Circle("+ str(C4) +") = {" + str(pto_front) + ","+ str(1) + "," + str(pto_frontinf) + "};" + '\n' )
#linea inferior entrada extrusión
C4e = numsplines+8
ficherofin.write("Circle("+ str(C4e) +") = {" + str(pto_front+diff_extr) + ","+ str(1+diff_extr) + "," + str(pto_frontinf+diff_extr) + "};" + '\n' )
#linea inferior
C5 = numsplines+9
ficherofin.write("Circle("+ str(C5) +") = {" + str(pto_frontinf) + ","+ str(1) + "," + str(pto_inf) + "};" + '\n' )
#linea infreior extrusión
C5e= numsplines+10
ficherofin.write("Circle("+ str(C5e) +") = {" + str(pto_frontinf+diff_extr) + ","+ str(1+diff_extr) + "," + str(pto_inf+diff_extr) + "};" + '\n' )
numcirc=10

#lineas estela
#linea superior estela
E1 = numsplines+numcirc+1
ficherofin.write("Line("+ str(E1) +") = {" + str(pto_sup) + ","+ str(pto_supwake) + "};" + '\n' )
#linea superior estela extrusión
E1e = numsplines+numcirc+2
ficherofin.write("Line("+ str(E1e) +") = {" + str(pto_sup+diff_extr) + ","+ str(pto_supwake+diff_extr) + "};" + '\n' )
#linea superior salida
E2 = numsplines+numcirc+3
ficherofin.write("Line("+ str(E2) +") = {" + str(pto_supwake) + ","+ str(pto_midwake) + "};" + '\n' )
#linea superior salida extrusión
E2e = numsplines+numcirc+4
ficherofin.write("Line("+ str(E2e) +") = {" + str(pto_supwake+diff_extr) + ","+ str(pto_midwake+diff_extr) + "};" + '\n' )
#linea inferior salida
E3 = numsplines+numcirc+5
ficherofin.write("Line("+ str(E3) +") = {" + str(pto_midwake) + ","+ str(pto_infwake) + "};" + '\n' )
#linea inferior salida extrusión
E3e = numsplines+numcirc+6
ficherofin.write("Line("+ str(E3e) +")= {" + str(pto_midwake+diff_extr) + ","+ str(pto_infwake+diff_extr) + "};" + '\n' )
#linea inferior estela
E4 = numsplines+numcirc+7
ficherofin.write("Line("+ str(E4) +") = {" + str(pto_infwake) + ","+ str(pto_inf) + "};" + '\n' )
#linea inferior estela extrusión
E4e = numsplines+numcirc+8
ficherofin.write("Line("+ str(E4e) +") = {" + str(pto_infwake+diff_extr) + ","+ str(pto_inf+diff_extr) + "};" + '\n' )
numest=8

#lineas radiales
#linea radial entrada
R1 = numsplines+numcirc+numest+1
ficherofin.write("Line("+ str(R1) +") = {" + str(ptoint) + ","+ str(pto_front) + "};" + '\n' )
#linea radial entrada ext
R1e = numsplines+numcirc+numest+2
ficherofin.write("Line("+ str(R1e) +") = {" + str(ptoint+diff_extr) + ","+ str(pto_front+diff_extr) + "};" + '\n' )
#linea radial entrada sup
R2 = numsplines+numcirc+numest+3
ficherofin.write("Line("+ str(R2) +") = {" + str(ptosup) + ","+ str(pto_frontsup) + "};" + '\n' )
#linea radial entrada sup ext
R2e = numsplines+numcirc+numest+4
ficherofin.write("Line("+ str(R2e) +") = {" + str(ptosup+diff_extr) + ","+ str(pto_frontsup+diff_extr) + "};" + '\n' )
#linea radial entrada inf
R3 = numsplines+numcirc+numest+5
ficherofin.write("Line("+ str(R3) +") = {" + str(ptoinf) + ","+ str(pto_frontinf) + "};" + '\n' )
#linea radial entrada inf ext
R3e = numsplines+numcirc+numest+6
ficherofin.write("Line("+ str(R3e) +") = {" + str(ptoinf+diff_extr) + ","+ str(pto_frontinf+diff_extr) + "};" + '\n' )
#linea radial sup
R4 = numsplines+numcirc+numest+7
ficherofin.write("Line("+ str(R4) +") = {" + str(1) + ","+ str(pto_sup) + "};" + '\n' )
#linea radial sup ext
R4e = numsplines+numcirc+numest+8
ficherofin.write("Line("+ str(R4e) +") = {" + str(1+diff_extr) + ","+ str(pto_sup+diff_extr) + "};" + '\n' )
#linea radial inf
R5 = numsplines+numcirc+numest+9
ficherofin.write("Line("+ str(R5) +") = {" + str(1) + ","+ str(pto_inf) + "};" + '\n' )
#linea radial inf ext
R5e = numsplines+numcirc+numest+10
ficherofin.write("Line("+ str(R5e) +") = {" + str(1+diff_extr) + ","+ str(pto_inf+diff_extr) + "};" + '\n' )
#linea radial salida 
R6 = numsplines+numcirc+numest+11
ficherofin.write("Line("+ str(R6) +") = {" + str(1) + ","+ str(pto_midwake) + "};" + '\n' )
#linea radial salida ext
R6e = numsplines+numcirc+numest+12
ficherofin.write("Line("+ str(R6e) +") = {" + str(1+diff_extr) + ","+ str(pto_midwake+diff_extr) + "};" + '\n' )
#linea radial rugosidad
R7 = numsplines+numcirc+numest+13
ficherofin.write("Line("+ str(R7) +") = {" + str(ptorug) + ","+ str(pto_rug) + "};" + '\n' )
#linea radial rugosidad ext
R7e = numsplines+numcirc+numest+14
ficherofin.write("Line("+ str(R7e) +") = {" + str(ptorug+diff_extr) + ","+ str(pto_rug+diff_extr) + "};" + '\n' )
numrad=14

lineascaras= numsplines+numcirc+numest+numrad

#Lineas de union entre ambas caras
# front
line_front = lineascaras+1
ficherofin.write("Line(" + str(line_front) + ") = {" + str(pto_front) + ","+str(pto_front+diff_extr) +"};" + '\n')
# superior
line_sup = lineascaras+2
ficherofin.write("Line(" + str(line_sup) + ") = {" + str(pto_sup) + ", " + str(pto_sup+diff_extr) + "};" + '\n')
# inferior
line_inf = lineascaras+3
ficherofin.write("Line(" + str(line_inf) + ") = {" + str(pto_inf) + ", " + str(pto_inf+diff_extr) + "};" + '\n')
# sup wake
line_supwake = lineascaras+4
ficherofin.write("Line(" + str(line_supwake) + ") = {" + str(pto_supwake) + ", " + str(pto_supwake+diff_extr) + "};" + '\n')
# middle wake
line_midwake = lineascaras+5
ficherofin.write("Line(" + str(line_midwake) + ") = {" + str(pto_midwake) + "," + str(pto_midwake+diff_extr) + "};" + '\n')
# inf wake
line_infwake = lineascaras+6
ficherofin.write("Line(" + str(line_infwake) + ") = {" + str(pto_infwake) + ", " + str(pto_infwake+diff_extr) + "};" + '\n')
# front sup
line_frontsup = lineascaras+7
ficherofin.write("Line(" + str(line_frontsup) + ") = {" + str(pto_frontsup) + ","+str(pto_frontsup+diff_extr) +"};" + '\n')
# front inf
line_frontinf = lineascaras+8
ficherofin.write("Line(" + str(line_frontinf) + ") = {" + str(pto_frontinf) + ","+str(pto_frontinf+diff_extr) +"};" + '\n')
#perfil LE
linele = lineascaras+9
ficherofin.write("Line(" + str(linele) + ") = {" + str(ptole) + ","+str(ptole+diff_extr) +"};" + '\n')
#perfil sup
linesup = lineascaras+10
ficherofin.write("Line(" + str(linesup) + ") = {" + str(ptosup) + ","+str(ptosup+diff_extr) +"};" + '\n')
#perfil inf
lineinf = lineascaras+11
ficherofin.write("Line(" + str(lineinf) + ") = {" + str(ptoinf) + ","+str(ptoinf+diff_extr) +"};" + '\n')
#perfil front
linefront = lineascaras+12
ficherofin.write("Line(" + str(linefront) + ") = {" + str(ptoint) + ","+str(ptoint+diff_extr) +"};" + '\n')
#perfil rug
linerug = lineascaras+13
ficherofin.write("Line(" + str(linerug) + ") = {" + str(ptorug) + ","+str(ptorug+diff_extr) +"};" + '\n')
#FF rug
line_rug = lineascaras+14
ficherofin.write("Line(" + str(line_rug) + ") = {" + str(pto_rug) + ","+str(pto_rug+diff_extr) +"};" + '\n')


###########################################################################################
#             CREAMOS CARAS DE LA MALLA
###########################################################################################
"+ str() + "
#Line Loops
#superficie 
ficherofin.write("Line Loop(1) = {"+ str(sp5) + ","+ str(R4) + ","+ str(C1) + ","+ str(-R2) + "};" + '\n' )
ficherofin.write("Line Loop(2) = {"+ str(sp4) + ","+ str(R2) + ","+ str(C2) + ","+ str(-R7) + "};" + '\n' )
ficherofin.write("Line Loop(3) = {"+ str(sp3) + ","+ str(R7) + ","+ str(C3) + ","+ str(-R1) + "};" + '\n' )
ficherofin.write("Line Loop(4) = {"+ str(sp2) + ","+ str(R1) + ","+ str(C4) + ","+ str(-R3) + "};" + '\n' )
ficherofin.write("Line Loop(5) = {"+ str(sp1) + ","+ str(R3) + ","+ str(C5) + ","+ str(-R5) + "};" + '\n' )
ficherofin.write("Line Loop(6) = {"+ str(R5) + ","+ str(-E4) + ","+ str(-E3) + ","+ str(-R6) + "};" + '\n' )
ficherofin.write("Line Loop(7) = {"+ str(R6) + ","+ str(-E2) + ","+ str(-E1) + ","+ str(-R4) + "};" + '\n' )

#superficie extruida
ficherofin.write("Line Loop(8) = {"+ str(sp5e) + ","+ str(R4e) + ","+ str(C1e) + ","+ str(-R2e) + "};" + '\n' )
ficherofin.write("Line Loop(9) = {"+ str(sp4e) + ","+ str(R2e) + ","+ str(C2e) + ","+ str(-R7e) + "};" + '\n' )
ficherofin.write("Line Loop(10) = {"+ str(sp3e) + ","+ str(R7e) + ","+ str(C3e) + ","+ str(-R1e) + "};" + '\n' )
ficherofin.write("Line Loop(11) = {"+ str(sp2e) + ","+ str(R1e) + ","+ str(C4e) + ","+ str(-R3e) + "};" + '\n' )
ficherofin.write("Line Loop(12) = {"+ str(sp1e) + ","+ str(R3e) + ","+ str(C5e) + ","+ str(-R5e) + "};" + '\n' )
ficherofin.write("Line Loop(13) = {"+ str(R5e) + ","+ str(-E4e) + ","+ str(-E3e) + ","+ str(-R6e) + "};" + '\n' )
ficherofin.write("Line Loop(14) = {"+ str(R6e) + ","+ str(-E2e) + ","+ str(-E1e) + ","+ str(-R4e) + "};" + '\n' )

#superficie perfil
ficherofin.write("Line Loop(15) = {"+ str(sp1) + ","+ str(lineinf) + ","+ str(-sp1e) + ","+ str(-linele) + "};" + '\n' )
ficherofin.write("Line Loop(16) = {"+ str(sp2) + ","+ str(linefront) + ","+ str(-sp2e) + ","+ str(-lineinf) + "};" + '\n' )
ficherofin.write("Line Loop(17) = {"+ str(sp3) + ","+ str(linerug) + ","+ str(-sp3e) + ","+ str(-linefront) + "};" + '\n' )
ficherofin.write("Line Loop(18) = {"+ str(sp4) + ","+ str(linesup) + ","+ str(-sp4e) + ","+ str(-linerug) + "};" + '\n' )
ficherofin.write("Line Loop(19) = {"+ str(sp5) + ","+ str(linele) + ","+ str(-sp5e) + ","+ str(-linesup) + "};" + '\n' )


#superficie freestream
ficherofin.write("Line Loop(20) = {"+ str(C1) + ","+ str(line_frontsup) + ","+ str(-C1e) + ","+ str(-line_sup) + "};" + '\n' )
ficherofin.write("Line Loop(21) = {"+ str(C2) + ","+ str(line_rug) + ","+ str(-C2e) + ","+ str(-line_frontsup) + "};" + '\n' )
ficherofin.write("Line Loop(22) = {"+ str(C3) + ","+ str(line_front) + ","+ str(-C3e) + ","+ str(-line_rug) + "};" + '\n' )
ficherofin.write("Line Loop(23) = {"+ str(C4) + ","+ str(line_frontinf) + ","+ str(-C4e) + ","+ str(-line_front) + "};" + '\n' )
ficherofin.write("Line Loop(24) = {"+ str(C5) + ","+ str(line_inf) + ","+ str(-C5e) + ","+ str(-line_frontinf) + "};" + '\n' )
ficherofin.write("Line Loop(25) = {"+ str(-E1) + ","+ str(line_sup) + ","+ str(E1e) + ","+ str(-line_supwake) + "};" + '\n' )
ficherofin.write("Line Loop(26) = {"+ str(-E2) + ","+ str(line_supwake) + ","+ str(E2e) + ","+ str(-line_midwake) + "};" + '\n' )
ficherofin.write("Line Loop(27) = {"+ str(-E3) + ","+ str(line_midwake) + ","+ str(E3e) + ","+ str(-line_infwake) + "};" + '\n' )
ficherofin.write("Line Loop(28) = {"+ str(-E4) + ","+ str(line_infwake) + ","+ str(E4e) + ","+ str(-line_inf) + "};" + '\n' )

#superficies interiores
ficherofin.write("Line Loop(29) = {"+ str(R1) + ","+ str(line_front) + ","+ str(-R1e) + ","+ str(-linefront) + "};" + '\n' )
ficherofin.write("Line Loop(30) = {"+ str(R2) + ","+ str(line_frontsup) + ","+ str(-R2e) + ","+ str(-linesup) + "};" + '\n' )
ficherofin.write("Line Loop(31) = {"+ str(R3) + ","+ str(line_frontinf) + ","+ str(-R3e) + ","+ str(-lineinf) + "};" + '\n' )
ficherofin.write("Line Loop(32) = {"+ str(R4) + ","+ str(line_sup) + ","+ str(-R4e) + ","+ str(-linele) + "};" + '\n' )
ficherofin.write("Line Loop(33) = {"+ str(R5) + ","+ str(line_inf) + ","+ str(-R5e) + ","+ str(-linele) + "};" + '\n' )
ficherofin.write("Line Loop(34) = {"+ str(R6) + ","+ str(line_midwake) + ","+ str(-R6e) + ","+ str(-linele) + "};" + '\n' )
ficherofin.write("Line Loop(35) = {"+ str(R7) + ","+ str(line_rug) + ","+ str(-R7e) + ","+ str(-linerug) + "};" + '\n' )


#superficie
ficherofin.write("Surface(1) = {1};" + '\n' )
ficherofin.write("Surface(2) = {2};" + '\n' )
ficherofin.write("Surface(3) = {3};" + '\n' )
ficherofin.write("Surface(4) = {4};" + '\n' )
ficherofin.write("Surface(5) = {5};" + '\n' )
ficherofin.write("Surface(6) = {6};" + '\n' )
ficherofin.write("Surface(7) = {7};" + '\n' )
ficherofin.write("Surface(8) = {8};" + '\n' )
ficherofin.write("Surface(9) = {9};" + '\n' )
ficherofin.write("Surface(10) = {10};" + '\n' )
ficherofin.write("Surface(11) = {11};" + '\n' )
ficherofin.write("Surface(12) = {12};" + '\n' )
ficherofin.write("Surface(13) = {13};" + '\n' )
ficherofin.write("Surface(14) = {14};" + '\n' )
ficherofin.write("Surface(15) = {15};" + '\n' )
ficherofin.write("Surface(16) = {16};" + '\n' )
ficherofin.write("Surface(17) = {17};" + '\n' )
ficherofin.write("Surface(18) = {18};" + '\n' )
ficherofin.write("Surface(19) = {19};" + '\n' )
ficherofin.write("Surface(20) = {20};" + '\n' )
ficherofin.write("Surface(21) = {21};" + '\n' )
ficherofin.write("Surface(22) = {22};" + '\n' )
ficherofin.write("Surface(23) = {23};" + '\n' )
ficherofin.write("Surface(24) = {24};" + '\n' )
ficherofin.write("Surface(25) = {25};" + '\n' )
ficherofin.write("Surface(26) = {26};" + '\n' )
ficherofin.write("Surface(27) = {27};" + '\n' )
ficherofin.write("Surface(28) = {28};" + '\n' )
ficherofin.write("Surface(29) = {29};" + '\n' )
ficherofin.write("Surface(30) = {30};" + '\n' )
ficherofin.write("Surface(31) = {31};" + '\n' )
ficherofin.write("Surface(32) = {32};" + '\n' )
ficherofin.write("Surface(33) = {33};" + '\n' )
ficherofin.write("Surface(34) = {34};" + '\n' )
ficherofin.write("Surface(35) = {35};" + '\n' )

###########################################################################################
#             Determinamos grosor de la capa límite
###########################################################################################

#y+ hallado con la calculadora online
sumat, y, indice = 0, 0.00016641005886756873, 0
#ratio de crecimiento escogido por nosotros
RT = 1.1
vector= []

while sumat<=R:
    sumat += y*RT**indice
    indice= indice+1
    vector.append(sumat) 

print(sumat)
print(indice)

###########################################################################################
#             Determinamos numero de celdas por bloque y grading
###########################################################################################
# 

ficherofin.write("Transfinite Line{"+str(line_front)+","+str(line_frontsup)+","+str(line_frontinf)+","+str(line_sup)+","+str(line_inf)+","+str(line_midwake)+","+str(line_rug)+"} = "+str(2)+" Using Progression 1.0;" + '\n' )

#mallado
ficherofin.write("Transfinite Line{"+str(R1)+","+str(R2)+","+str(R3)+","+str(R4)+","+str(R5)+","+str(R7)+","+str(R1e)+","+str(R2e)+","+str(R3e)+","+str(R4e)+","+str(R5e)+","+str(R7e)+"} = "+str(indice)+" Using Progression "+str(RT)+";" + '\n' )
ficherofin.write("Transfinite Line{"+str(-E2)+","+str(E3)+","+str(-E2e)+","+str(E3e)+"} = "+str(indice)+" Using Progression 1.025;" + '\n' )

# airfoil
ficherofin.write("Transfinite Line{"+str(sp1)+","+str(sp1e)+"} = "+str(60)+" Using Progression 1.04;" + '\n' )
ficherofin.write("Transfinite Line{"+str(-C5)+","+str(-C5e)+"} = "+str(60)+" Using Progression 1.05;" + '\n' )
ficherofin.write("Transfinite Line{"+str(sp2)+","+str(sp2e)+"} = "+str(50)+" Using Progression 0.97;" + '\n' )
ficherofin.write("Transfinite Line{"+str(-C4)+","+str(-C4e)+"} = "+str(50)+" Using Bump 5.0;" + '\n' )
ficherofin.write("Transfinite Line{"+str(sp3)+","+str(sp3e)+"} ="+str(80)+" Using Bump 3.0;" + '\n' )
ficherofin.write("Transfinite Line{"+str(C3)+","+str(C3e)+"} = "+str(80)+" Using Bump 0.1;" + '\n' )
ficherofin.write("Transfinite Line{"+str(sp4)+","+str(sp4e)+"} = "+str(80)+" Using Progression 1.0;" + '\n' )
ficherofin.write("Transfinite Line{"+str(C2)+","+str(C2e)+"} = "+str(80)+" Using Bump 1.0;" + '\n' )
ficherofin.write("Transfinite Line{"+str(sp5)+","+str(sp5e)+"} = "+str(80)+" Using Bump 0.13;" + '\n' )
ficherofin.write("Transfinite Line{"+str(C1)+","+str(C1e)+"} = "+str(80)+" Using Progression 1.03;" + '\n' )
# wake
#ficherofin.write("Transfinite Line{"+str(R6)+","+str(E1)+","+str(-E4)+","+str(R6e)+","+str(E1e)+","+str(-E4e)+"} = "+str(190)+" Using Progression 1.037;" + '\n' )
ficherofin.write("Transfinite Line{"+str(R6)+","+str(R6e)+"} = "+str(160)+" Using Progression 1.037;" + '\n' )
ficherofin.write("Transfinite Line{"+str(E1)+","+str(-E4)+","+str(E1e)+","+str(-E4e)+"} = "+str(160)+" Using Progression 1.032;" + '\n' )

'''
ficherofin.write("Transfinite Line{1:56} = "+str(10)+" Using Progression 1.00;" + '\n' )
'''
########################################################################################### 
#             Determinamos volumenes
###########################################################################################

ficherofin.write("Transfinite Surface{1:35};" + '\n' )
ficherofin.write("Recombine Surface{1:35};" + '\n' )

#No hace falta poner las caras en un orden concreto
ficherofin.write("Surface loop(1) = {"+ str(1) + ","+ str(8)  + ","+ str(19) + ","+ str(20)+ ","+ str(30)+ ","+ str(32) + "};" + '\n' )
ficherofin.write("Surface loop(2) = {"+ str(2) + ","+ str(9)  + ","+ str(18) + ","+ str(21)+ ","+ str(30)+ ","+ str(35) + "};" + '\n' )
ficherofin.write("Surface loop(3) = {"+ str(3) + ","+ str(10)  + ","+ str(17) + ","+ str(22)+ ","+ str(29)+ ","+ str(35) + "};" + '\n' )
ficherofin.write("Surface loop(4) = {"+ str(4) + ","+ str(11) + ","+ str(16) + ","+ str(23)+ ","+ str(29)+ ","+ str(31) + "};" + '\n' )
ficherofin.write("Surface loop(5) = {"+ str(5) + ","+ str(12) + ","+ str(15) + ","+ str(24)+ ","+ str(31)+ ","+ str(33) + "};" + '\n' )
ficherofin.write("Surface loop(6) = {"+ str(6) + ","+ str(13) + ","+ str(27) + ","+ str(28)+ ","+ str(33)+ ","+ str(34) + "};" + '\n' )
ficherofin.write("Surface loop(7) = {"+ str(7) + ","+ str(14) + ","+ str(25) + ","+ str(26)+ ","+ str(32)+ ","+ str(34) + "};" + '\n' )

ficherofin.write("Volume(1) = {1};" + '\n' )
ficherofin.write("Volume(2) = {2};" + '\n' )
ficherofin.write("Volume(3) = {3};" + '\n' )
ficherofin.write("Volume(4) = {4};" + '\n' )
ficherofin.write("Volume(5) = {5};" + '\n' )
ficherofin.write("Volume(6) = {6};" + '\n' )
ficherofin.write("Volume(7) = {7};" + '\n' )

ficherofin.write("Transfinite Volume{1:7};" + '\n' )

#NOTA!!!: EL GMSH4 NO VA CON EL OPENFOAM, HAY QUE USAR EL GMSH3 (SOLO CAMBIA 'Curve Loop' por 'Line Loop')


ficherofin.write("Mesh 3;" + '\n' )

###########################################################################################
#             Determinamos nombres de las superficies y volúmenes físicos
###########################################################################################

ficherofin.write("Physical Surface('Farfield') = {20,21,22,23,24,25,26,27,28};" + '\n' )
ficherofin.write("Physical Surface('Foil') = {15,16,17,18,19};" + '\n' )
ficherofin.write("Physical Surface('Symmetry1') = {1,2,3,4,5,6,7};" + '\n' )
ficherofin.write("Physical Surface('Symmetry2') = {8,9,10,11,12,13,14};" + '\n' )
#
ficherofin.write("Physical Volume('FLUID') = {1:7};" + '\n' )
ficherofin.write("Save 'airfoil_mesh.msh';" + '\n' )

ficherofin.close()
