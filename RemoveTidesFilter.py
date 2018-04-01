#! /usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import csv
from pylab import *
from scipy import signal
from earthquake import Earthquake
import os
def RemoveTidesFilter(Filename,earthquake,maxperiod):
    with open(Filename) as f:
        reader=csv.reader(f)
        next(reader)
        t=[]
        h=[]
        for row in reader:
            t.append(float(row[0]))
            h.append(float(row[1]))
        #print(t,h)
        t.reverse()
        h.reverse()
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
        #print(b,a,h)
        hout = signal.filtfilt(b,a,h)
        index1=0
        #print(t)
        for tsample in list(t):
            if tsample/60<0:
                index1=index1+1
        t=array(t[index1:size(t)-1])
        hout=array(hout[index1:size(hout)-1])
        #print(t,hout) 
        figure()
        plot(t/60,hout,linewidth=0.4)
        axes = plt.gca()
        axes.set_ylabel('Water Height[m]')
        axes.set_xlabel('Minutes after earthquake[min]')
        plt.title(Filename+'_Filter')
        if os.path.exists(earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]):#new cache folder for now and future
            pass
        else:
            os.mkdir(earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2])
        filename='./'+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+Filename.split("./cache")[1].split(earthquake.date[0])[0]+"filter.png"
        savefig(filename,dpi=800)
        c=open("./"+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+"/"+Filename.split("./cache")[1].split(earthquake.date[0])[0]+"filter.csv","w",newline='')#newline='' is for no empty line
        #print('Open correctly!')
        writer=csv.writer(c)#open the earthquake data cache file
        writer.writerow(['Relative Time','WaterDepth'])
        for rela_time,waterdepth in zip(list(t),list(hout)):
            Temp=[rela_time,waterdepth]
            writer.writerow(Temp)
        c.close()
        print("png file and csv of processed signal(by high-pass filter) is saved to",filename+'/.csv')

# earthquake=Earthquake()
# earthquake.initfrom('./cache/earthquake.csv',28)
# RemoveTidesFilter('./cache/DartData_2141620110311062550.csv',earthquake,2*60*60)
        