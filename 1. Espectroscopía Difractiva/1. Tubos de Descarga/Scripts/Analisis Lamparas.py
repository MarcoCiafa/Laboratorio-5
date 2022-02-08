# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 21:39:34 2022

@author: Cami_
"""
import numpy as np
import pandas as pd
from scipy import signal
from scipy import optimize
import matplotlib.pyplot as plt


#%%

''' Datos '''

file_path = r"C:\Users\Cami_\Documents\UBA\Laboratorio 5\1. Espectrometría Difractiva\1. Lamparas\Na\Na - 100.csv"
df = pd.read_csv(file_path,
                 sep=';',
                 skiprows=33,
                 skipfooter=1,
                 header=None,
                 engine='python')



LongOnda = df[0]
Intensidad = df[1]

''' Grafico '''

fig = plt.figure(1, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(LongOnda, Intensidad, color='darkviolet')
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad', fontsize=16)

#plt.title(r'$H_{2}$ (1 ms)', fontsize=16)

'''
 Colores:
     Ar: 'darkviolet'
     H2: 'mediumvioletred'
     He: 'gold'
     Hg: 'cornflowerble'
     Kr: 'mediumturquoise'
     Na: 'orange'
     Ne: 'orangered'
 '''


#%%

''' Buscador de Picos '''

# Aca hay que ir personalizando para cada caso (lo anoté todo en los txt)


Max, Propiedades =signal.find_peaks(Intensidad,
                                    height= [0.04, 1],
                                    prominence= 0,
                                    distance=1
                                    # threshold= 1e-2,
                                    # width= 10
                                    )
LongOnda_Max = np.array(LongOnda)[Max]
error_LongOnda_Max = (LongOnda[1] - LongOnda[0])
Intensidad_Max  = np.array(Intensidad)[Max]

print('Strong Lines : ')
print(LongOnda_Max)



# Grafico:

fig = plt.figure(2, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(LongOnda, Intensidad, color='darkviolet', zorder=0)
ax.scatter(LongOnda_Max, Intensidad_Max, color='indigo', zorder=5)
ax.set_xlabel('Longitud de Onda (nm)', fontsize=16)
ax.set_ylabel('Intensidad', fontsize=16)

#plt.title(r'$H_{2}$ (1 ms)', fontsize=16)
# ax.annotate(r'$H_{\sigma}$', (LongOnda_Max[0], Intensidad_Max[0]), fontsize=13)
# ax.annotate(r'$H_{\gamma}$', (LongOnda_Max[1], Intensidad_Max[1]), fontsize=13)
# ax.annotate(r'$H_{\beta}$', (LongOnda_Max[1], Intensidad_Max[1]), fontsize=13)
# ax.annotate(r'$H_{\alpha}$', (LongOnda_Max[3], Intensidad_Max[3]), fontsize=13)

'''
 Colores:
     Ar: 'darkviolet' - 'indigo'
     H2: 'mediumvioletred' - 'deeppink'
     He: 'gold' - 'orange'
     Hg: 'cornflowerble' - 'blue'
     Kr: 'mediumturquoise' - 'teal'
     Na: 'orange' - 'orangered'
     Ne: 'orangered' - 'red'
 '''


#%%

''' Grafico Espectral (? '''

# Lo hice pensando en el de H2. No terminé, no creo que sea muy importante.

Long_Onda_H = np.array([657.6014404, 487.0827332, 435.1246643, 411.757782])
x_ticks = [r'$H_{\alpha}$', r'$H_{\beta}$', r'$H_{\gamma}$', r'$H_{\sigma}$']

fig = plt.figure(3, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
plt.xticks(Long_Onda_H, x_ticks, fontsize=15)
for i in Long_Onda_H:
    ax.vlines(i, ymin=0, ymax=1, )


#%%

''' Calculo de la constante de Rydberg '''

n_1 = 2
Long_Onda_H = np.array([657.6014404, 487.0827332, 435.1246643, 411.757782])  # alpha, beta, gamma, sigma
n_2 = np.array([3, 4, 5, 6])


# Ajuste:

y_dt = 1/Long_Onda_H
x_dt = 1/(n_1**2) - 1/(n_2**2)

def funcion(x_dt, R):
    f = R*x_dt
    return f

def fit_curvefit(datax, datay, function):

    pfit, pcov = \
         optimize.curve_fit(funcion,datax,datay)
    error = []
    for i in range(len(pfit)):
        try:
          error.append(np.absolute(pcov[i][i])**0.5)
        except:
          error.append( 0.00 )
    pfit_curvefit = pfit
    perr_curvefit = np.array(error)
    return pfit_curvefit, perr_curvefit

pfit, perr = fit_curvefit(x_dt, y_dt, funcion)


# Constante de Rydberg:

R       = pfit[0] * (10**7)
error_R = perr[0] * (10**7)

print('Constante de Rydberg = ' + ' ( ' + str(R) + ' +/- ' + str(error_R) + ' ) ' + 'cm^-1')


# Grafico:

fig = plt.figure(3, figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(x_dt, y_dt, 'o', color='blue')
ax.plot(x_dt, funcion(x_dt, pfit), color = 'cornflowerblue', label = r'$R_{H}$ = (' + str(round(R)) + ' $\pm$ ' + str(round(error_R)) + ') $cm^{-1}$')
ax.set_xlabel(r'$1/n_{1}^{2} - 1/n_{2}^{2}$', fontsize=16)
ax.set_ylabel(r'$1/\lambda$ ($cm^{-1}$)', fontsize=16)
ax.set_title(r'Serie de Balmer ($n_{1} = 2$)', fontsize=16)
ax.legend(fontsize=14)


#%%







#%%
