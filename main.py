#! /usr/bin/python
# -*- coding: utf-8 -*-

from earthquake import Earthquake
from GetUsgsData import GetUsgsData
from GetDartData import GetDartData
from ChooseDartStation import ChooseDartStation
from settings import Settings
from RemoveTidesPolynomialFit import RemoveTidesPolynomialFit
from UpdateDartStation import UpdateDartStation
from RemoveTidesFilter import RemoveTidesFilter
import re

def test():
    Earthquake_Settings=Settings()
    GetUsgsData(Earthquake_Settings)
    UpdateDartStation()
    earthquake=Earthquake()
    earthquake.printall('./cache/earthquake.csv')
    command=input('please input the number of earthquake you want to study>>> ')
    earthquake.initfrom('./cache/earthquake.csv',int(command))
    tar_station=ChooseDartStation(earthquake)
    for stationnum in tar_station:
        try:
            GetDartData(stationnum,earthquake)
            filename="./cache/DartData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv"
            RemoveTidesPolynomialFit(filename,earthquake)
            filename="./cache/DartData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv"
            RemoveTidesFilter(filename,earthquake,2*60*60)
        except:
            print("Sorry,no data for station",stationnum, "or something wrong with the process step.")
            continue

            
            
def GUIMAIN():
    while True:
        command=input(">>>")
        
test()