import json
import requests
from urllib import request
from bs4 import BeautifulSoup
import csv
import operator

def GetiocStationData():
    StationNumber=[]
    Longitude=[]
    Latitude=[]
    a=0
    with request.urlopen('http://www.ioc-sealevelmonitoring.org/ssc/service.php?format=json') as download:
        data=download.read().decode('utf-8')
        file = open("code.json","w")
        file.write(data)
        file.close()
        with open('code.json') as f:
            ioc_raw_data=json.load(f)
            for ioc_raw_dict in ioc_raw_data:
                if a>=2201:
                    raw_data_station_web=request.urlopen('http://www.ioc-sealevelmonitoring.org/station.php?code='+ioc_raw_dict['ssc_id'].split('SSC-')[1]).read().decode('utf-8')
                    Temp=raw_data_station_web.split('data: {code: "')[1].split('"}')[0]
                    if Temp==ioc_raw_dict['ssc_id'].split('SSC-')[1]:
                        StationNumber.append(Temp)
                        Longitude.append(ioc_raw_dict['geo:lon'])
                        Latitude.append(ioc_raw_dict['geo:lat'])
                        print(Temp)
                a=a+1
                print(str(a)+'/2344')
                if(a>2343):
                    break
            c=open("./cache/iocStationRecord.csv","a",newline='')#newline='' is for no empty line
            writer=csv.writer(c)#open the earthquake data cache file
            #writer.writerow(['StationNumber','Longitude','Latitude'])
            for station,longitude,latitude in zip(StationNumber,Longitude,Latitude):
                Temp=[station,longitude,latitude]
                writer.writerow(Temp)
            c.close()
GetiocStationData()