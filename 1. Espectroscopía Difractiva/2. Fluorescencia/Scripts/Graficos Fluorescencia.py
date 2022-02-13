# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 09:55:39 2022

@author: Cami_
"""

import os
import numpy as np
import pandas as pd
# from scipy import signal
# from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

#%%

''' Datos '''

DirPath = (r"C:\Users\Cami_\Documents\UBA\Laboratorio 5\1. Espectrometría Difractiva"
           r"\2. Fluorescencia\Mediciones 2\Absorcion")

DirPath2 = (r"C:\Users\Cami_\Documents\UBA\Laboratorio 5\1. Espectrometría Difractiva"
            r"\2. Fluorescencia\Mediciones 2\Emision")


LampFile    = r"Lámpara - Agua.csv"
TransFile   = r"4 - Trans - Cum.csv"
EmiFile     = r"4 - Emi - Cum.csv"


LampPath    = os.path.join(DirPath,
                           LampFile)
TransPath   = os.path.join(DirPath,
                           TransFile)
EmiPath     = os.path.join(DirPath2,
                           EmiFile)


Lamp    = pd.read_csv(LampPath,
                      sep=";",
                      engine="python",
                      skiprows= 33,
                      skipfooter=1,
                      header=None,
                      names=["Longitud de Onda (nm)",
                             "Intensidad (u.a.)"]
                      )

Trans   = pd.read_csv(TransPath,
                      sep=";",
                      engine="python",
                      skiprows= 33,
                      skipfooter=1,
                      header=None,
                      names=["Longitud de Onda (nm)",
                             "Intensidad (u.a.)"]
                      )

Emi     = pd.read_csv(EmiPath,
                      sep=";",
                      engine="python",
                      skiprows= 33,
                      skipfooter=1,
                      header=None,
                      names=["Longitud de Onda (nm)",
                             "Intensidad (u.a.)"]
                      )

print(Lamp)
print(Trans)
print(Emi)


# Lampara con Agua
LampWavelength  = Lamp["Longitud de Onda (nm)"]
LampIntensity   = Lamp["Intensidad (u.a.)"]

# Luz Transmitida Muestra 
TransWavelength = Trans["Longitud de Onda (nm)"]
TransIntensity  = Trans["Intensidad (u.a.)"]

# Luz Emitida Muestra
EmiWavelength   = Emi["Longitud de Onda (nm)"]
EmiIntensity    = Emi["Intensidad (u.a.)"]*7/2


#%%

''' Suavizador de Señal '''

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

SmoothLamp      = MA(LampIntensity, 100)
SmoothTrans     = MA(TransIntensity, 100)
SmoothEmi       = MA(EmiIntensity, 100)

#%%

''' Gráfico luz lampara y luz transmitida '''

# Crudo
fig = plt.figure(1, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(LampWavelength,
         LampIntensity,
         color="tab:blue",
         label='Lámpara')
ax.plot(TransWavelength,
         TransIntensity,
         color="tab:orange",
         label='Transmición')
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad', fontsize=16)
ax.legend(fontsize=15)

# Suavizado
fig = plt.figure(2, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(LampWavelength,
         SmoothLamp,
         color="tab:blue",
         lw=2,
         label='Lámpara')
ax.plot(TransWavelength,
         SmoothTrans,
         color="tab:orange",
         lw=2,
         label='Transmición')
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad', fontsize=16)
ax.legend(fontsize=15)


#%%

''' Defino Absorción '''

AbsRe = SmoothLamp - SmoothTrans

AbsTeo = 1 - SmoothTrans / SmoothLamp
Emi = SmoothEmi


''' Grafico '''
fig = plt.figure(3, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(LampWavelength,
         SmoothLamp,
         color="tab:blue",
         lw=2,
         label='Lámpara')
ax.plot(TransWavelength,
         SmoothTrans,
         color="tab:orange",
         lw=2,
         label='Transmición')
ax.plot(TransWavelength,
         AbsTeo,
         color="tab:red",
         lw=2,
         label='Absorción')
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad', fontsize=16)
ax.legend(fontsize=15)

#%%

''' Ahora todo junto '''

DeltaLongM = 200
DeltaLongm = 2 
DeltaIntM =   0.2
DeltaIntm = 2

fig = plt.figure(4, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

ax.xaxis.set_major_locator(MultipleLocator(DeltaLongM))
ax.xaxis.set_minor_locator(AutoMinorLocator(DeltaLongm))
ax.yaxis.set_major_locator(MultipleLocator(DeltaIntM))
ax.yaxis.set_minor_locator(AutoMinorLocator(DeltaIntm))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')


ax.plot(LampWavelength,
         SmoothLamp,
         color="tab:blue",
         lw=2,
         label='Lámpara')
ax.plot(EmiWavelength,
         Emi,
         color="tab:green",
         lw=2,
         label='Emisión')
ax.plot(TransWavelength,
         AbsTeo,
         color="tab:red",
         lw=2,
         label='Absorción')
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad', fontsize=16)
ax.legend(fontsize=15)

plt.title('Muestra II', fontsize=17)

#%%

# ''' Ley de Lamber-Beer '''

# I = I0 np.exp(epsilon * c * l)












#%%
