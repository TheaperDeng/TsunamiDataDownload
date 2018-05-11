#! /usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap 
import csv
from pylab import *
from earthquake import Earthquake
from GenHTML import GenHTML

def PlotMap(earthquake,stationnum,Filename,iocstationname,iocFilename):
    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution=None,
    width=8E6, height=8E6,
    lat_0=earthquake.epi[1], lon_0=earthquake.epi[0],)
    m.etopo(scale=0.5, alpha=0.5)
    x, y = m(earthquake.epi[0], earthquake.epi[1])
    print(x,y)
    z, w = m(earthquake.epi[0]+1.5, earthquake.epi[1])
    plt.plot(x, y, '*r', markersize=18)
    plt.text(z, w, earthquake.depth+'km', fontsize=14,color = "r")
    for number in stationnum:
        with open(Filename) as f:
            reader=csv.reader(f)
            for row in reader:
                if row[0]==number:
                        x, y = m(float(row[1]), float(row[2]))
                        print(x,y)
                        z, w = m(float(row[1])+1.5, float(row[2]))
                        plt.plot(x, y, '^k', markersize=9)
                        plt.text(z, w, str(number), fontsize=12)
                        GenHTML('./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+'/map.html',x/10000,800-y/10000,'DartData_'+number+'PolynomialFit')#DartData_32401PolynomialFit.png
    for name in iocstationname:
        with open(iocFilename) as f:
            reader=csv.reader(f)
            for row in reader:
                if row[0]==name:
                        x, y = m(float(row[1]), float(row[2]))
                        z, w = m(float(row[1])+1.5, float(row[2]))
                        plt.plot(x, y, 'ok', markersize=9)
                        plt.text(z, w, str(name), fontsize=12)
                        GenHTML('./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+'/map.html',x/10000,800-y/10000,'iocData_'+name+'PolynomialFit')
    filename='./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+"/Map.png"
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
    savefig(filename)
# earthquake=Earthquake()
# earthquake.initfrom('./cache/earthquake.csv',4)
# PlotMap(earthquake,['42409','43413','32489','32411'],'./cache/DartStationRecord.csv',['chia'],'./cache/iocStationRecord.csv')