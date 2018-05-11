#! /usr/bin/python
# -*- coding: utf-8 -*-

from urllib import request
from earthquake import Earthquake 
import re,os,csv
from DateShift import DateShift

def getdarturl(stationnum,earthquake):
    '''get the data form [stationnum]Dart and save it in a indentified csv file'''
    urlhead='http://www.ndbc.noaa.gov/station_page.php?station='
    url=urlhead+stationnum+'&type=0&startyear='+str(DateShift(earthquake.date,-1)[0])+'&startmonth='+str(DateShift(earthquake.date,-1)[1])+'&startday='+str(DateShift(earthquake.date,-1)[2])+'&endyear='+str(DateShift(earthquake.date,1)[0])+'&endmonth='+str(DateShift(earthquake.date,1)[1])+'&endday='+str(DateShift(earthquake.date,1)[2])+'&submit=Submit'
        
    return url


def GetDartData(stationnum,earthquake):
    url=getdarturl(stationnum,earthquake)
    print(url)
    with request.urlopen(url) as f:
        data=f.read()
        #print('Data:',data.decode('utf-8'))
        data=data.decode('utf-8')
        try:
            Temp=data.split('#yr  mo dy hr mn  s -      m')[1].split('</textarea></label></pre>',1)[0]
        except IndexError as e:
            return
        #print(Temp)
        rela_time=[]
        height=[]
        while True:
            try:
                Temp2=Temp.split(earthquake.date[0],1)[1].split(earthquake.date[0],1)[0]
            except IndexError as e:
                break
            Temp=Temp.split(earthquake.date[0],1)[1]
            #print(Temp2)
            m=re.match(r'\s\d{2}\s(\d{2})\s(\d{2})\s(\d{2})\s(\d{2})\s\d\s(\d{1,4}.\d{3})',Temp2)
            if m:
                rela_time_temp=0
                #print(m[1],m[2],m[3],m[4])
                # rela_time_temp=(int(m[1])-int(earthquake.time_zero[0]))*3600+(int(m[2])-int(earthquake.time_zero[1]))*60+(int(m[3])-int(earthquake.time_zero[2]))*1
                if int(m[1])-5>int(earthquake.date[2]):
                    rela_time_temp=-86400
                if int(m[1])+5<int(earthquake.date[2]):
                    rela_time_temp=86400
                rela_time_temp=rela_time_temp+(int(m[1])-int(earthquake.date[2]))*86400+(int(m[2])-int(earthquake.time_zero[0]))*3600+(int(m[3])-int(earthquake.time_zero[1]))*60+(int(m[4])-int(earthquake.time_zero[2]))*1
                height_temp=m[5]
                rela_time.append(rela_time_temp)
                height.append(height_temp)
            else:
                break
        #print(rela_time,height)
        c=open("./cache/DartData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv","w",newline='')#newline='' is for no empty line
        #print('Open correctly!')
        writer=csv.writer(c)#open the earthquake data cache file
        writer.writerow(['Relative Time','WaterDepth'])
        for rela_time,waterdepth in zip(rela_time,height):
            if waterdepth=='9999.000':
                continue
            Temp=[rela_time,waterdepth]
            writer.writerow(Temp)
        c.close()
        print(stationnum, 'Dart Data Download!')
    
# earthquake=Earthquake()
# earthquake.initfrom('./cache/earthquake.csv',4)
# GetDartData('43413',earthquake)