#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:56:03 2022

@author: publico
"""

import pyvisa
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt





class Osciloscope(object):
    '''
    Clase para el manejo de osciloscopios TDS2000
    usando PyVISA de interfaz
    '''
    
    def __init__(self, instrument_number = 0):

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
    
    
    def getVoltageP2P(self, Canal= 1):
        
        self._osci.write(f'MEASUrement:IMMed:SOUrce CH{Canal}')
        self._osci.write("MEASUrement:IMMed:TYPe PK2pk")
        
        return self._osci.query_ascii_values('MEASUrement:IMMed:VALue?')
    
    def getWindow(self, canal, savedata= False):
        
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
        
        
        if savedata == True:
            
            dict_ = {"Tiempo": tiempo,
                     "Tensión": data}
            
            DF = pd.DataFrame(dict_)
            
            Path = (r"/home/publico/Desktop/L5 2022V - G3/"
                    r"0. Comunicación con Instrumentos/archivo.csv")
            
            DF.to_csv(Path,
                      header= True)

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
    
    
    
    
class AFG(object):
    '''
    Clase para el manejo de generadores de funciones 
    AFG3000 usando PyVISA de interfaz
    '''
    
    def __init__(self, instrument = 0):
      
        self.rm = pyvisa.ResourceManager('@py')
        
        if len(self.rm.list_resources()) > 0:
            self._inst = self.rm.open_resource(self.rm.list_resources()[instrument])
        else:
            self._inst = []
            print('No se detectó ningún instrumento')
        if self._inst != []:
            try:
                print('El IDN del instrumento es ', self._inst.query("*IDN?"))
            except:
                print('El instrumento no respondió cuando se le preguntó el nombre.')
    
    def __del__(self):
        self._inst.close()
        
        
    def turnOn(self, channel = 1):
        self._inst.write("OUTPut{}:STATe ON".format(channel))
        
    def turnOff(self, channel = 1):
        self._inst.write("OUTPut{}:STATe OFF".format(channel))
        
        
    def getFrequency(self, channel = 1):
        return self._inst.query_ascii_values('SOURce{}:FREQuency?'.format(channel))[0]
        
    def setFrequency(self, freq, channel = 1): #gen.SetFrequency('5 kHz') o por default en Hz
        self._inst.write("SOURce{}:FREQuency {}".format(channel,freq))    
        
        
    def getShape(self, channel = 1):
        return self._inst.query_ascii_values('SOURce{}:FUNCtion:SHAPe?'.format(channel), 
                                              converter = 's')[0]
    
    def setShape(self, shape, channel = 1): #gen.SetShape('SQUare')
        self._inst.write("SOURce{}:FUNCtion {}".format(channel,shape)) 
    
    
    def getVoltage(self, channel = 1):
        return self._inst.query_ascii_values('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude?'.format(channel))[0]
    
    def setVoltage(self, voltage, channel = 1): #gen.SetVoltage(2) Vpp
        self._inst.write('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude {}'.format(channel, voltage))
        
        
    def getOffset(self, channel = 1):
        return self._inst.query_ascii_values('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet?'.format(channel))[0]        
    
    def setOffset(self, offset, channel = 1): #gen.SetOffset(1) V
        self._inst.write('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet {}'.format(channel, offset))        
    
    
    def generalSet(self,
                    freq,
                    voltage,
                    offset = '0 V',
                    shape = 'SIN',
                    channel = 1):
        
        self.setFrequency(freq, channel)
        self.setVoltage(voltage, channel)
        self.setOffset(offset, channel)
        self.setShape(shape, channel)
        
    def Barrido(self,
                Amplitud,
                FrecuenciaInicial,
                FrecuenciaFinal,
                Paso,
                TiempoEnCadaFrec, # > 1.5s
                Canal= 1):
        
        Frecuencias = np.arange(FrecuenciaInicial,
                                FrecuenciaFinal,
                                Paso)
        
        self.setVoltage(voltage= Amplitud,
                        channel= Canal)

        for iFrecuencia in Frecuencias:
            
            self.setFrequency(freq= iFrecuencia,
                              channel = Canal)
            time.sleep(TiempoEnCadaFrec)
        





        
        
        
        


        
""" 0. """

osc = Osciloscope(0)
afg = AFG(1)

# Cerrar todo.
osc.__del__()
afg.__del__()



# # """ 1. """

# # FGfreq = 200
# # afg.setFrequency(FGfreq,
# #                  channel= 1)

# # scale = 2/(10 * FGfreq)
# # osc.setTimeScale(scale)


# # Time, Voltage = osc.getWindow(canal= 1)


# # import matplotlib.pyplot as plt
# # plt.plot(Time, Voltage)

# # """ 2. """

# # afg.Barrido(Amplitud= 1,
# #             FrecuenciaInicial= 100,
# #             FrecuenciaFinal= 200,
# #             Paso= 10,
# #             TiempoEnCadaFrec= 2, # > 1.5s
# #             Canal= 1)


# # """ 3. """

# # osc.getWindow(canal= 1, savedata= True)


""" 4. """

Canal = 1

def SúperBarrido(Amplitud,
            FrecuenciaInicial,
            FrecuenciaFinal,
            Paso,
            TiempoEnCadaFrec):
    
    Frecuencias = np.arange(FrecuenciaInicial,
                            FrecuenciaFinal,
                            Paso)
    
    afg.setVoltage(voltage= Amplitud,
                    channel= Canal)

    VolP2P = []
    
    for iFrecuencia in Frecuencias:
        
        afg.setFrequency(freq= iFrecuencia,
                          channel = Canal)
        time.sleep(TiempoEnCadaFrec)
        
        osc.getWindow(canal= 1, savedata= True)
        VolP2P.append(osc.getVoltageP2P(Canal= 1))
        
    return Frecuencias, VolP2P
    
    
Frecuencias, VolP2P = SúperBarrido(Amplitud= 1,
                                   FrecuenciaInicial= 100,
                                   FrecuenciaFinal= 200,
                                   Paso= 10,
                                   TiempoEnCadaFrec= 2)

plt.plot(Frecuencias, VolP2P)
    
