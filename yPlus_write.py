#!/usr/bin/env python3
import os
from configuration import *
import sys
sys.path.append('ThirdParty/BL_yplus_calculator')
sys.path.append('herramientas_actuales/')
import yplus_calculation as yp

# To date, we need first cell height to configure dotgeogenerator.py (in herramientas_actuales/)
# we look into the firsCellHeight line in the file and replace it
# me voy a escribir el código específico, la abstracción queda pendiente
file = 'dotgeogenerator.py'
path = 'herramientas_actuales/'
filepath = path + file
pattern = 'firstCellHeight = '
#now we calculate first layer height with parameters defined in configuration.py
y = yp.main(desired_yPlus, rho, Umag, chord, mu, print_boolean=True)

#imports to manage/read/write files
from tempfile import mkstemp
from shutil import move, copymode

absfilepath = os.path.abspath(filepath) #better to use absolute paths to file
with open(filepath) as f:
    fh, temp_path = mkstemp() #temporary empty file created. temp_path is absolute!
    new_file = open(temp_path,'w') #open object for our temp file in write mode
    #we already have the old file open as f
    for line in f:
        if pattern in line:
            new_file.write(pattern + str(y) + ' \n')
            print("I wrote this line:", pattern + str(y))
        elif 'current_yPlus = ' in line:
            new_file.write('current_yPlus = ' + str(desired_yPlus) + '\n')
            print('yPlus flag updated: ', str(desired_yPlus))
        else:
            new_file.write(line)
    copymode(absfilepath, temp_path)
    os.remove(absfilepath)
    move(temp_path, absfilepath)
#the syntax "with" in line 24 closes the file automatically when we're done

print("yPlus-calculated first cell height substituted")