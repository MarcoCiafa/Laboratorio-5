# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 08:16:27 2022

@author: Publico
"""


# %% Importar mediciones.

import os

#DirPath = (r"C:\Users\marco\Documents\1. Facultad\2022 - 0° Verano"
#           r"\Laboratorio 5\1. Espectroscopía Difractiva"
#           r"\2. Fluorescencia\Mediciones")

DirPath = (r"D:\Labo 5 - Verano 2022\Grupo 3\2. Fluorescencia"
           r"\Mediciones 2\Absorción")

DirPath2 = (r"D:\Labo 5 - Verano 2022\Grupo 3\2. Fluorescencia"
            r"\Mediciones 2\Emisión")


LampFile    = r"Lámpara - Agua.csv"
TransFile   = r"4 - Trans - Cum.csv"
EmiFile     = r"4 - Emi - Cum.csv"


LampPath    = os.path.join(DirPath,
                           LampFile)
TransPath   = os.path.join(DirPath,
                           TransFile)
EmiPath     = os.path.join(DirPath2,
                           EmiFile)

import pandas as pd

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


LampWavelength  = Lamp["Longitud de Onda (nm)"]
LampIntensity   = Lamp["Intensidad (u.a.)"]

TransWavelength = Trans["Longitud de Onda (nm)"]
TransIntensity  = Trans["Intensidad (u.a.)"]

# AbsWavelength = Trans["Longitud de Onda (nm)"]
# AbsIntensity  = 1 - Trans["Intensidad (u.a.)"]

#EmiWavelength   = Emi["Longitud de Onda (nm)"]
#EmiIntensity    = Emi["Intensidad (u.a.)"]


# %% Graficar mediciones.

import matplotlib.pyplot as plt

plt.figure(1)
plt.plot(LampWavelength,
         LampIntensity,
         color="tab:blue")
plt.plot(TransWavelength,
         TransIntensity,
         color="tab:orange")
plt.plot(EmiWavelength,
          EmiIntensity,
          color="tab:green")


# %% Suavizo la señal.

import numpy as np

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


plt.figure(2)
plt.plot(LampWavelength,
         SmoothLamp,
         color="tab:blue")
plt.plot(TransWavelength,
         SmoothTrans,
         color="tab:orange")
plt.plot(EmiWavelength,
          SmoothEmi,
          color="tab:green")




## %% Normalizo los espectros.
#
#SmoothNormLamp  = SmoothLamp    / max(SmoothLamp)
#SmoothNormTrans = SmoothTrans   / max(SmoothTrans)
#SmoothNormEmi   = SmoothEmi     / max(SmoothEmi)
#
#plt.figure(3)
#plt.plot(LampWavelength,
#         SmoothNormLamp,
#         color="tab:blue")
#plt.plot(TransWavelength,
#         SmoothNormTrans,
#         color="tab:orange")
##plt.plot(EmiWavelength,
##          SmoothNormEmi,
##          color="tab:green")


# %% Defino la Absorción

AbsRe = SmoothLamp - SmoothTrans

AbsTeo = 1 - SmoothTrans / SmoothLamp
Emi = SmoothEmi


plt.figure(4)
plt.plot(LampWavelength,
         SmoothNormLamp,
         color="tab:blue")
plt.plot(TransWavelength,
         AbsTeo,
         color="tab:orange")
#plt.plot(TransWavelength,
#         AbsRe,
#         color="tab:red")
plt.plot(EmiWavelength,
         Emi,
         color="tab:green")






# %% Determino la concenctración.

I = I0 np.exp(epsilon * c * l)





