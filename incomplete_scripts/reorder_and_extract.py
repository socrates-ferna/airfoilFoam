#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
#import airfoil_treatment
#SELECCIONADOR DE BORDE DE ATAQUE

#ATMO & FLIGHT CONDITIONS
c=3; rho=1.225; U=51;


# In[2]:


#nuestro vector de entrada por terminal debería ser el:
#[nombre del archivo a leer, el nombre del output, porcentaje de la cuerda que nos quedamos]
#Pendiente hacerlo interactivo, añadir el switch (en favoritos) para sacar las etiquetas que quiera
#elegir si borde de ataque o de salida
#pendiente testear a ver si también lo saca bien para todas las deformadas
xref=sys.argv[3]
xref=float(xref)
yref=.05
foil=pd.read_csv(sys.argv[1],sep=';')
current_labels=list(foil.columns)
default_labels=["U:0","U:1","U:2","nuTilda","nut","p","yPlus","Points:0","Points:1","Points:2"]
new_labels=['p', 'x', 'y', 'Cp', 'p_muestra']
foil.drop_duplicates(subset='x', inplace=True)

# In[3]:


def rename_labels(passed_foil,new_labels,current_labels):
    paired_labels=dict(zip(current_labels,new_labels))
    passed_foil.rename(columns=paired_labels,inplace=True)
#rename_labels(foil,new_labels,current_labels)


# In[19]:


foil=foil[foil.x < xref]
foil.x=foil.x-xref
foil.y=foil.y-yref
foil['zcomplementario']=foil.y-1j*foil.x
foil=foil.iloc[np.angle(foil.zcomplementario).argsort()]
foil.x=foil.x+xref
foil.y=foil.y+yref
#fig=plt.plot(foil.x,foil.y)
#fig.show()

# In[20]:


foil.p = foil.p*2 #transformamos a Cp
foil.p = foil.p*0.5*rho*(U**2)  #transformamos a p-p_inf en Pa
foil.x, foil.y = foil.x*c*1000, foil.y*c*1000
out_labels=['x','y','p']
foil.to_csv(sys.argv[2], sep=';', columns=out_labels, index=False)

