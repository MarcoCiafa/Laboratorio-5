# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:47:38 2022

@author: Labo5 v2022
"""

import pyvisa
import numpy as np

class Osciloscope(object):
    '''Clase para el manejo de osciloscopios TDS2000 usando PyVISA de interfaz'''
    def __init__(self, instrument_number = 0):
	#Defino el recurso
        rm = pyvisa.ResourceManager('@py')
        res = rm.list_resources()
        resource_name = res[instrument_number]
        self._osci = rm.open_resource(resource_name)
        self.id = self._osci.query("*IDN?")
        print('Osc name: ' + self.id)

	#Configuración de curva
        self._osci.write('DAT:ENC RPB') # Modo de transmision: Binario positivo. 
        self._osci.write('DAT:WID 1') #1 byte de dato. Con RPB 127 es la mitad de la pantalla
        self._osci.write("DAT:STAR 1") #La curva mandada inicia en el primer dato
        self._osci.write("DAT:STOP 2500") #La curva mandada finaliza en el último dato


        #Adquisición por sampleo
        self._osci.write("ACQ:MOD SAMP")
		
        #Seteo de canal
        # self.setCanal(canal = 1, escala = 20e-3)
        # self.setCanal(canal = 2, escala = 20e-3)
        # self.setTiempo(escala = 1e-3, cero = 0)
		
        #Bloquea el control del osciloscopio
        # self._osci.write("LOC ALL")

    def __del__(self):
        self._osci.write("UNL ALL") #Desbloquea el control del osciloscopio
        self._osci.close()

		
    def setTimeScale(self, escala, cero = 0):
        self._osci.write("HOR:SCA {0}".format(escala))
        self._osci.write("HOR:POS {0}".format(cero))	
	
        
    def getTimeScale(self):
        tdiv = self._osci.query_ascii_values('HOR:SCA?')[0]
        return tdiv
        
    def setVScale(self,scale,channel):
        self._osci.write('CH'+str(channel)+':VOLTS '+str(scale))
    

    def getVScale(self,channel):
        # self.write('CH'+str(channel)+':VOLTS '+str(scale))
        scale = self._osci.query_ascii_values('CH'+str(channel)+':VOLTS?')[0]
        return scale
   
    def setTrigger(self, level=0):
        self._osci.write('TRIG:MAIN:LEVEL {0}'.format(level))

    def getTrigger(self):
        return self._osci.query_ascii_values('TRIG:MAIN:LEVEL?')[0]
        
    def getWindow(self,canal):
        self._osci.write("SEL:CH{0} ON".format(canal)) #Hace aparecer el canal en pantalla. Por si no está habilitado
        self._osci.write("DAT:SOU CH{0}".format(canal)) #Selecciona el canal
	#xze primer punto de la waveform
	#xin intervalo de sampleo
	#ymu factor de escala vertical
	#yoff offset vertical
        xze, xin, yze, ymu, yoff = self._osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', 
                                                                 separator=';') 
        data = (self._osci.query_binary_values('CURV?', datatype='B', 
                                               container=np.array) - yoff) * ymu + yze        
        tiempo = xze + np.arange(len(data)) * xin
        return tiempo, data
    
    def setMeasurements(self):
         self._osci.write('MEASUrement:MEAS1:SOUrce CH1')
         self._osci.write('MEASUrement:MEAS1:TYPE PK2pk')
         self._osci.write('MEASUrement:MEAS1:UNITS V')
         
         
         self._osci.write('MEASUrement:MEAS2:SOUrce CH1')
         self._osci.write('MEASUrement:MEAS2:TYPE freq')
         self._osci.write('MEASUrement:MEAS2:UNITS HZ')
         
         self._osci.write('MEASUrement:MEAS3:SOUrce CH1')
         self._osci.write('MEASUrement:MEAS3:TYPE MEAN')
         self._osci.write('MEASUrement:MEAS3:UNITS V')
    
    def getMeasValues(self):
        v1 = self._osci.query_ascii_values('MEASUrement:MEAS1:VAL?')
        v2 = self._osci.query_ascii_values('MEASUrement:MEAS2:VAL?')
        v3 = self._osci.query_ascii_values('MEASUrement:MEAS3:VAL?')
        return v1,v2,v3
    