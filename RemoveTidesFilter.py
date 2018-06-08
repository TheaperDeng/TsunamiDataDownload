#! /usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import csv
from pylab import *
from scipy import signal
from earthquake import Earthquake
from settings import Settings
import os
def RemoveTidesFilter(Filename,earthquake,maxperiod,Settings,starttime=-2500,endtime=1200):
    with open(Filename) as f:
        reader=csv.reader(f)
        next(reader)
        t=[]
        h=[]
        for row in reader:
            t.append(float(row[0]))
            h.append(float(row[1]))
        #print(t,h)
        if t[0]>0:
            t.reverse()
            h.reverse()
        index1=0
        index2=0
        for tsample in t:
            if tsample/60<starttime:
                index1=index1+1
            if tsample/60<endtime:
                index2=index2+1
        t=t[index1:index2]
        h=h[index1:index2]
        dtmax=-1
        dtmin=1000
        for i in range(1,size(t)):
            dttemp=abs(t[i]-t[i-1])
            if (dttemp>dtmax):
                dtmax=dttemp
            if (dttemp<dtmin):
                dtmin=dttemp
        if (dtmin!=dtmax):
            #print('hh')
            dt=60
            tval=range(int(t[0]),int(t[size(t)-1]),int(dt))
            #print(tval)
            hval=interp(tval,t,h)
            #print(tval,hval)
            t=array(tval)
            h=array(hval)
        else:
            #print('??')
            dt=dtmax
            t=array(t)
            h=array(h)
        #print(t,h)
        # plot(t,h,linewidth=0.4)
        # show()
        w = dt*2.0/maxperiod
        n0 = 7
        b,a = signal.butter(n0,w,'high')  
        # print(b,a,h)
        hout = signal.filtfilt(b,a,h)
        index1=0
        index2=0
        #print(t)
        for tsample in list(t):
            if tsample/60<0:
                index1=index1+1
            if tsample/60<Settings.Filterlastmin:
                index2=index2+1
                
        # t=array(t[index1:index2])
        # hout=array(hout[index1:index2])
        
        #print(t,hout) 
        figure()
        plot(t/60.0,hout,linewidth=0.4)
        
        axes = plt.gca()
        #axes.set_xlim([0,Settings.Filterlastmin])
        axes.set_ylabel('Water Height[m]')
        axes.set_xlabel('Minutes after earthquake[min]')
        x1,x2,y1,y2 = plt.axis()
        plt.axis((0,Settings.Filterlastmin,y1,y2))
        plt.title(Filename+'_Filter')
        if os.path.exists(earthquake.date[0]+earthquake.date[1]+earthquake.date[2]):#new cache folder for now and future
            pass
        else:
            os.mkdir(earthquake.date[0]+earthquake.date[1]+earthquake.date[2])
        filename='./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+Filename.split("./cache")[1].split(earthquake.date[0])[0]+"filter.png"
        savefig(filename,dpi=600)
        plt.close()
        c=open("./"+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+"/"+Filename.split("./cache")[1].split(earthquake.date[0])[0]+"filter.csv","w",newline='')#newline='' is for no empty line
        #print('Open correctly!')
        writer=csv.writer(c)#open the earthquake data cache file
        writer.writerow(['Relative Time','WaterDepth'])
        for rela_time,waterdepth in zip(list(t),list(hout)):
            Temp=[rela_time,waterdepth]
            writer.writerow(Temp)
        c.close()
        print("png file and csv of processed signal(by high-pass filter) is saved to",filename+'/.csv')

# earthquake=Earthquake()
# earthquake.initfrom('./cache/earthquake.csv',4)
# RemoveTidesFilter('./cache/iocData_huat20170908044919.csv',earthquake,2*60*60)
        