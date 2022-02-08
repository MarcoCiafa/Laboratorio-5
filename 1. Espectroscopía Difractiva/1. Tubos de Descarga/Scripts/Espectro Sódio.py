# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# %% Importar mediciones.

import os

DirPath = (r"C:\Users\marco\Documents\1. Facultad\2022 - 0° Verano"
           r"\Laboratorio 5\1. Espectroscopía Difractiva"
           r"\1. Tubos de Descarga\Mediciones\Na")

# FileNamePrefix = "Na - "

# IntegrationTime = [0.075,
#                    2,
#                    10,
#                    50,
#                    100,
#                    1000]

FileName = "Na - 1000"
FileNameSuffix = ".csv"


DATA = FileName + FileNameSuffix


FullPath = os.path.join(DirPath,
                        DATA)



import pandas as pd

DF = pd.read_csv(FullPath,
                 sep=";",
                 engine="python",
                 skiprows= 33,
                 skipfooter=1,
                 header=None,
                 names=["Longitud de Onda (nm)",
                        "Intensidad (u.a.)"]
                 )

print(DF)

Wavelength  = DF["Longitud de Onda (nm)"]
Intensity   = DF["Intensidad (u.a.)"]


# %% Graficar mediciones.

import matplotlib.pyplot as plt

plt.plot(Wavelength,
         Intensity)



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
