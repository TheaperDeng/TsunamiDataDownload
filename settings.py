#! /usr/bin/python
# -*- coding: utf-8 -*-

'''Setting class which can read config.cav to initialize the program'''

__author__ = 'Junwei Deng'

import csv

class Settings():
    def __init__(self):
        self.starttime='2010-01-01'#start at starttime
        self.endtime='2018-05-10'#end at endtime
        self.minmagnitude=7.5#only earthquakes which larger than 7.5 mag will be record
        self.maxdepth=50#only earthquakes which happened 50km or less will be record
        self.ifDartStationUpdate=False# Manually decide whether we need to update the DART station information
        self.autoDartStationChoose=50# The script will choose [autoDartStationChoose] DART stations nearest to the earthquakes
        self.manualDartStationList=[]# Only available if autoDartStationChoose is 0. Manually choose which DART station to study.
        self.autoiocStationChoose=50# The script will choose [autoiocStationChoose] stations nearest to the earthquakes
        self.manualiocStationList=[]# Only available if autoiocStationChoose is 0. Manually choose which ioc station to study.
        self.iocprs=True# Decide if we use the prs data in ioc stations
        self.iocrad=True# Only available if iocprs is false or there is no prs data. Decide if we use the rad data in ioc stations
        self.ifPolynomial=True# Decide if we use the Polynomial way to process the data.
        self.Polynomiallevel=20# The polynomial order
        self.Polynomiallastmin=150# The Tsunami data last for this long time.
        self.ifFilter=True# Decide if we use the Filter way to process the data.
        self.Filtermaxperiod=2*60*60# cutoff frequency of the Filter
        # Filterstartmin=distance./200(m/s)-1h vs 0
        self.Filterlastmin=150# The Tsunami data last for this long time.
        # farest+10
        # newwindows map???
    def inifrom(self,filename):
        with open(filename) as f:
            reader=csv.reader(f)
            for row in reader:
                if row[0]=='starttime':
                    self.starttime=row[1]
                if row[0]=='endtime':
                    self.endtime=row[1] 
                if row[0]=='minmagnitude':
                    self.minmagnitude=float(row[1])
                if row[0]=='maxdepth':
                    self.maxdepth=int(row[1])
                if row[0]=='ifDartStationUpdate':
                    if (row[1]=='yes' or row[1]=='y' or row[1]=='Yes' or float(row[1])>0):
                        self.ifDartStationUpdate=True
                    else:
                        self.ifDartStationUpdate=False
                if row[0]=='autoDartStationChoose':
                    self.autoDartStationChoose=int(row[1])
                if row[0]=='manualDartStationList':
                    for number in row[1:len(row)]:
                        self.manualDartStationList.append(number)
                if row[0]=='autoiocStationChoose':
                    self.autoiocStationChoose=int(row[1])
                if row[0]=='manualiocStationList':
                    for number in row[1:len(row)]:
                        self.manualiocStationList.append(number)
                if row[0]=='iocprs':
                    if (row[1]=='yes' or row[1]=='y' or row[1]=='Yes' or float(row[1])>0):
                        self.iocprs=True
                    else:
                        self.iocprs=False
                if row[0]=='iocrad':
                    if (row[1]=='yes' or row[1]=='y' or row[1]=='Yes' or float(row[1])>0):
                        self.iocrad=True
                    else:
                        self.iocrad=False
                if row[0]=='ifPolynomial':
                    if (row[1]=='yes' or row[1]=='y' or row[1]=='Yes' or float(row[1])>0):
                        self.ifPolynomial=True
                    else:
                        self.ifPolynomial=False
                if row[0]=='Polynomiallastmin':
                    self.Polynomiallastmin=int(row[1])
                if row[0]=='Filtermaxperiod':
                    self.Filtermaxperiod=int(row[1])
                if row[0]=='Filterlastmin':
                    self.Filterlastmin=int(row[1])
                if row[0]=='ifFilter':
                    if (row[1]=='yes' or row[1]=='y' or row[1]=='Yes' or float(row[1])>0):
                        self.ifFilter=True
                    else:
                        self.ifFilter=False
    def printfrom(self):
        print('starttime',self.starttime)
        print('endtime',self.endtime)
        print('minmagnitude',self.minmagnitude)
        print('maxdepth',self.maxdepth)
        print('ifDartStationUpdate',self.ifDartStationUpdate)
        print('autoDartStationChoose',self.autoDartStationChoose)
        print('manualDartStationList',self.manualDartStationList)
        print('autoiocStationChoose',self.autoiocStationChoose)
        print('manualiocStationList',self.manualiocStationList)
        print('iocprs',self.iocprs)
        print('iocrad',self.iocrad)
        print('ifPolynomial',self.ifPolynomial)
        print('Polynomiallevel',self.Polynomiallevel)
        print('Polynomiallastmin',self.Polynomiallastmin)
        print('ifFilter',self.ifFilter)
        print('Filtermaxperiod',self.Filtermaxperiod)
        print('Filterlastmin',self.Filterlastmin)
# settings=Settings()
# settings.inifrom('config.csv')
# settings.printfrom()