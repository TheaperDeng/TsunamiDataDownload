#! /usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import csv
from pylab import *
from earthquake import Earthquake
import os
def RemoveTidesPolynomialFit(Filename,earthquake,starttime=-2500,endtime=1200):
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
        for tsample in t:
            if tsample/60<starttime:
                index1=index1+1
            if tsample/60<endtime:
                index2=index2+1
        t=array(t[index1:index2])
        h=array(h[index1:index2])
        z1=polyfit(t,h,20)
        h=h-polyval(z1,t)
        #print(t,h)
        index1=0
        index2=0
        for tsample in list(t):
            if tsample/60>0:
                index1=index1+1
        t=array(t[0:index1])
        h=array(h[0:index1])
        #print(t,h)
        figure()
        plot(t,h,linewidth=0.4)
        #show()
        if os.path.exists(earthquake.date[0]+earthquake.date[1]+earthquake.date[2]):#new cache folder for now and future
            pass
        else:
            os.mkdir(earthquake.date[0]+earthquake.date[1]+earthquake.date[2])
        filename='./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+Filename.split("./cache")[1].split(earthquake.date[0])[0]+".png"
        savefig(filename,dpi=500)
        print("jpg file of processed signal is saved to",filename)
#earthquake=Earthquake()
#earthquake.initfrom('./cache/earthquake.csv',1)
#RemoveTidesPolynomialFit('./cache/DartData_52402.csv',earthquake)