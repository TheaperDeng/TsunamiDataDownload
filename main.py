#! /usr/bin/python
# -*- coding: utf-8 -*-

from earthquake import Earthquake
from GetUsgsData import GetUsgsData
from GetDartData import GetDartData
from ChooseDartStation import ChooseDartStation
from ChooseDartStation import ChooseiocStation
from settings import Settings
from RemoveTidesPolynomialFit import RemoveTidesPolynomialFit
from UpdateDartStation import UpdateDartStation
from RemoveTidesFilter import RemoveTidesFilter
from PlotMap import PlotMap
from GetiocData import GetiocData
from GenHTML import GenHTML
import re

def test():
    Earthquake_Settings=Settings()
    GetUsgsData(Earthquake_Settings)
    UpdateDartStation()
    earthquake=Earthquake()
    earthquake.printall('./cache/earthquake.csv')
    command=input('please input the number of earthquake you want to study>>> ')
    earthquake.initfrom('./cache/earthquake.csv',int(command))
    tar_Dart_station=ChooseDartStation(earthquake)
    tar_ioc_station=ChooseiocStation(earthquake)
    Dartstationnumvalid=[]
    iocstationnumvalid=[]

    for stationnum in tar_Dart_station:
        try:
            GetDartData(stationnum,earthquake)
            filename="./cache/DartData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv"
            RemoveTidesPolynomialFit(filename,earthquake)
            
            filename="./cache/DartData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv"
            RemoveTidesFilter(filename,earthquake,2*60*60)
            Dartstationnumvalid.append(stationnum)
        except:
            print("Sorry,no data for station",stationnum, "or something wrong with the process step.")
            continue
    for stationnum in tar_ioc_station:
        errorindex=GetiocData(stationnum,earthquake)
        if errorindex==-1:
            continue
        filename="./cache/iocData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv"
        RemoveTidesPolynomialFit(filename,earthquake)
        filename="./cache/iocData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv"
        RemoveTidesFilter(filename,earthquake,2*60*60)
        iocstationnumvalid.append(stationnum)
    print(Dartstationnumvalid,iocstationnumvalid)
    f1=open('./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+'/map.html','w')
    f1.write(r'<html><body><img src="Map.png" border="0" usemap="#planetmap"alt="Planets" /><map name="planetmap" id="planetmap">')
    f1.close()
    PlotMap(earthquake,Dartstationnumvalid,'./cache/DartStationRecord.csv',iocstationnumvalid,'./cache/iocStationRecord.csv')
    f1=open('./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+'/map.html','a')
    f1.write('</map></body></html>')
    f1.close()        
def GUIMAIN():
    while True:
        command=input(">>>")
        
test()