#! /usr/bin/python
# -*- coding: utf-8 -*-

from urllib import request
from earthquake import Earthquake 
import re,os,csv

def getdarturl(stationnum,earthquake):
    '''get the data form [stationnum]Dart and save it in a indentified csv file'''
    urlhead='http://www.ndbc.noaa.gov/station_page.php?station='
    url=urlhead+stationnum+'&type=0&startyear='+earthquake.date[0]+'&startmonth='+earthquake.date[1]+'&startday='+earthquake.date[2]+'&endyear='+earthquake.date[0]+'&endmonth='+earthquake.date[1]+'&endday='+earthquake.date[2]+'&submit=Submit'
    return url


def GetDartData(stationnum,earthquake):
    url=getdarturl(stationnum,earthquake)
    print(url)
    with request.urlopen(url) as f:
        data=f.read()
        #print('Data:',data.decode('utf-8'))
        data=data.decode('utf-8')
        Temp=data.split('#yr  mo dy hr mn  s -      m')[1].split('</textarea></label></pre>',1)[0]
        print(Temp)
        rela_time=[]
        height=[]
        while True:
            try:
                Temp2=Temp.split(earthquake.date[0],1)[1].split(earthquake.date[0],1)[0]
            except IndexError as e:
                break
            Temp=Temp.split(earthquake.date[0],1)[1]
            m=re.match(r'\s\d{2}\s\d{2}\s(\d{2})\s(\d{2})\s(\d{2})\s\d\s(\d{1,4}.\d{3})',Temp2)
            if m:
                #print(m[1],m[2],m[3],m[4])
                rela_time_temp=(int(m[1])-int(earthquake.time_zero[0]))*3600+(int(m[2])-int(earthquake.time_zero[1]))*60+(int(m[3])-int(earthquake.time_zero[2]))*1
                height_temp=m[4]
                rela_time.append(rela_time_temp)
                height.append(height_temp)
            else:
                break
        print(rela_time,height)
        if os.path.exists('./cache'):#new cache folder for now and future
            pass
        else:
            os.mkdir('./cache')
        c=open("./cache/DartData_"+stationnum+".csv","w",newline='')#newline='' is for no empty line
        #print('Open correctly!')
        writer=csv.writer(c)#open the earthquake data cache file
        writer.writerow(['Relative Time','WaterDepth'])
        for rela_time,waterdepth in zip(rela_time,height):
            Temp=[rela_time,waterdepth]
            writer.writerow(Temp)
        c.close()
        print('Done!')
    
earthquake=Earthquake()
earthquake.initfrom('./cache/earthquake.csv',1)
GetDartData('43413',earthquake)