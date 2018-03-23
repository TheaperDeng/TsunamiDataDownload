#! /usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import csv
from pylab import *

def RemoveTidesPolynomialFit(Filename,starttime=-2500,endtime=1200):
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
        figure()
        plot(t,h)
        #show()
        filename='.'+Filename.split("./cache")[1].split(".csv")[0]+".jpg"
        savefig(filename)
        print("jpg file of processed signal is saved to",filename)
#RemoveTidesPolynomialFit('./cache/DartData_52402.csv')