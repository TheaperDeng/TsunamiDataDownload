#! /usr/bin/python
# -*- coding: utf-8 -*-
from dateutil.parser import parse
from urllib import request
from bs4 import BeautifulSoup
import csv
import re
from earthquake import Earthquake 
from DateShift import DateShift
from settings import Settings

def GetiocData(stationnum,earthquake,Settings):
    ioc='http://www.ioc-sealevelmonitoring.org/bgraph.php?code='+stationnum+'&period=3&endtime='+str(DateShift(earthquake.date,2)[0])+'-'+str(DateShift(earthquake.date,2)[1])+'-'+str(DateShift(earthquake.date,2)[2])
    header={'User-Agent': 'Mozilla/5.0'}
    page=request.urlopen(ioc)
    soup=BeautifulSoup(page,"html.parser")
    print(ioc)
    filename="./cache/iocData_"+stationnum+earthquake.date[0]+earthquake.date[1]+earthquake.date[2]+earthquake.time_zero[0]+earthquake.time_zero[1]+earthquake.time_zero[2]+".csv"
    f = open(filename, 'w',newline='')
    csv_writer = csv.writer(f)
    
    time=''
    prs=''
    index=0
    timeindex=0
    prsindex=0
    radindex=0
    tables = soup.findAll('table')
    try:
        tab = tables[0]
    except:
        return -1
    for tr in tab.findAll('tr'):  
        for td in tr.findAll('td'):  
            if td.getText()=='Time (UTC)':
                timeindex=index
            if td.getText()=='prs(m)':
                prsindex=index
            if td.getText()=='rad(m)':
                radindex=index
            index=index+1
        break
    if (prsindex==0 or Settings.iocprs==False) and (radindex==0 or Settings.iocrad==False):
        return -1
    for tr in tab.findAll('tr'):  
        index=0
        for td in tr.findAll('td'): 
            if (index==timeindex):
                time=td.getText()
                m=re.match(r'(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})',time)#2017-09-08 00:00:00
                if m:
                    a = parse(m[1]+r"/"+m[2])# 2017-10-01/12:12:12
                    b = parse(earthquake.date[0]+'-'+earthquake.date[1]+'-'+earthquake.date[2]+'/'+earthquake.time_zero[0]+':'+earthquake.time_zero[1]+':'+earthquake.time_zero[2])
                    relatime=(a-b).total_seconds()
                    # relatime=0
                    # if int(m[1])-5>int(earthquake.date[2]):
                        # relatime=-86400
                    # if int(m[1])+5<int(earthquake.date[2]):
                        # relatime=86400
                    # relatime=relatime+(int(m[1])-int(earthquake.date[2]))*86400+(int(m[2])-int(earthquake.time_zero[0]))*3600+(int(m[3])-int(earthquake.time_zero[1]))*60+(int(m[4])-int(earthquake.time_zero[2]))*1
                else:
                    relatime='Time(UTC)'
            if (index==prsindex and prsindex!=0 and Settings.iocprs==True):
                prs=td.getText()
            if (index==radindex and radindex!=0 and Settings.iocrad==True and (Settings.iocprs==False or prsindex==0)):
                prs=td.getText()
            index=index+1
        #print(relatime,prs)
        try:
            csv_writer.writerow([ x for x in [relatime,prs]])
        except:
            continue
    return 0
# Setting=Settings()
# earthquake=Earthquake()
# earthquake.initfrom('./cache/earthquake.csv',19)
# GetiocData('orma',earthquake,Setting)