#! /usr/bin/python
# -*- coding: utf-8 -*-

from urllib import request
import re
import os
import csv

def UpdateDartStation():
    '''download a station list of Dart and some necessary stat'''
    urlNOAADartList = 'http://www.ndbc.noaa.gov/dart.shtml'#main page to get a list
    with request.urlopen(urlNOAADartList) as f:
        data=f.read()
        data=data.decode('utf-8')
        Temp=data.split('dartstns = [')[1].split('];',1)[0].replace("'","")
        stations = [x.strip() for x in Temp.split(',')]
        #print(stations)

    urlNOAAStationhead='http://www.ndbc.noaa.gov/station_page.php?station='
    longitude=[]
    latitude=[]
    waterdepth=[]
    for station in stations:
        print(station,"is updating")
        urlNOAAStation=urlNOAAStationhead+station
        #print(urlNOAAStation)
        with request.urlopen(urlNOAAStation) as f:
            data=f.read()
            data=data.decode('utf-8')
            Temp=data.split(station+' (',1)[1].split(')',1)[0]#Temp is row data of location(e.g.'134.342N 18.954W')
            try:
                Temp2=data.split('Water depth:</b> ',1)[1].split(' m')[0]
            except IndexError as e:
                Temp2='-1'
                
            #print(Temp)
            #print(Temp2)
            if re.match(r'(\d{1,3}.\d{3})N\s(\d{1,3}.\d{3})E',Temp):#use regex to match the string we get
                m=re.match(r'(\d{1,3}.\d{3})N\s(\d{1,3}.\d{3})E',Temp)
                latitude.append(m.group(1))
                longitude.append(m.group(2))
                waterdepth.append(Temp2)
                continue
            if re.match(r'(\d{1,3}.\d{3})S\s(\d{1,3}.\d{3})E',Temp):
                m=re.match(r'(\d{1,3}.\d{3})S\s(\d{1,3}.\d{3})E',Temp)
                latitude.append('-'+m.group(1))
                longitude.append(m.group(2))
                waterdepth.append(Temp2)
                continue
            if re.match(r'(\d{1,3}.\d{3})N\s(\d{1,3}.\d{3})W',Temp):
                m=re.match(r'(\d{1,3}.\d{3})N\s(\d{1,3}.\d{3})W',Temp)
                latitude.append(m.group(1))
                longitude.append('-'+m.group(2))
                waterdepth.append(Temp2)
                continue
            if re.match(r'(\d{1,3}.\d{3})S\s(\d{1,3}.\d{3})W',Temp):
                m=re.match(r'(\d{1,3}.\d{3})S\s(\d{1,3}.\d{3})W',Temp)
                latitude.append('-'+m.group(1))
                longitude.append('-'+m.group(2))
                waterdepth.append(Temp2)
                continue
            
    if os.path.exists('./cache'):#new cache folder for now and future
        pass
    else:
        os.mkdir('./cache')
    c=open("./cache/DartStationRecord.csv","w",newline='')#newline='' is for no empty line
    #print('Open correctly!')
    writer=csv.writer(c)#open the earthquake data cache file
    writer.writerow(['StationNumber','Longitude','Latitude','WaterDepth'])
    for station,longitude,latitude,waterdepth in zip(stations,longitude,latitude,waterdepth):
        Temp=[station,longitude,latitude,waterdepth]
        writer.writerow(Temp)
    c.close()
    print('Dart Station update!')

#updateDartStation()