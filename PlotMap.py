#! /usr/bin/python
# -*- coding: utf-8 -*-

'''Plot a map to virtrualize the location of stations and earthquake'''

__author__ = 'Junwei Deng'

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap 
import csv
from pylab import *
from earthquake import Earthquake
from GenHTML import GenHTML

def PlotMap(earthquake,stationnum,Filename,iocstationname,iocFilename):
    #You can use this function just like following:
        # earthquake=Earthquake()
        # earthquake.initfrom('./cache/earthquake.csv',24)
        # PlotMap(earthquake,['21413','43413', '32411', '42409', '32489', '32067', '32413', '46412', '44402', '32412'],'./cache/DartStationRecord.csv',['chia'],'./cache/iocStationRecord.csv')
    maxx=-1000
    minx=1000
    maxy=-1000
    miny=1000
    
    for station in stationnum:
        with open("./cache/DartStationRecord.csv","r",encoding="utf-8")as f:
            #print(maxy,maxx)
            reader=csv.reader(f)
            next(reader)
            for row in reader:
                if row[0]==station:
                    #print('qwq')
                    if maxx<=min(abs(float(row[1])-earthquake.epi[0]),360-abs(float(row[1])-earthquake.epi[0])):
                        maxx=min(abs(float(row[1])-earthquake.epi[0]),360-abs(float(row[1])-earthquake.epi[0]))
                    if maxy<=abs(float(row[2])-earthquake.epi[1]):
                        maxy=abs(float(row[2])-earthquake.epi[1])
            #print(maxy,maxx)
                
    for station in iocstationname:
        with open("./cache/iocStationRecord.csv","r",encoding="utf-8")as f:
            #print(maxy,maxx)
            reader=csv.reader(f)
            next(reader)
            for row in reader:
                if row[0]==station:
                    #print('qwq')
                    if maxx<=min(abs(float(row[1])-earthquake.epi[0]),360-abs(float(row[1])-earthquake.epi[0])):
                        maxx=min(abs(float(row[1])-earthquake.epi[0]),360-abs(float(row[1])-earthquake.epi[0]))
                    if maxy<=abs(float(row[2])-earthquake.epi[1]):
                        maxy=abs(float(row[2])-earthquake.epi[1])
            #print(maxy,maxx)
    #print(maxx,minx,maxy,miny)
    
    k1=(maxx*2+20)/10
    k2=k1
    # print(k2)
    if (k2<=17 and k2>=4):
        fig = plt.figure(figsize=(k1,k2))
        m = Basemap(projection='lcc', resolution=None,
        width=k1*1E6, height=k2*1E6,
        lat_0=earthquake.epi[1], lon_0=earthquake.epi[0],)
    if (k2>17):
        k1=30
        k2=17
        fig = plt.figure(figsize=(k1,k2))
        m = Basemap(projection='lcc', resolution=None,
        width=k1*1E6, height=k2*1E6,
        lat_0=2, lon_0=-165,)
    if (k2<4):
        k1=8
        k2=8
        fig = plt.figure(figsize=(k1,k2))
        m = Basemap(projection='lcc', resolution=None,
        width=k1*1E6, height=k2*1E6,
        lat_0=earthquake.epi[1], lon_0=earthquake.epi[0],)

    m.etopo(scale=0.5, alpha=0.5)
    x, y = m(earthquake.epi[0], earthquake.epi[1])
    q, e = m(0,0)
    #print(q,e)
    z, w = m(earthquake.epi[0]+1.5, earthquake.epi[1])
    plt.plot(x, y, '*r', markersize=18)
    plt.text(z, w, earthquake.depth+'km', fontsize=14,color = "r")
    for number in stationnum:
        with open(Filename) as f:
            reader=csv.reader(f)
            for row in reader:
                if row[0]==number: 
                        x, y = m(float(row[1]), float(row[2]))
                        # print(x,y)
                        z, w = m(float(row[1])+1.5, float(row[2]))
                        plt.plot(x, y, '^m', markersize=9)
                        plt.text(z, w, str(number), fontsize=12)
                        if (k1<1 and k2<1):
                            GenHTML('./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+'/map.html',x/10000,k2*100-y/10000,'DartData_'+number+'PolynomialFit')#DartData_32401PolynomialFit.png
                        else:
                            GenHTML('./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+'/map.html',x/10000,k2*100-y/10000,'DartData_'+number+'PolynomialFit')#DartData_32401PolynomialFit.png
    for name in iocstationname:
        with open(iocFilename) as f:
            reader=csv.reader(f)
            for row in reader:
                if row[0]==name:
                        x, y = m(float(row[1]), float(row[2]))
                        z, w = m(float(row[1])+1.5, float(row[2]))
                        plt.plot(x, y, 'ob', markersize=9)
                        plt.text(z, w, str(name), fontsize=12)
                        GenHTML('./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+'/map.html',x/10000,k2*100-y/10000,'iocData_'+name+'PolynomialFit')
    filename='./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+"/Map.png"
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
    savefig(filename)
    
# earthquake=Earthquake()
# earthquake.initfrom('./cache/earthquake.csv',24)
# PlotMap(earthquake,['21413','43413', '32411', '42409', '32489', '32067', '32413', '46412', '44402', '32412'],'./cache/DartStationRecord.csv',['chia'],'./cache/iocStationRecord.csv')