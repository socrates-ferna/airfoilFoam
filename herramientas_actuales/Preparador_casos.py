#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:13:29 2019

@author: usuario
"""

import shutil
from math import sin, cos, pi
import os

#determinar angulos a ensayar
angulos = list(range(userdefrange));
#angulos = np.array(angulos)

#definir vector direcciones
cosenos= [ cos(angulos[i]*pi/180) for i in range(len(angulos))];
senos= [ sin(angulos[i]*pi/180) for i in range(len(angulos))];
velocidad=1;
angcoefs=[angulos[:],senos[:],cosenos[:]];

#Definir vector velocidades
vel,vely,velx=[],[],[];
for i in range(len(angulos)):
    velx.append(velocidad*cosenos[i])
    vely.append(velocidad*senos[i])
    vel.append([velx[i],vely[i]])

#comprobación
print (angcoefs)
print (vel)

#crear cada caso
#limpiar controlDict
#os.remove('NACA_641-212/system/controlDict')
#sustituir los guiones velocidades y posicioness
for i in range(len(angulos)):
    #angulo del caso
    angcaso= angcoefs[0][i]
    ruta=(str(angcaso))
    casocdr=(str(ruta)+'/system/controlDictref')
    casocd=(str(ruta)+'/system/controlDict')
    casoUr=(str(ruta)+'/0/Ureferencia')
    casoU=(str(ruta)+'/0/U')
    
    #determinamos nueva direccion
    nueva_direccion_lift ="    liftDir         ("+str(-angcoefs[1][i])+" 0 "+str(angcoefs[2][i])+");";
    nueva_direccion_drag ="    dragDir         ("+str(angcoefs[2][i])+" 0 "+str(angcoefs[1][i])+");";
    #determinamos nueva velocidade
    nuevo_internal_field ="internalField   uniform ("+str(vel[i][0])+" 0 "+str(vel[i][1])+");";
    nuevo_freestreamValue ="freestreamValue   uniform ("+str(vel[i][0])+" 0 "+str(vel[i][1])+");";
    nuevo_value=("value   uniform ("+str(vel[i][0])+" 0 "+str(vel[i][1])+");");
    
    #crear caso, creamos archivos particulares
    shutil.copytree('caso_gen', ruta)
    shutil.copy(str(casocdr),str(casocd))
    shutil.copy(str(casoUr),str(casoU))
    
    #nos metemos en el archivo controlDict y remplazamos
    controlD = open(str(casocd),"r")
    hbk = controlD.readlines()
    controlD.close()
    for j in range(len(hbk)):
        if "liftDir" in hbk[j]:
            print(hbk[j])
            hbk[j] = nueva_direccion_lift
            print(hbk[j])
        if "dragDir" in hbk[j]:
            print(hbk[j])
            hbk[j] = nueva_direccion_drag
            print(hbk[j])
    controlD = open(str(casocd),"w")
    controlD.writelines(hbk)
    controlD.close()
    
    #nos metemos en el archivo U y remplazamos
    guionU = open(str(casoU),"r")
    hbk = guionU.readlines()
    guionU.close()
    for j in range(len(hbk)):
        if "internalField   uniform" in hbk[j]:
            print(hbk[j])
            hbk[j] = nuevo_internal_field
            print(hbk[j])
    guionU = open(str(casoU),"w")        
    guionU.writelines(hbk)
    guionU.close()
    
    os.remove(str(ruta)+'/0/Ureferencia')   

#
#controlDict.read
#controlDict.write("")
#
#    U = open('/home/usuario/Documents/David/Casos/caso_gen/0/U','r+')
