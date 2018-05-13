#! /usr/bin/python
# -*- coding: utf-8 -*-

class Settings():
    '''Setting class is a Input of all that filter condition of earthquakes'''
    def __init__(self):
        self.starttime='2010-01-01'#start at starttime
        self.endtime='2018-03-27'#end at endtime
        self.minmagnitude=7.5#only earthquakes which larger than 7.5 mag will be record
        self.maxdepth=50#only earthquakes which happened 50km or less will be record
        self.ifDartStationUpdate=True
        self.autoDartStationChoose=True
        self.manualDartStationList=['43413']
        self.autoiocStationChoose=True
        self.manualiocStationList=['chia']
        self.iocprs=True
        self.iocrad=True
        self.ifPolynomial=True
        self.Polynomiallevel=20
        self.Polynomiallastmin=150
        self.ifFilter=True
        self.Filtermaxperiod=2*60*60
        self.Filterlastmin=150