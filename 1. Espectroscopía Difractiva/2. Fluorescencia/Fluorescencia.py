# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# %% Importar mediciones.

import os

DirPath = (r"C:\Users\marco\Documents\1. Facultad\2022 - 0° Verano"
           r"\Laboratorio 5\1. Espectroscopía Difractiva"
           r"\2. Fluorescencia\Mediciones")

LampFile    = r"Lámpara - 6.csv"
TransFile   = r"Absorción\1. Rodamina (300 flecha 250) - 8.csv"
EmiFile     = r"Emisión\1. Rodamina (300 flecha 250) - 10000.csv"


LampPath    = os.path.join(DirPath,
                           LampFile)
TransPath   = os.path.join(DirPath,
                           TransFile)
EmiPath     = os.path.join(DirPath,
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

EmiWavelength   = Emi["Longitud de Onda (nm)"]
EmiIntensity    = Emi["Intensidad (u.a.)"]


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


# %% Normalizo los espectros.

SmoothNormLamp  = SmoothLamp    / max(SmoothLamp)
SmoothNormTrans = SmoothTrans   / max(SmoothTrans)
SmoothNormEmi   = SmoothEmi     / max(SmoothEmi)

plt.figure(3)
plt.plot(LampWavelength,
         SmoothNormLamp,
         color="tab:blue")
plt.plot(TransWavelength,
         SmoothNormTrans,
         color="tab:orange")
plt.plot(EmiWavelength,
          SmoothNormEmi,
          color="tab:green")


# %% Defino la Absorción

AbsTeo = 1 - SmoothNormTrans / SmoothNormLamp
Emi = SmoothEmi


plt.figure(4)
# plt.plot(LampWavelength,
#          SmoothNormLamp,
#          color="tab:blue")
plt.plot(TransWavelength,
         AbsTeo,
         color="tab:orange")
plt.plot(EmiWavelength,
         Emi,
         color="tab:green")












# %% Buscar máximos.

from scipy import signal
import numpy as np

Max, Propiedades = signal.find_peaks(Intensity,
                                      height= [0.05, 0.99],
                                     # threshold= 0.005,
                                      prominence= 0.05,
                                     # distance=1
                                     # width= [1,5]
                                     )

WavelengthMax   = np.array(Wavelength)[Max]
DeltaWavelength = Wavelength[1] - Wavelength[0]

IntensityMax    = np.array(Intensity)[Max]

print(f"Líneas Espectrales: {WavelengthMax}")

plt.plot(Wavelength,
         Intensity,
         ls="dashed",
         ms=2)
plt.scatter(WavelengthMax,
            IntensityMax,
            color= "red")
