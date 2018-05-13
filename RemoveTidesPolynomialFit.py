#! /usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import csv
from pylab import *
from earthquake import Earthquake   
import os
from settings import Settings
def RemoveTidesPolynomialFit(Filename,earthquake,Settings,starttime=-2500,endtime=1200):
    with open(Filename) as f:
        reader=csv.reader(f)
        next(reader)
        t=[]
        h=[]
        for row in reader:
            t.append(float(row[0]))
            h.append(float(row[1]))
        index1=0
        index2=0
        if t[0]>0:
            t.reverse()
            h.reverse()
        for tsample in t:
            if tsample/60<starttime:
                index1=index1+1
            if tsample/60<endtime:
                index2=index2+1
        t=array(t[index1:index2])
        h=array(h[index1:index2])
        z1=polyfit(t,h,Settings.Polynomiallevel)
        h=h-polyval(z1,t)
        
        ttemp=[]
        htemp=[]
        indexx=0
        for tsample in list(t):
            if tsample/60>0 and tsample/60<Settings.Polynomiallastmin:
                ttemp.append(tsample)
                htemp.append(list(h)[indexx])
            indexx=indexx+1
        t=array(ttemp)
        h=array(htemp)
        
        
        # #print(t,h)
        # index1=0
        # index2=0
        # for tsample in list(t):
            # if tsample/60>0:
                # index1=index1+1
        # t=array(t[0:index1])
        # h=array(h[0:index1])
        # #print(t,h)
        figure()

        plot(t/60,h,linewidth=0.4)
        axes = plt.gca()
        axes.set_ylabel('Water Height[m]')
        axes.set_xlabel('Minutes after earthquake[min]')
        axes.set_title(Filename+'_PolynomialFit')
        #show()
        if os.path.exists(earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]):#new cache folder for now and future
            pass
        else:
            os.mkdir(earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2])
        filename='./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+Filename.split("./cache")[1].split(earthquake.date[0])[0]+"PolynomialFit.png"
        savefig(filename,dpi=600)
        c=open("./"+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+"/"+Filename.split("./cache")[1].split(earthquake.date[0])[0]+"PolynomialFit.csv","w",newline='')#newline='' is for no empty line
        #print('Open correctly!')
        writer=csv.writer(c)#open the earthquake data cache file
        writer.writerow(['Relative Time','WaterDepth'])
        for rela_time,waterdepth in zip(list(t),list(h)):
            Temp=[rela_time,waterdepth]
            writer.writerow(Temp)
        c.close()
        print("png and csv file of processed signal(by polynomialfit) is saved to",filename+'/.csv')
#earthquake=Earthquake()
#earthquake.initfrom('./cache/earthquake.csv',1)
#RemoveTidesPolynomialFit('./cache/DartData_52402.csv',earthquake)