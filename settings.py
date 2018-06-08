#! /usr/bin/python
# -*- coding: utf-8 -*-

class Settings():
    '''Setting class is a Input of all that filter condition of earthquakes'''
    def __init__(self):
        self.starttime='2010-01-01'#start at starttime
        self.endtime='2018-05-10'#end at endtime
        self.minmagnitude=7.5#only earthquakes which larger than 7.5 mag will be record
        self.maxdepth=50#only earthquakes which happened 50km or less will be record
        self.ifDartStationUpdate=True# Manually decide whether we need to update the DART station information
        self.autoDartStationChoose=5# The script will choose 5 DART stations nearest to the earthquakes
        self.manualDartStationList=['43413']# Only available if autoDartStationChoose is False. Manually choose which DART station to study.
        self.autoiocStationChoose=5# The script will choose first 1,3,5 ioc stations nearest to the earthquakes
        self.manualiocStationList=['chia']# Only available if autoiocStationChoose is False. Manually choose which ioc station to study.
        self.iocprs=True# Decide if we use the prs data in ioc stations
        self.iocrad=True# Only available if iocprs is false or there is no prs data. Decide if we use the rad data in ioc stations
        self.ifPolynomial=True# Decide if we use the Polynomial way to process the data.
        self.Polynomiallevel=20# The polynomial order
        self.Polynomiallastmin=150# The Tsunami data last for this long time.
        self.ifFilter=True# Decide if we use the Filter way to process the data.
        self.Filtermaxperiod=2*60*60# 傅里叶变换之后，高通滤波器的cutoff周期
        # Filterstartmin=distance./200(m/s)-1h vs 0
        self.Filterlastmin=150# The Tsunami data last for this long time.
        #(DARTmagenta)ok
        #(iocb)ok
        # farest+10
        # newwindows map???