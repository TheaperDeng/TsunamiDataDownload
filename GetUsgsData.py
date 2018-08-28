#! /usr/bin/python
# -*- coding: utf-8 -*-

'''get USGS data for earthquake information'''

__author__ = 'Junwei Deng'


from settings import Settings
import csv
import requests
import os

def GetUrlFromSettings(Earthquake_Settings):
    '''Get the download url from USGS'''
    url='https://earthquake.usgs.gov/fdsnws/event/1/query.csv?'
    url=url+'starttime='+Earthquake_Settings.starttime
    url=url+'&endtime='+Earthquake_Settings.endtime
    url=url+'&minmagnitude='+str(Earthquake_Settings.minmagnitude)
    url=url+'&maxdepth='+str(Earthquake_Settings.maxdepth)
    return url

def GetUsgsData(Earthquake_Settings):
    '''Get earthquake data from USGS under filter and save as csv file'''
    #you can use it as following
        #Earthquake_Settings=Settings()
        #GetUsgsData(Earthquake_Settings)
    
    #Earthquake_Settings=Settings()
    url=GetUrlFromSettings(Earthquake_Settings)#get download url
    #print(url)

    if os.path.exists('./cache'):#new cache folder for now and future
        pass
    else:
        os.mkdir('./cache')
        
    c=open("./cache/earthquake.csv","w",newline='')#newline='' is for no empty line
    #print('Open correctly!')
    writer=csv.writer(c)#open the earthquake data cache file

    with requests.Session() as s:#save the file
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            #print(row)
            writer.writerow(row)
            
    c.close()#close the cache file
    print('USGS Download!')
    
#Earthquake_Settings=Settings()
#GetUsgsData(Earthquake_Settings)