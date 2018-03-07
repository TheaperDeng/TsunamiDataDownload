#! /usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2, sys


print ('\n--> update DART stations list ...')

urlNOAADartList = 'http://www.ndbc.noaa.gov/dart.shtml'
req = urllib2.Request(urlNOAADartList)
response = urllib2.urlopen(req)
the_page = response.read()

s = the_page.split('dartstns =')[1]
s = s.strip().split('[')[1].split(']')[0].replace("'","")
stations = [x.strip() for x in s.split(',')]


print ('\n--> download DART stations location and water depth ...')

f = open('DARTStationsInfo'+'.info','w')
f.close()
f = open('StationsLocationAllDART.gmttxt','w')
f.write('Longitude Lattiude\n')
f.close()
f = open('StationsNamesAllDART.gmttxt','w')
f.close()
for IS in range(0,len(stations)):
	station = stations[IS]
	if(IS%5 == 0):
		sys.stdout.write('\n    '+station.ljust(10,' '))
	elif((IS+1)%5 == 0):
		sys.stdout.write(station)
	else:
		sys.stdout.write(station.ljust(10,' '))
	sys.stdout.flush()

	urlNOAADart = "http://www.ndbc.noaa.gov/station_page.php?station="+station
	req = urllib2.Request(urlNOAADart)
	response = urllib2.urlopen(req)
	the_page = response.read()

	lat = '-9999.0'; lon = '-9999.0'; wd = '-9999.0'
	if(the_page.find(' N ') != -1):
		l = the_page.split(' N '); ll = l[0].split('\n'); lat = ll[len(ll)-1].replace('<b>','').strip()
		if(l[1].find(' E ') != -1):
			lon = l[1].split(' E ')[0]
		else:
			lon = '-'+l[1].split(' W ')[0]
		if(the_page.lower().find('water depth:') != -1):
			wd = the_page.lower().split('water depth:')[1].split(' ')[1]
	elif(the_page.find(' S ') != -1):
		l = the_page.split(' S '); ll = l[0].split('\n'); lat = '-'+ll[len(ll)-1].replace('<b>','').strip()
		if(l[1].find(' E ') != -1):
			lon = l[1].split(' E ')[0]
		else:
			lon = '-'+l[1].split(' W ')[0]
		if(the_page.lower().find('water depth:') != -1):
			wd = the_page.lower().split('water depth:')[1].split(' ')[1]
	
	if(IS != len(stations)-1):
		s1 = station.ljust(10, ' ') + lon.ljust(10, ' ') + lat.ljust(9, ' ') + wd + '\n'
		s2 = lon+'\t'+lat+'\t'+station+'\n'
		s3 = lon+'\t'+lat+'\t'+'20'+'\t'+'0'+'\t'+'0'+'\tTC'+'\t'+station+'\n'
	else:
		s1 = station.ljust(10, ' ') + lon.ljust(10, ' ') + lat.ljust(9, ' ') + wd
		s2 = lon+'\t'+lat+'\t'+station
		s3 = lon+'\t'+lat+'\t'+'20'+'\t'+'0'+'\t'+'0'+'\tTC'+'\t'+station

	f = open('DARTStationsInfo'+'.info','a')
	f.write(s1)
	f.close()

	f = open('StationsLocationAllDART.gmttxt','a')
	f.write(s2)
	f.close()

	f = open('StationsNamesAllDART.gmttxt','a')
	f.write(s3)
	f.close()


print ('\n\n')
