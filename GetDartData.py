#! /usr/bin/python
# -*- coding: utf-8 -*-

'''Get Dart station data by an earthquake and save it in a indentified csv file'''

__author__ = 'Junwei Deng'

from dateutil.parser import parse
from urllib import request
from earthquake import Earthquake 
import re,os,csv
from DateShift import DateShift

def getdarturl(stationnum,earthquake):
    '''joint a url website address'''
    urlhead='http://www.ndbc.noaa.gov/station_page.php?station='
    url=urlhead+stationnum+'&type=0&startyear='+str(DateShift(earthquake.date,-1)[0])+'&startmonth='+str(DateShift(earthquake.date,-1)[1])+'&startday='+str(DateShift(earthquake.date,-1)[2])+'&endyear='+str(DateShift(earthquake.date,1)[0])+'&endmonth='+str(DateShift(earthquake.date,1)[1])+'&endday='+str(DateShift(earthquake.date,1)[2])+'&submit=Submit'
        
    return url


def GetDartData(stationnum,earthquake):
    '''Get Dart station data by an earthquake and save it in a indentified csv file'''
    #You can directly use this function as following:
        # earthquake=Earthquake()
        # earthquake.initfrom('./cache/earthquake.csv',4)
        # GetDartData('43413',earthquake)
    url=getdarturl(stationnum,earthquake)
    print(url)
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
    req = request.Request(url, headers=head)
    with request.urlopen(req) as f:
        data=f.read()
        #print('Data:',data.decode('utf-8'))
        data=data.decode('utf-8')
        try:
            Temp=data.split('#yr  mo dy hr mn  s -      m')[1].split('</textarea></label></pre>',1)[0]#find the front of the data
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
            m=re.match(r'\s(\d{2})\s(\d{2})\s(\d{2})\s(\d{2})\s(\d{2})\s\d\s(\d{1,4}.\d{3})',Temp2)# 10 29 23 45 00 1 2773.538
            if m:
                a = parse(earthquake.date[0]+'-'+m[1]+'-'+m[2]+r'/'+m[3]+":"+m[4]+":"+m[5])# 2017-10-01/12:12:12
                #print(a)
                b = parse(earthquake.date[0]+'-'+earthquake.date[1]+'-'+earthquake.date[2]+'/'+earthquake.time_zero[0]+':'+earthquake.time_zero[1]+':'+earthquake.time_zero[2])
                relatime=(a-b).total_seconds()
                height_temp=m[6]
                rela_time.append(relatime)
                height.append(height_temp)
            else:
                relatime='Time(UTC)'

        c=open("./cache/DartData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv","w",newline='')#newline='' is for no empty line
        #print('Open correctly!')
        writer=csv.writer(c)#open the earthquake data cache file
        writer.writerow(['Relative Time','WaterDepth'])
        for rela_time,waterdepth in zip(rela_time,height):#9999.000 error is basically cleaned here
            if waterdepth=='9999.000':
                continue
            Temp=[rela_time,waterdepth]
            writer.writerow(Temp)
        c.close()
        print(stationnum, 'Dart Data Download!')
    
# earthquake=Earthquake()
# earthquake.initfrom('./cache/earthquake.csv',4)
# GetDartData('43413',earthquake)