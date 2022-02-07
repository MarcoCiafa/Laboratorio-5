
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:47:38 2022
@author: Labo5 v2022
"""
import pyvisa
import numpy as np
import time

class AFG(object):
    '''Clase para el manejo de generadores de funciones AFG3000 usando PyVISA de interfaz'''
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
    
    def generalSet(self, freq, voltage, offset = '0 V', shape = 'SIN', channel = 1):
        self.setFrequency(freq, channel)
        self.setVoltage(voltage, channel)
        self.setOffset(offset, channel)
        self.setShape(shape, channel)
    
