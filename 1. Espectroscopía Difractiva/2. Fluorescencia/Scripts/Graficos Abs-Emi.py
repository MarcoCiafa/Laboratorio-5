# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 11:43:27 2022

@author: Cami_
"""

#%%

import os
import numpy as np
import pandas as pd
# from scipy import signal
# from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

#%%

''' Grafico Transmisión de la lámpara '''

Lamp_Path = r"C:\Users\Cami_\Documents\UBA\Laboratorio 5\1. Espectrometría Difractiva\2. Fluorescencia\1. Muestras\Absorción\Lado Largo\Lámpara - Agua.csv"


Lamp    = pd.read_csv(Lamp_Path,
                      sep=";",
                      engine="python",
                      skiprows= 33,
                      skipfooter=1,
                      header=None,
                      names=["Longitud de Onda (nm)",
                             "Intensidad (u.a.)"]
                      )


LampWavelength  = Lamp["Longitud de Onda (nm)"]
LampIntensity   = Lamp["Intensidad (u.a.)"]


# Grafico
fig = plt.figure(1, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

DeltaxM = 200
Deltaxm = 2 
DeltayM =   0.2
Deltaym = 2

ax.xaxis.set_major_locator(MultipleLocator(DeltaxM))
ax.xaxis.set_minor_locator(AutoMinorLocator(Deltaxm))
ax.yaxis.set_major_locator(MultipleLocator(DeltayM))
ax.yaxis.set_minor_locator(AutoMinorLocator(Deltaym))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

ax.plot(LampWavelength,
         LampIntensity,
         color="black",
         lw=1,
         label='Lámpara (Agua)')
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad (u. a)', fontsize=16)
ax.legend(fontsize=15)



#%%

''' Datos Transmisión '''


DirPath_T = (r"C:\Users\Cami_\Documents\UBA\Laboratorio 5\1. Espectrometría Difractiva"
            r"\2. Fluorescencia\1. Muestras\Absorción\Lado Largo")


# Archivos a leer:
# Labels = [1,2,3,5,9,10,11,12,13,14,15,16,17,18]
# Labels = [12,13,14,15,16,17,18]
# Labels = [4, 6, 7, 8]
Labels = [4]

TransFiles = []
for i in Labels:
    TransFiles.append(f"{i} - Trans - Cum.csv")

TransPaths = []
for TransiFile in TransFiles:
    TransPaths.append(os.path.join(DirPath_T,
                               TransiFile)
    )

T = []
for TransiPath in TransPaths:
    T.append(pd.read_csv(TransiPath,
                         sep=";",
                         engine="python",
                         skiprows= 33,
                         skipfooter=1,
                         header=None,
                         names=["Longitud de Onda (nm)",
                                "Intensidad (u.a.)"]
                         )
    )

Wavelength = T[0]["Longitud de Onda (nm)"]
TIntensities = []
for Ti in T:
    TIntensities.append(Ti["Intensidad (u.a.)"])
    
    
#%%

''' Grafico Transmisión'''


# Grafico Crudo
fig = plt.figure(2, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

DeltaxM = 200
Deltaxm = 2 
DeltayM =   0.2
Deltaym = 2

ax.xaxis.set_major_locator(MultipleLocator(DeltaxM))
ax.xaxis.set_minor_locator(AutoMinorLocator(Deltaxm))
ax.yaxis.set_major_locator(MultipleLocator(DeltayM))
ax.yaxis.set_minor_locator(AutoMinorLocator(Deltaym))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

n = len(TIntensities)
color=iter(cm.rainbow(np.linspace(0,1,n)))


ax.plot(LampWavelength,
         LampIntensity,
         color="black",
         lw=1,
         label='Agua')

for i, TIntensitiesi in enumerate(TIntensities):
    colour = next(color)
    ax.plot(Wavelength,
             TIntensitiesi,
             label=str(Labels[i],),
             color= colour
             )
    
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad (u. a)', fontsize=16)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          title='Muestra :',
          title_fontsize=15,
          fontsize=15)


#%%

''' Suavizado de los Datos (Transmisión Rodamina y Lámpara (agua) ) '''

def MA(Signal, WindowSize):
    """
        Signal: Señal a suavizar con la media móvil.
        WindowSize: Cantidad de muestras a promediar
                    (los extremos promedian con menos)
    """

    # Kernel de la convolución (todos 1 porque queremos el promedio)
    Window  = np.ones(int(WindowSize)) / float(WindowSize)

    MA      = np.convolve(Signal, Window, 'same')
    return MA

SmoothT = []
for Ti in TIntensities:
    SmoothT.append(MA(Ti, 100))
    
SmoothLamp = MA(LampIntensity, 100)
    
#%%

# Grafico Suavizado
fig = plt.figure(3, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

DeltaxM = 200
Deltaxm = 2 
DeltayM =   0.2
Deltaym = 2

ax.xaxis.set_major_locator(MultipleLocator(DeltaxM))
ax.xaxis.set_minor_locator(AutoMinorLocator(Deltaxm))
ax.yaxis.set_major_locator(MultipleLocator(DeltayM))
ax.yaxis.set_minor_locator(AutoMinorLocator(Deltaym))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

n = len(SmoothT)
color=iter(cm.rainbow(np.linspace(0,1,n)))


ax.plot(LampWavelength,
          SmoothLamp,
          color="black",
          lw=1,
          label='Agua')

for i, SmoothTi in enumerate(SmoothT):
    colour = next(color)
    ax.plot(Wavelength,
             SmoothTi,
             label=str(Labels[i],),
             color= colour
             )
    
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad (u. a)', fontsize=16)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          title='Muestra :',
          title_fontsize=15,
          fontsize=15)


#%%


''' Cálculo de Absorción '''

SmoothA = 1 - SmoothT / SmoothLamp

fig = plt.figure(4, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

DeltaxM = 200
Deltaxm = 2 
DeltayM =   0.2
Deltaym = 2

ax.xaxis.set_major_locator(MultipleLocator(DeltaxM))
ax.xaxis.set_minor_locator(AutoMinorLocator(Deltaxm))
ax.yaxis.set_major_locator(MultipleLocator(DeltayM))
ax.yaxis.set_minor_locator(AutoMinorLocator(Deltaym))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

n = len(SmoothA)
color=iter(cm.rainbow(np.linspace(0,1,n)))


# ax.plot(LampWavelength,
#           SmoothLamp,
#           color="black",
#           lw=1,
#           label='Agua')

for i, SmoothAi in enumerate(SmoothA):
    colour = next(color)
    ax.plot(Wavelength,
             SmoothAi,
             label=str(Labels[i],),
             color= colour
             )
    
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad (u. a)', fontsize=16)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          title='Muestra :',
          title_fontsize=15,
          fontsize=15)




#%%


''' Datos Emisión '''

DirPath_E = (r"C:\Users\Cami_\Documents\UBA\Laboratorio 5\1. Espectrometría Difractiva"
            r"\2. Fluorescencia\1. Muestras\Emisión\Lado Largo")


# Archivos a leer:
#Labels = [12,13,14,15,16,17,18]
# Labels = [1,2,3,5,9,10,11,12,13,14,15,16,17,18]
# Labels = [4, 6, 7, 8]
Labels = [12]

EmiFiles = []
for i in Labels:
    EmiFiles.append(f"{i} - Emi - Rod.csv")

EmiPaths = []
for EmiiFile in EmiFiles:
    EmiPaths.append(os.path.join(DirPath_E,
                                 EmiiFile)
    )

E = []
for EmiiPath in EmiPaths:
    E.append(pd.read_csv(EmiiPath,
                         sep=";",
                         engine="python",
                         skiprows= 33,
                         skipfooter=1,
                         header=None,
                         names=["Longitud de Onda (nm)",
                                "Intensidad (u.a.)"]
                         )
    )

Wavelength = T[0]["Longitud de Onda (nm)"]
EIntensities = []

# CorrectIntTime = [7/20,1,1,1,1,1,1]
# CorrectIntTime = [1,1,7/1500,7/200,7/500,7/200,7/50,7/20,1,1,1,1,1,1]
# CorrectIntTime = [7/1500, 7/1500, 7/1500, 7/1500]
# CorrectIntTime = [1,1,1,1]
CorrectIntTime = [1]
for i,Ei in enumerate(E):
    EIntensities.append(Ei["Intensidad (u.a.)"]*CorrectIntTime[i])
    
    
    
#%%


''' Grafico Emisión '''


# Grafico Crudo
fig = plt.figure(5, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

DeltaxM = 200
Deltaxm = 2 
DeltayM =   0.2
Deltaym = 2

ax.xaxis.set_major_locator(MultipleLocator(DeltaxM))
ax.xaxis.set_minor_locator(AutoMinorLocator(Deltaxm))
ax.yaxis.set_major_locator(MultipleLocator(DeltayM))
ax.yaxis.set_minor_locator(AutoMinorLocator(Deltaym))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

n = len(EIntensities)
color=iter(cm.rainbow(np.linspace(0,1,n)))


for i, EIntensitiesi in enumerate(EIntensities):
    colour = next(color)
    ax.plot(Wavelength,
             EIntensitiesi,
             label=str(Labels[i],),
             color= colour
             )
    
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad (u. a)', fontsize=16)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          title='Muestra :',
          title_fontsize=15,
          fontsize=15)

#%%


''' Grafico Suavizado (Emisión) '''

SmoothE = []
for Ei in EIntensities:
    SmoothE.append(MA(Ei, 100))
    
    
fig = plt.figure(6, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

DeltaxM = 200
Deltaxm = 2 
DeltayM =   0.2
Deltaym = 2

ax.xaxis.set_major_locator(MultipleLocator(DeltaxM))
ax.xaxis.set_minor_locator(AutoMinorLocator(Deltaxm))
ax.yaxis.set_major_locator(MultipleLocator(DeltayM))
ax.yaxis.set_minor_locator(AutoMinorLocator(Deltaym))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

n = len(SmoothE)
color=iter(cm.rainbow(np.linspace(0,1,n)))


for i, SmoothEi in enumerate(SmoothE):
    colour = next(color)
    ax.plot(Wavelength,
             SmoothEi,
             label=str(Labels[i],),
             color= colour
             )
    
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad (u. a)', fontsize=16)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          title='Muestra :',
          title_fontsize=15,
          fontsize=15)

#%%

''' Grafico Emisión y Absorción para Muestra Particular '''


    
fig = plt.figure(7, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

DeltaxM = 200
Deltaxm = 2 
DeltayM =   0.2
Deltaym = 2

ax.xaxis.set_major_locator(MultipleLocator(DeltaxM))
ax.xaxis.set_minor_locator(AutoMinorLocator(Deltaxm))
ax.yaxis.set_major_locator(MultipleLocator(DeltayM))
ax.yaxis.set_minor_locator(AutoMinorLocator(Deltaym))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

for SmoothEi in SmoothE:
    ax.plot(Wavelength,
             SmoothEi,
             lw=1.5,
             label='Emisión',
             color='lightseagreen'
             )
for SmoothAi in SmoothA:
    ax.plot(Wavelength,
             SmoothAi,
             lw=1.5,
             label='Absorción',
             color='orange'
             )

ax.plot(LampWavelength,
          SmoothLamp,
          color="black",
          lw=1.5,
          label='Agua')
    
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad (u. a)', fontsize=16)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          title_fontsize=15,
          fontsize=15)
plt.title('Muestra 4', fontsize=15)

#%%

